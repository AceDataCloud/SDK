import { fetchTracks, generateTrack } from "./tasks.js";
import messages from "./messages.json";

function english(id, values = {}) {
  return messages[id].defaultMessage.replace(/\{(\w+)\}/g, (_, key) => String(values[key]));
}

export function mountPanel(root, insertTrack, translate = english, openLink) {
  root.innerHTML = `<form><label><span data-message="appToken"></span><input type="password" autocomplete="off" required></label>
    <label><span data-message="taskId"></span><input type="text" required></label>
    <button data-message="find"></button></form>
    <details><summary data-message="create"></summary><form><label><span data-message="prompt"></span><textarea required></textarea></label>
    <p data-message="cost"></p><button data-message="generate"></button></form></details>
    <p aria-live="polite"></p><section></section>
    <a data-message="getToken" href="https://platform.acedata.cloud/console/applications" target="_blank" rel="noopener noreferrer"></a>`;
  for (const element of root.querySelectorAll("[data-message]")) {
    element.textContent = translate(element.dataset.message);
  }
  if (openLink) root.querySelector("a").onclick = (event) => {
    event.preventDefault();
    openLink(event.currentTarget.href);
  };
  const form = root.querySelector("form");
  const [token, task] = form.querySelectorAll("input");
  const status = root.querySelector("[aria-live]");
  const results = root.querySelector("section");
  const generation = root.querySelector("details form");
  const generateButton = generation.querySelector("button");
  let attempt;
  generation.onsubmit = async (event) => {
    event.preventDefault();
    const prompt = generation.querySelector("textarea").value.trim();
    if (!token.value.trim()) { status.textContent = translate("tokenRequired"); return; }
    if (!attempt || attempt.prompt !== prompt) attempt = { prompt, key: crypto.randomUUID() };
    generateButton.disabled = true;
    try {
      const id = await generateTrack(token.value, prompt, attempt.key);
      task.value = id;
      root.querySelector("details").open = false;
      status.textContent = translate("accepted");
      attempt = undefined;
    } catch (error) {
      status.textContent = translate("uncertain");
    } finally { generateButton.disabled = false; }
  };
  let requestNumber = 0;
  form.onsubmit = async (event) => {
    event.preventDefault();
    const request = ++requestNumber;
    results.replaceChildren();
    status.textContent = translate("searching");
    try {
      const { state, tracks } = await fetchTracks(token.value, task.value);
      if (request !== requestNumber) return;
      status.textContent = translate("results", {state, count: tracks.length});
      for (const track of tracks) {
        const card = document.createElement("article");
        const title = document.createElement("strong");
        title.textContent = track.title;
        const player = document.createElement("audio");
        player.controls = true; player.preload = "none"; player.src = track.url;
        const button = document.createElement("button");
        button.textContent = translate("insert");
        button.onclick = async () => {
          button.disabled = true;
          try { await insertTrack(track); if (request === requestNumber) status.textContent = translate("inserted"); }
          catch (error) { if (request === requestNumber) status.textContent = translate(error.message === "unsupported" || error.message === "durationMissing" ? error.message : "insertFailed"); }
          finally { button.disabled = false; }
        };
        card.append(title, player, button); results.append(card);
      }
    } catch (error) {
      if (request === requestNumber) status.textContent = translate("lookupFailed");
    }
  };
}
