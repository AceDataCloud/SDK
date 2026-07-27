/**
 * Maestro (maestro) — generated from the platform OpenAPI spec.
 *
 * Do not edit by hand: run `python scripts/generate_providers.py`. Parameter
 * names, types, enums and required-ness all come from the live spec.
 */

import { Transport } from '../../runtime/transport';


export interface MaestroGenerateOptions {
  /** Natural-language brief describing the video to produce (the topic, what to show, tone, audience). The agent decides the script, visuals, voiceover and edit. */
  prompt: string;
  /** Output languages, e.g. ["zh-cn", "en"]. The first is the primary language; each additional one reuses the visuals with a localized voiceover + render and is billed +6 credits. */
  langs?: string[];
  /** Optional visual-style preset — expressed through typography, palette, motion, image treatment and pacing. Orthogonal to `scenario` (it does NOT change routing). `auto` (default) lets the director pick; every other value adopts a real named look: `cinematic` = dark film-noir (black + blood-red, Oswald); `glass` = Apple / iOS-26 frosted liquid glass; `luxury` = timeless near-black + indigo, huge whitespace; `swiss` = precise grid + electric blue + oversized numerals; `modern` = clean light SaaS; `editorial` = cream magazine + serif; `warm` = intimate cream + amber; `vibrant` = festive folk colour; `neon` = electric neon glow; `mono` = grayscale, type-led; `pastel` = soft candy pastels; `bold` = huge poster type; `industrial` = raw glitch + rust; `futuristic` = particle glow. A freeform string is also accepted as a soft hint. */
  style?: "auto" | "cinematic" | "glass" | "luxury" | "swiss" | "modern" | "editorial" | "warm" | "vibrant" | "neon" | "mono" | "pastel" | "bold" | "industrial" | "futuristic" | "retro";
  /** Optional narration voice — the **timbre** of the voiceover, independent of language. `auto` (default) lets the director pick a fitting voice. Every preset is cross-lingual: the same voice speaks whatever language(s) you set in `langs`, so choose purely by character — `warm-female`, `bright-female`, `anchor-female`, `clean-female`, `calm-male`, `deep-male`, `documentary-male`, `energetic-male`, `storyteller-male`. Advanced: a raw 32-character Fish `reference_id` is also accepted. For `drama` / `avatar` this sets the primary / narrator timbre; distinct characters may still get their own. */
  voice?: "auto" | "warm-female" | "bright-female" | "anchor-female" | "clean-female" | "calm-male" | "deep-male" | "documentary-male" | "energetic-male" | "storyteller-male";
  /** generate = a new video. remix / edit / extend = iterate on a previous video (require `ref_task_id`). */
  action?: "generate" | "remix" | "edit" | "extend";
  /** Output aspect ratio (hint — the agent may follow the prompt). */
  aspect?: "9:16" | "16:9" | "1:1";
  /** Production tier, a multiplier on the duration-based price. `draft` = a fast rough cut for previewing the idea (~0.5× the standard credits); `standard` = balanced (default, 1×); `premium` = richer, more detailed and polished (~2× the standard credits). Affects turnaround, detail and price. */
  quality?: "draft" | "standard" | "premium";
  /** Target video length in seconds (1–600, i.e. up to 10 minutes). Billed by duration: credits ≈ 0.85 × duration × quality multiplier × scenario multiplier, so a longer or video-native workflow costs proportionally more. */
  duration?: number;
  /** How to route the video — a hint; the AI director still decides the final structure. `auto` (default) = the director chooses from your brief. `narrated` = multi-scene narrated video with real photos + voiceover + data cards (people / brands / explainers / history / products). `drama` = acted short drama with characters + dialogue (短剧) and bills at 1.35×. `avatar` = talking-head / digital human (needs a portrait image via `file_urls`, or a chosen digital human) and bills at 1.15×. `motion` = abstract kinetic-typography / data / logo motion graphic. `slideshow` = presentation deck / pitch. Legacy values `general` / `explainer` / `product` / `website` / `changelog` / `captions` are still accepted (mapped to `auto`), and `slides` maps to `slideshow`. */
  scenario?: "auto" | "narrated" | "drama" | "avatar" | "motion" | "slideshow";
  /** Optional reference media (image / video / audio URLs) the agent can use — e.g. a product shot or logo to feature, footage to caption. */
  fileUrls?: string[];
  /** Required when `action` is remix / edit / extend: the task_id of the previous video to start from. */
  refTaskId?: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface MaestroEstimatesOptions {
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

/** maestro client. */
export class Maestro {
  constructor(private transport: Transport) {}

  /** Maestro Video Generation API */
  async generate(options: MaestroGenerateOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["prompt"] = options.prompt;
    body["langs"] = options.langs ?? ["zh-cn"];
    body["style"] = options.style ?? "auto";
    body["voice"] = options.voice ?? "auto";
    body["action"] = options.action ?? "generate";
    body["aspect"] = options.aspect ?? "9:16";
    body["quality"] = options.quality ?? "standard";
    body["duration"] = options.duration ?? 30;
    body["scenario"] = options.scenario ?? "auto";
    if (options.fileUrls !== undefined) body["file_urls"] = options.fileUrls;
    if (options.refTaskId !== undefined) body["ref_task_id"] = options.refTaskId;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "aspect", "async", "callbackUrl", "duration", "fileUrls", "langs", "maxWait", "pollInterval", "prompt", "quality", "refTaskId", "scenario", "style", "voice", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/maestro/videos", { json: body })) as Record<string, unknown>;
  }

  /** Call /maestro/estimates. */
  async estimates(options: MaestroEstimatesOptions = {}): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "maxWait", "pollInterval", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/maestro/estimates", { json: body })) as Record<string, unknown>;
  }

}
