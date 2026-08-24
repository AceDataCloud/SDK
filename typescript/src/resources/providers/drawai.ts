/**
 * Drawai (drawai) — generated from the platform OpenAPI spec.
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

export interface DrawaiGenerateOptions {
  /** Headshots Generate Mode */
  mode: "fast" | "relax";
  /** Headshots Generate Template */
  template: "male_portrait" | "male_portrait2" | "kindergarten" | "logo_tshirt" | "wedding" | "business_photo" | "bob_suit" | "female_portrait";
  /** Headshots Generate Image Urls */
  imageUrls: string[];
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

/** drawai client. */
export class Drawai {
  constructor(private transport: Transport) {}

  /** Generate */
  async generate(options: DrawaiGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["mode"] = options.mode;
    body["template"] = options.template;
    body["image_urls"] = options.imageUrls;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "imageUrls", "maxWait", "mode", "pollInterval", "template", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/headshots/generate", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/headshots/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
