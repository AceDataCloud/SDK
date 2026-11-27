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

const sample = {
  title: "Studio chimes",
  url: "https://cdn.jsdelivr.net/gh/AceDataCloud/SDK@a3f1eca5aa18b269847e71bf4b8f1e073a0a17a9/examples/creative-audio/canva/studio-chimes.mp3",
  durationMs: 6000,
};

async function insertTrack({ title, url, durationMs }, aiDisclosure = "app_generated", mimeType = "audio/mp3") {
  if (!features.isSupported(addAudioTrack)) throw new Error("unsupported");
  if (!Number.isFinite(durationMs) || durationMs <= 0) throw new Error("durationMissing");
  const audio = await upload({ type: "audio", mimeType, url, title,
    durationMs, aiDisclosure });
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
  const [adding, setAdding] = React.useState(false);
  const [feedback, setFeedback] = React.useState(null);
  const label = (id) => intl.formatMessage({ id, ...messages[id] });
  async function addSample() {
    setAdding(true);
    try {
      await insertTrack(sample, "none", "audio/mpeg");
      setFeedback("inserted");
    } catch (error) {
      setFeedback(error.message === "unsupported" ? "unsupported" : "insertFailed");
    } finally {
      setAdding(false);
    }
  }
  return React.createElement("main", null,
    React.createElement("div", { ref: element }),
    React.createElement("section", { "aria-label": label("sampleTitle") },
      React.createElement("strong", null, label("sampleTitle")),
      React.createElement("audio", { controls: true, preload: "none", src: sample.url }),
      React.createElement("button", { type: "button", onClick: addSample, disabled: adding }, label("addSample")),
      React.createElement("p", { "aria-live": "polite" }, feedback ? label(feedback) : "")));
}

prepareDesignEditor({
  async render() {
    const target = document.getElementById("root");
    createRoot(target).render(React.createElement(AppI18nProvider, null, React.createElement(Panel)));
  },
});
