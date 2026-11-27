export async function fetchTracks(token, taskId, send = fetch) {
  const id = taskId.trim();
  if (!id || !token.trim()) throw new Error("Enter an application token and an existing task ID.");
  const response = await send("https://api.acedata.cloud/acemusic/tasks", {
    method: "POST", redirect: "error", credentials: "omit",
    headers: { Authorization: "Bearer " + token.trim(), "Content-Type": "application/json" },
    body: JSON.stringify({ action: "retrieve", id }),
  });
  if (!response.ok) throw new Error("Task lookup returned HTTP " + response.status + ".");
  const result = await response.json();
  const group = result.response ?? {};
  if (result.id !== id || (group.task_id != null && group.task_id !== id)) {
    throw new Error("The returned task ID differs from the requested task.");
  }
  const tracks = Array.isArray(group.data) ? group.data.flatMap((item) => {
    if (!item || typeof item.audio_url !== "string") return [];
    let url;
    try { url = new URL(item.audio_url); } catch { return []; }
    if (url.protocol !== "https:" || url.username || url.password) return [];
    return [{ title: item.title || "ACE Music track", url: url.href,
              durationMs: Math.round(Number(item.duration) * 1000) }];
  }) : [];
  return { state: group.status || result.state || "pending", tracks };
}

export async function generateTrack(token, prompt, key, send = fetch) {
  if (!token.trim() || !prompt.trim()) throw new Error("Enter an application token and describe the soundtrack.");
  const response = await send("https://api.acedata.cloud/acemusic/audios", {
    method: "POST", redirect: "error", credentials: "omit",
    headers: { Authorization: "Bearer " + token.trim(), "Content-Type": "application/json", "Idempotency-Key": key },
    body: JSON.stringify({ action: "generate", custom: false, async: true, model: "acemusic-v1.1",
      prompt: prompt.trim() }),
  });
  const result = await response.json();
  if (!response.ok || result.success === false || typeof result.task_id !== "string" || !result.task_id) {
    throw new Error("No confirmed task ID. Check your Ace task history before submitting again.");
  }
  return result.task_id;
}
