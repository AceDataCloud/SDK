import { upload } from "@canva/asset";
import { addAudioTrack } from "@canva/design";
import { features } from "@canva/platform";
import { mountPanel } from "../shared/panel.js";
import "../shared/panel.css";

const panel = document.createElement("main");
document.body.append(panel);
mountPanel(panel, async ({ title, url, durationMs }) => {
  if (!features.isSupported(addAudioTrack)) throw new Error("This design type does not support audio tracks.");
  if (!Number.isFinite(durationMs) || durationMs <= 0) throw new Error("This track has no usable duration.");
  const audio = await upload({ type: "audio", mimeType: "audio/mp3", url, title,
    durationMs, aiDisclosure: "app_generated" });
  await audio.whenUploaded();
  await addAudioTrack({ ref: audio.ref });
});
