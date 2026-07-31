/**
 * QrArt (qrart) — generated from the platform OpenAPI spec.
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
  /** QR code content type. */
  type: 'link' | 'text' | 'email' | 'phone' | 'sms';
  /** Art style prompt. */
  prompt: string;
  /** Error correction level. */
  ecl?: 'L' | 'M' | 'Q' | 'H';
  /** QR code weight. */
  qrw?: number;
  /** Random seed. */
  seed?: number;
  /** Number of diffusion steps. */
  steps?: number;
  /** Style preset. */
  preset?: 'sunset' | 'floral' | 'snowflakes' | 'feathers' | 'raindrops';
  /** Whether to use raw URL. */
  rawurl?: boolean;
  /** Rotation angle. */
  rotate?: 0 | 90 | 180 | 270;
  /** QR code content. */
  content?: string;
  /** Pattern style. */
  pattern?: 'custom' | 's1' | 's2' | 's3' | 'rd1';
  /** Logo position. */
  position?: 'center' | 'top' | 'right' | 'bottom' | 'left';
  /** Sub-marker style. */
  subMarker?: 'square' | 'circle' | 'box' | 'random' | 'plus';
  /** Pixel style. */
  pixelStyle?: 'square' | 'rounded' | 'dot' | 'squircle' | 'row';
  /** Aspect ratio. */
  aspectRatio?: '1:1' | '16:9' | '9:16' | '4:3' | '3:4';
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

  /** Art QR Code generation API — generates a styled QR code image. */
  async generate(options: QrartGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body['type'] = options.type;
    body['prompt'] = options.prompt;
    if (options.ecl !== undefined) body['ecl'] = options.ecl;
    if (options.qrw !== undefined) body['qrw'] = options.qrw;
    if (options.seed !== undefined) body['seed'] = options.seed;
    if (options.steps !== undefined) body['steps'] = options.steps;
    if (options.preset !== undefined) body['preset'] = options.preset;
    if (options.rawurl !== undefined) body['rawurl'] = options.rawurl;
    if (options.rotate !== undefined) body['rotate'] = options.rotate;
    if (options.content !== undefined) body['content'] = options.content;
    if (options.pattern !== undefined) body['pattern'] = options.pattern;
    if (options.position !== undefined) body['position'] = options.position;
    if (options.subMarker !== undefined) body['sub_marker'] = options.subMarker;
    if (options.pixelStyle !== undefined) body['pixel_style'] = options.pixelStyle;
    if (options.aspectRatio !== undefined) body['aspect_ratio'] = options.aspectRatio;
    for (const [key, value] of Object.entries(options)) {
      if (!['aspectRatio', 'async', 'callbackUrl', 'content', 'ecl', 'maxWait', 'pattern', 'pixelStyle', 'pollInterval', 'position', 'preset', 'prompt', 'qrw', 'rawurl', 'rotate', 'seed', 'steps', 'subMarker', 'type', 'wait'].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', '/qrart/generate', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/qrart/tasks', this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }
}
