import { fetchTracks, generateTrack } from "./tasks.js";

export function mountPanel(root, insertTrack) {
  root.innerHTML = `<form><label>Application token<input type="password" autocomplete="off" required></label>
    <label>Existing ACE Music task ID<input type="text" required></label>
    <button>Find tracks</button></form>
    <details><summary>Create a soundtrack</summary><form><label>Describe the soundtrack<textarea required></textarea></label>
    <p>Generation uses your Ace application credits. You can listen before adding a track.</p>
    <button>Generate with credits</button></form></details>
    <p aria-live="polite"></p><section></section>
    <a href="https://platform.acedata.cloud/console/applications" target="_blank" rel="noopener noreferrer">Get an application token</a>`;
  const form = root.querySelector("form");
  const [token, task] = form.querySelectorAll("input");
  const status = root.querySelector("p");
  const results = root.querySelector("section");
  const generation = root.querySelector("details form");
  const generateButton = generation.querySelector("button");
  let attempt;
  generation.onsubmit = async (event) => {
    event.preventDefault();
    const prompt = generation.querySelector("textarea").value.trim();
    if (!token.value.trim()) { status.textContent = "Enter your Ace application token first."; return; }
    if (!attempt || attempt.prompt !== prompt) attempt = { prompt, key: crypto.randomUUID() };
    generateButton.disabled = true;
    try {
      const id = await generateTrack(token.value, prompt, attempt.key);
      task.value = id;
      root.querySelector("details").open = false;
      status.textContent = "Task accepted. Save its ID and use Find tracks to check the original task.";
      attempt = undefined;
    } catch (error) {
      status.textContent = "Submission was not confirmed. Check your Ace task history before retrying.";
    } finally { generateButton.disabled = false; }
  };
  let requestNumber = 0;
  form.onsubmit = async (event) => {
    event.preventDefault();
    const request = ++requestNumber;
    results.replaceChildren();
    status.textContent = "Looking up your task…";
    try {
      const { state, tracks } = await fetchTracks(token.value, task.value);
      if (request !== requestNumber) return;
      status.textContent = "Task status: " + state + ". " + tracks.length + " tracks available.";
      for (const track of tracks) {
        const card = document.createElement("article");
        const title = document.createElement("strong");
        title.textContent = track.title;
        const player = document.createElement("audio");
        player.controls = true; player.preload = "none"; player.src = track.url;
        const button = document.createElement("button");
        button.textContent = "Add track to design";
        button.onclick = async () => {
          button.disabled = true;
          try { await insertTrack(track); if (request === requestNumber) status.textContent = "Track added."; }
          catch (error) { if (request === requestNumber) status.textContent = error.message || "Could not insert this track."; }
          finally { button.disabled = false; }
        };
        card.append(title, player, button); results.append(card);
      }
    } catch (error) {
      if (request === requestNumber) status.textContent = error.message || "Task lookup failed.";
    }
  };
}
