import { upload } from "@canva/asset";
import { addAudioTrack } from "@canva/design";
import { features, requestOpenExternalUrl } from "@canva/platform";
import { prepareDesignEditor } from "@canva/intents/design";
import { AppI18nProvider } from "@canva/app-i18n-kit";
import React, { useEffect, useRef } from "react";
import { createRoot } from "react-dom/client";
import { useIntl } from "react-intl";
import messages from "../shared/messages.json";
import { mountPanel } from "../shared/panel.js";
import "../shared/panel.css";

async function insertTrack({ title, url, durationMs }) {
  if (!features.isSupported(addAudioTrack)) throw new Error("unsupported");
  if (!Number.isFinite(durationMs) || durationMs <= 0) throw new Error("durationMissing");
  const audio = await upload({ type: "audio", mimeType: "audio/mp3", url, title,
    durationMs, aiDisclosure: "app_generated" });
  await audio.whenUploaded();
  await addAudioTrack({ ref: audio.ref });
}

function Panel() {
  const intl = useIntl();
  const element = useRef(null);
  useEffect(() => {
    mountPanel(element.current, insertTrack,
      (id, values) => intl.formatMessage({ id, ...messages[id] }, values),
      (url) => requestOpenExternalUrl({ url }));
  }, [intl]);
  return React.createElement("main", { ref: element });
}

prepareDesignEditor({
  async render() {
    const target = document.getElementById("root");
    createRoot(target).render(React.createElement(AppI18nProvider, null, React.createElement(Panel)));
  },
});
