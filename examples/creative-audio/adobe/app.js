import addOnUISdk from "https://express.adobe.com/static/add-on-sdk/sdk.js";
import { mountPanel } from "../shared/panel.js";
import "../shared/panel.css";
async function insertTrack({ title, url }) {
  const file = await fetch(url, { credentials: "omit", referrerPolicy: "no-referrer" });
  if (!file.ok) throw new Error("Audio download returned HTTP " + file.status + ".");
  const blob = await file.blob();
  if (!blob.size) throw new Error("The audio download was empty.");
  await addOnUISdk.app.document.addAudio(blob, { title });
}

await addOnUISdk.ready;
mountPanel(document.querySelector("#tasks"), insertTrack);

const button = document.querySelector("#add-sample");
const player = document.querySelector("#sample-player");
const status = document.querySelector("#sample-status");
button.addEventListener("click", async () => {
  button.disabled = true;
  try {
    await insertTrack({ title: "Studio chimes", url: player.src });
    status.textContent = "Sample added.";
  } catch {
    status.textContent = "Could not add the sample to this design.";
  } finally {
    button.disabled = false;
  }
});
