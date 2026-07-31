/**
 * QRart (qrart) — generated from the platform OpenAPI spec.
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

export type QRartType = 'link' | 'text' | 'email' | 'phone' | 'sms';
export type QRartEcl = 'L' | 'M' | 'Q' | 'H';
export type QRartRotate = 0 | 90 | 180 | 270;
export type QRartPaddingLevel = 0 | 5 | 10 | 15 | 20;
export type QRartPaddingNoise = 0 | 0.25 | 0.5 | 0.75 | 1;
export type QRartAspectRatio = '1:1' | '16:9' | '9:16' | '4:3' | '3:4';
export type QRartPixelStyle = 'square' | 'rounded' | 'dot' | 'squircle' | 'row' | 'column';
export type QRartPosition = 'center' | 'top' | 'right' | 'bottom' | 'left' | 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
export type QRartMarkerShape = 'square' | 'circle' | 'plus' | 'box' | 'octagon' | 'random' | 'tiny-plus';
export type QRartSubMarker = 'square' | 'circle' | 'box' | 'random' | 'plus';

export interface QRartGenerateOptions {
  prompt: string;
  type: QRartType;
  content?: string;
  contentImageUrl?: string;
  ecl?: QRartEcl;
  qrw?: number;
  seed?: number;
  steps?: number;
  aspectRatio?: QRartAspectRatio;
  preset?: string;
  pattern?: string;
  pixelStyle?: QRartPixelStyle;
  position?: QRartPosition;
  markerShape?: QRartMarkerShape;
  subMarker?: QRartSubMarker;
  paddingLevel?: QRartPaddingLevel;
  paddingNoise?: QRartPaddingNoise;
  rotate?: QRartRotate;
  rawurl?: boolean;
  async?: boolean;
  callbackUrl?: string;
}

export class QRart {
  constructor(private transport: Transport) {}

  async generate(
    opts: QRartGenerateOptions & { wait?: boolean; pollInterval?: number; maxWait?: number },
  ): Promise<TaskHandle> {
    const body: Record<string, unknown> = { prompt: opts.prompt, type: opts.type };
    if (opts.content !== undefined) body.content = opts.content;
    if (opts.contentImageUrl !== undefined) body.content_image_url = opts.contentImageUrl;
    if (opts.ecl !== undefined) body.ecl = opts.ecl;
    if (opts.qrw !== undefined) body.qrw = opts.qrw;
    if (opts.seed !== undefined) body.seed = opts.seed;
    if (opts.steps !== undefined) body.steps = opts.steps;
    if (opts.aspectRatio !== undefined) body.aspect_ratio = opts.aspectRatio;
    if (opts.preset !== undefined) body.preset = opts.preset;
    if (opts.pattern !== undefined) body.pattern = opts.pattern;
    if (opts.pixelStyle !== undefined) body.pixel_style = opts.pixelStyle;
    if (opts.position !== undefined) body.position = opts.position;
    if (opts.markerShape !== undefined) body.marker_shape = opts.markerShape;
    if (opts.subMarker !== undefined) body.sub_marker = opts.subMarker;
    if (opts.paddingLevel !== undefined) body.padding_level = opts.paddingLevel;
    if (opts.paddingNoise !== undefined) body.padding_noise = opts.paddingNoise;
    if (opts.rotate !== undefined) body.rotate = opts.rotate;
    if (opts.rawurl !== undefined) body.rawurl = opts.rawurl;
    if (opts.callbackUrl !== undefined) body.callback_url = opts.callbackUrl;
    body.async = opts.async ?? true;
    const result = (await this.transport.request('POST', '/qrart/generate', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/qrart/tasks', this.transport, result);
    if (opts.wait) {
      await handle.wait({ pollInterval: opts.pollInterval, maxWait: opts.maxWait });
    }
    return handle;
  }
}
