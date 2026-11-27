import addOnUISdk from "https://express.adobe.com/static/add-on-sdk/sdk.js";
import { mountPanel } from "../shared/panel.js";
import "../shared/panel.css";
import { mountMediaImport } from "./media.js";

async function insertMedia({ type = "audio", title, url }) {
  const file = await fetch(url, { credentials: "omit", referrerPolicy: "no-referrer" });
  if (!file.ok) throw new Error("Media download returned HTTP " + file.status + ".");
  const blob = await file.blob();
  if (!blob.size) throw new Error("The media download was empty.");
  const doc = addOnUISdk.app.document;
  if (type === "image") await doc.addImage(blob, { title });
  else if (type === "video") await doc.addVideo(blob, { title });
  else await doc.addAudio(blob, { title });
}

await addOnUISdk.ready;
mountPanel(document.querySelector("#tasks"), insertMedia);
mountMediaImport(document.querySelector("#media"), insertMedia);

const button = document.querySelector("#add-sample");
const player = document.querySelector("#sample-player");
const status = document.querySelector("#sample-status");
button.addEventListener("click", async () => {
  button.disabled = true;
  try {
    await insertMedia({ title: "Studio chimes", url: player.src });
    status.textContent = "Sample added.";
  } catch {
    status.textContent = "Could not add the sample to this design.";
  } finally {
    button.disabled = false;
  }
});
