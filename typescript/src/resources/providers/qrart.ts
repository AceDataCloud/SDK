/**
 * Qrart (qrart) — generated from the platform OpenAPI spec.
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

export interface QrartGenerateOptions {
  /** Qrart Generate Type */
  type: "link" | "text" | "email" | "phone" | "sms";
  /** Qrart Generate Prompt */
  prompt: string;
  /** Qrart Generate Ecl */
  ecl?: "L" | "M" | "Q" | "H";
  /** Qrart Generate Qrw */
  qrw?: number;
  /** Qrart Generate Seed */
  seed?: number;
  /** Qrart Generate Steps */
  steps?: number;
  /** Qrart Generate Preset */
  preset?: "sunset" | "floral" | "snowflakes" | "feathers" | "raindrops" | "ultra-realism" | "epic-realms" | "intricate-studio" | "symmetric-masterpiece" | "luminous-highway" | "celestial-journey" | "neon-mech" | "ethereal-low-poly" | "golden-vista" | "cinematic-expanse" | "cinematic-warm" | "desolate-wilderness" | "vibrant-palette" | "enigmatic-journey" | "timeless-cinematic" | "regal-galaxy" | "illustrious-canvas" | "expressive-mural" | "serene-haze";
  /** Qrart Generate Rawurl */
  rawurl?: boolean;
  /** Qrart Generate Rotate */
  rotate?: number;
  /** Qrart Generate 2 */
  content?: string;
  /** Qrart Generate Pattern */
  pattern?: "custom" | "s1" | "s2" | "s3" | "rd1" | "rd2" | "rd3" | "d1" | "d2" | "d3" | "r1" | "r2" | "r3" | "c1" | "c2" | "c3" | "sq1" | "sq2" | "sq3";
  /** Qrart Generate Position */
  position?: "center" | "top" | "right" | "bottom" | "left" | "top-left" | "top-right" | "bottom-left" | "bottom-right";
  /** Qrart Generate Sub Marker */
  subMarker?: "square" | "circle" | "box" | "random" | "plus";
  /** Qrart Generate Pixel Style */
  pixelStyle?: "square" | "rounded" | "dot" | "squircle" | "row" | "column";
  /** Qrart Generate Aspect Ratio */
  aspectRatio?: "1:1" | "16:9" | "9:16" | "4:3" | "3:4";
  /** Qrart Generate Marker Shape */
  markerShape?: "square" | "circle" | "plus" | "box" | "octagon" | "random" | "tiny-plus";
  /** Qrart Generate Padding Level */
  paddingLevel?: number;
  /** Qrart Generate Padding Noise */
  paddingNoise?: number;
  /** Qrart Generate Content Image Url */
  contentImageUrl?: string;
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

/** qrart client. */
export class Qrart {
  constructor(private transport: Transport) {}

  /** Generate an QR code */
  async generate(options: QrartGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["type"] = options.type;
    body["prompt"] = options.prompt;
    if (options.ecl !== undefined) body["ecl"] = options.ecl;
    if (options.qrw !== undefined) body["qrw"] = options.qrw;
    if (options.seed !== undefined) body["seed"] = options.seed;
    if (options.steps !== undefined) body["steps"] = options.steps;
    if (options.preset !== undefined) body["preset"] = options.preset;
    if (options.rawurl !== undefined) body["rawurl"] = options.rawurl;
    if (options.rotate !== undefined) body["rotate"] = options.rotate;
    if (options.content !== undefined) body["content"] = options.content;
    if (options.pattern !== undefined) body["pattern"] = options.pattern;
    if (options.position !== undefined) body["position"] = options.position;
    if (options.subMarker !== undefined) body["sub_marker"] = options.subMarker;
    if (options.pixelStyle !== undefined) body["pixel_style"] = options.pixelStyle;
    if (options.aspectRatio !== undefined) body["aspect_ratio"] = options.aspectRatio;
    if (options.markerShape !== undefined) body["marker_shape"] = options.markerShape;
    if (options.paddingLevel !== undefined) body["padding_level"] = options.paddingLevel;
    if (options.paddingNoise !== undefined) body["padding_noise"] = options.paddingNoise;
    if (options.contentImageUrl !== undefined) body["content_image_url"] = options.contentImageUrl;
    for (const [key, value] of Object.entries(options)) {
      if (!["aspectRatio", "async", "callbackUrl", "content", "contentImageUrl", "ecl", "markerShape", "maxWait", "paddingLevel", "paddingNoise", "pattern", "pixelStyle", "pollInterval", "position", "preset", "prompt", "qrw", "rawurl", "rotate", "seed", "steps", "subMarker", "type", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/qrart/generate", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/qrart/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
