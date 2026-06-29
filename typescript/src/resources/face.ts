/** Face transformation resources (`/face/*`). */

import { Transport } from '../runtime/transport';

export class Face {
  constructor(private transport: Transport) {}

  private call(action: string, body: Record<string, unknown>): Promise<Record<string, unknown>> {
    return this.transport.request('POST', `/face/${action}`, { json: body });
  }

  analyze(opts: { imageUrl: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { imageUrl, ...rest } = opts;
    return this.call('analyze', { image_url: imageUrl, ...rest });
  }

  beautify(opts: { imageUrl: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { imageUrl, ...rest } = opts;
    return this.call('beautify', { image_url: imageUrl, ...rest });
  }

  changeAge(opts: { imageUrl: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { imageUrl, ...rest } = opts;
    return this.call('change-age', { image_url: imageUrl, ...rest });
  }

  changeGender(opts: { imageUrl: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { imageUrl, ...rest } = opts;
    return this.call('change-gender', { image_url: imageUrl, ...rest });
  }

  detectLive(opts: { imageUrl: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { imageUrl, ...rest } = opts;
    return this.call('detect-live', { image_url: imageUrl, ...rest });
  }

  swap(opts: { sourceImageUrl: string; targetImageUrl: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { sourceImageUrl, targetImageUrl, ...rest } = opts;
    return this.call('swap', { source_image_url: sourceImageUrl, target_image_url: targetImageUrl, ...rest });
  }

  cartoon(opts: { imageUrl: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { imageUrl, ...rest } = opts;
    return this.call('cartoon', { image_url: imageUrl, ...rest });
  }
}
