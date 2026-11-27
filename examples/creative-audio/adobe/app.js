import addOnUISdk from "https://express.adobe.com/static/add-on-sdk/sdk.js";
import { mountPanel } from "../shared/panel.js";
import "../shared/panel.css";
await addOnUISdk.ready;
mountPanel(document.querySelector("main"), async ({ title, url }) => {
  const file = await fetch(url, { credentials: "omit", referrerPolicy: "no-referrer" });
  if (!file.ok) throw new Error("Audio download returned HTTP " + file.status + ".");
  const blob = await file.blob();
  if (!blob.size) throw new Error("The audio download was empty.");
  await addOnUISdk.app.document.addAudio(blob, { title });
});
