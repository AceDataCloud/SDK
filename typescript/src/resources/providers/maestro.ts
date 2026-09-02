/**
 * Maestro (maestro) — generated from the platform OpenAPI spec.
 *
 * Do not edit by hand: run `python scripts/generate_providers.py`. Parameter
 * names, types, enums and required-ness all come from the live spec.
 */

import { Transport } from '../../runtime/transport';
import { TaskHandle } from '../../runtime/tasks';


function taskId(result: Record<string, unknown>): string {
  if (typeof result?.task_id === 'string') return result.task_id;
  const data = result?.data as Record<string, unknown> | undefined;
  if (data && typeof data.task_id === 'string') return data.task_id;
  return typeof result?.id === 'string' ? result.id : '';
}

export interface MaestroGenerateOptions {
  /** Natural-language brief describing the video to produce (the topic, what to show, tone, audience). The agent decides the script, visuals, voiceover and edit. */
  prompt: string;
  /** Production action. Lite supports generate/edit; Standard adds remix; Pro adds extend. remix/edit/extend require `ref_task_id`. */
  action?: "generate" | "remix" | "edit" | "extend";
  /** Required when `action` is remix / edit / extend: the task_id of the previous video to start from. */
  refTaskId?: string;
  /** Optional reference media (image / video / audio URLs) the agent can use — e.g. a product shot or logo to feature, footage to caption. */
  fileUrls?: string[];
  /** Output languages. Lite supports 1, Standard up to 2, and Pro up to 4. The first is primary; each additional delivered language is billed +6 credits. */
  langs?: string[];
  /** Required output aspect ratio. Lite renders 720p/24fps; Standard and Pro render 1080p/30fps. */
  aspect?: "9:16" | "16:9" | "1:1";
  /** Target video length in seconds. Lite: 5–30; Standard: 5–120; Pro: 5–300. Successful jobs are billed by actual delivered duration, never above the requested duration. */
  duration?: number;
  /** Production route. Lite supports auto/narrated/captions; Standard adds avatar; Pro adds drama. `captions` requires source video in `file_urls`; `avatar` requires a portrait. avatar bills at 1.15× and drama at 1.35×. */
  scenario?: "auto" | "narrated" | "captions" | "avatar" | "drama";
  /** Optional visual-style preset — expressed through typography, palette, motion, image treatment and pacing. Orthogonal to `scenario` (it does NOT change routing). `auto` (default) lets the director pick; every other value adopts a real named look: `cinematic` = dark film-noir (black + blood-red, Oswald); `glass` = Apple / iOS-26 frosted liquid glass; `luxury` = timeless near-black + indigo, huge whitespace; `swiss` = precise grid + electric blue + oversized numerals; `modern` = clean light SaaS; `editorial` = cream magazine + serif; `warm` = intimate cream + amber; `vibrant` = festive folk colour; `neon` = electric neon glow; `mono` = grayscale, type-led; `pastel` = soft candy pastels; `bold` = huge poster type; `industrial` = raw glitch + rust; `futuristic` = particle glow. A freeform string is also accepted as a soft hint. */
  style?: "auto" | "cinematic" | "glass" | "luxury" | "swiss" | "modern" | "editorial" | "warm" | "vibrant" | "neon" | "mono" | "pastel" | "bold" | "industrial" | "futuristic" | "retro";
  /** Optional narration voice — the **timbre** of the voiceover, independent of language. `auto` (default) lets the director pick a fitting voice. Every preset is cross-lingual: the same voice speaks whatever language(s) you set in `langs`, so choose purely by character — `warm-female`, `bright-female`, `anchor-female`, `clean-female`, `calm-male`, `deep-male`, `documentary-male`, `energetic-male`, `storyteller-male`. Advanced: a raw 32-character Fish `reference_id` is also accepted. For `drama` / `avatar` this sets the primary / narrator timbre; distinct characters may still get their own. */
  voice?: "auto" | "warm-female" | "bright-female" | "anchor-female" | "clean-female" | "calm-male" | "deep-male" | "documentary-male" | "energetic-male" | "storyteller-male";
  /** Submit asynchronously and poll. Defaults to true. */
  async?: boolean;
  /** Wait for completion before returning the handle. */
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

/** maestro client. */
export class Maestro {
  constructor(private transport: Transport) {}

  /** Call /maestro/videos. */
  async generate(options: MaestroGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["prompt"] = options.prompt;
    body["action"] = options.action ?? "generate";
    if (options.refTaskId !== undefined) body["ref_task_id"] = options.refTaskId;
    if (options.fileUrls !== undefined) body["file_urls"] = options.fileUrls;
    body["langs"] = options.langs ?? ["zh-cn"];
    body["aspect"] = options.aspect ?? "9:16";
    body["duration"] = options.duration ?? 30;
    body["scenario"] = options.scenario ?? "auto";
    body["style"] = options.style ?? "auto";
    body["voice"] = options.voice ?? "auto";
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "aspect", "async", "callbackUrl", "duration", "fileUrls", "langs", "maxWait", "pollInterval", "prompt", "refTaskId", "scenario", "style", "voice", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/maestro/videos", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/maestro/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
