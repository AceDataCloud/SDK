const services = new Map([
  ["suno", { name: "Suno", type: "audio", field: "audio_url" }],
  ["nano-banana", { name: "Nano Banana", type: "image", field: "image_url" }],
  ["openai", { name: "GPT Image", type: "image", field: "url" }],
  ["seedream", { name: "Seedream", type: "image", field: "image_url" }],
  ["flux", { name: "Flux", type: "image", field: "image_url" }],
  ["seedance", { name: "Seedance", type: "video", field: "video_url" }],
  ["kling", { name: "Kling", type: "video", field: "video_url" }],
  ["veo", { name: "Veo", type: "video", field: "video_url" }],
  ["hailuo", { name: "Hailuo", type: "video", field: "video_url" }],
]);

export async function fetchMedia(service, token, id, send = fetch) {
  const spec = services.get(service);
  if (!spec || !token || !id) throw new Error("Choose a media service and enter its application token and task ID.");
  const response = await send("https://api.acedata.cloud/" + service + "/tasks", {
    method: "POST", redirect: "error", credentials: "omit",
    headers: { Authorization: "Bearer " + token, "Content-Type": "application/json" },
    body: JSON.stringify({ action: "retrieve", id }),
  });
  if (!response.ok) throw new Error("Task lookup returned HTTP " + response.status + ".");
  const record = await response.json();
  const result = record?.response;
  if (record?.id !== id || (result?.task_id != null && result.task_id !== id)) {
    throw new Error("The returned task ID differs from the requested task.");
  }
  let rows = Array.isArray(result?.data) ? result.data : [];
  if (service === "seedance") rows = [result?.data?.content];
  if (service === "kling") rows = [result];
  const items = [];
  for (const row of rows) {
    const value = row?.[spec.field];
    if (typeof value !== "string") continue;
    let url;
    try { url = new URL(value); } catch { continue; }
    if (url.protocol !== "https:" || url.username || url.password) continue;
    items.push({ type: spec.type, title: row.title || spec.name + " " + (items.length + 1), url: url.href });
  }
  const state = result?.status || result?.state || result?.data?.status || record.state || record.status ||
    (result?.success === false || result?.error ? "failed" : rows.find(row => row?.state)?.state) ||
    (record.finished_at || items.length || result?.success === true ? "completed" : "pending");
  return { state, items };
}

export function mountMediaImport(root, addMedia) {
  const select = root.querySelector("select");
  for (const [service, spec] of services) select.add(new Option(spec.name, service));
  const form = root.querySelector("form");
  const results = root.querySelector("section");
  const status = root.querySelector("[role=status]");
  let revision = 0;
  function reset() {
    revision++;
    results.replaceChildren();
    status.textContent = "";
  }
  select.addEventListener("change", () => { reset(); form.elements.token.value = ""; form.elements.task.value = ""; });
  form.addEventListener("input", reset);
  async function lookup(event) {
    event.preventDefault();
    if (!form.reportValidity()) return;
    reset();
    const current = revision;
    status.textContent = "Looking up task…";
    try {
      const { state, items } = await fetchMedia(select.value, form.elements.token.value.trim(), form.elements.task.value.trim());
      if (current !== revision) return;
      status.textContent = state + " · " + items.length + (items.length === 1 ? " item" : " items");
      for (const item of items) {
        const card = document.createElement("article");
        const title = document.createElement("strong");
        title.textContent = item.title;
        const preview = document.createElement(item.type === "image" ? "img" : item.type);
        preview.style.maxWidth = "100%";
        if (item.type === "image") { preview.alt = item.title; preview.referrerPolicy = "no-referrer"; }
        else { preview.controls = true; preview.preload = "none"; }
        preview.src = item.url;
        const button = document.createElement("button");
        button.type = "button";
        button.textContent = "Add " + item.type + " to design";
        button.onclick = async () => {
          button.disabled = true;
          try { await addMedia(item); if (revision === current) status.textContent = "Added to design."; }
          catch { if (revision === current) status.textContent = "Could not import this file. Check its URL, format and size."; }
          finally { button.disabled = false; }
        };
        card.append(title, preview, button);
        results.append(card);
      }
    } catch (error) {
      if (revision === current) status.textContent = error.message || "Unable to retrieve this task.";
    }
  }
  // Express sandbox blocks native form submission before the submit event fires.
  form.querySelector("button").addEventListener("click", lookup);
  form.addEventListener("submit", lookup);
}
