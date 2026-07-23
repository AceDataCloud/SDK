/** Image generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type ImageProvider = 'nano-banana' | 'flux' | 'seedream' | 'hcaptcha' | 'image2text' | 'recaptcha' | (string & {});

const IMAGE_ENDPOINTS: Record<string, string> = {
  hcaptcha: '/captcha/recognition/hcaptcha',
  image2text: '/captcha/recognition/image2text',
  recaptcha: '/captcha/recognition/recaptcha2',
};

const isCaptchaProvider = (provider: string): boolean => provider in IMAGE_ENDPOINTS;

export class Images {
  constructor(private transport: Transport) {}

  async generate(opts: {
    prompt?: string;
    provider?: ImageProvider;
    action?: 'generate' | 'edit';
    model?: string;
    negativePrompt?: string;
    imageUrl?: string;
    imageUrls?: string[];
    image?: string;
    question?: string;
    queries?: unknown;
    websiteKey?: string;
    websiteUrl?: string;
    pageAction?: string;
    aspectRatio?: string;
    resolution?: string;
    callbackUrl?: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const {
      prompt,
      provider = 'nano-banana',
      action,
      model,
      negativePrompt,
      imageUrl,
      imageUrls,
      image,
      question,
      queries,
      websiteKey,
      websiteUrl,
      pageAction,
      aspectRatio,
      resolution,
      callbackUrl,
      wait: shouldWait,
      pollInterval,
      maxWait,
      ...rest
    } = opts;
    const captchaProvider = isCaptchaProvider(provider);
    if (!prompt && !captchaProvider) {
      throw new Error('prompt is required for image generation providers');
    }
    const endpoint = IMAGE_ENDPOINTS[provider] ?? `/${provider}/images`;
    const body: Record<string, unknown> = { ...rest };
    if (prompt !== undefined && !captchaProvider) body.prompt = prompt;
    if (action !== undefined) body.action = action;
    if (model !== undefined) body.model = model;
    if (negativePrompt !== undefined) body.negative_prompt = negativePrompt;
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (imageUrls !== undefined) body.image_urls = imageUrls;
    if (image !== undefined) body.image = image;
    if (question !== undefined) body.question = question;
    if (queries !== undefined) body.queries = queries;
    if (websiteKey !== undefined) body.website_key = websiteKey;
    if (websiteUrl !== undefined) body.website_url = websiteUrl;
    if (pageAction !== undefined) body.page_action = pageAction;
    if (aspectRatio !== undefined) body.aspect_ratio = aspectRatio;
    if (resolution !== undefined) body.resolution = resolution;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;

    const result = await this.transport.request('POST', endpoint, { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, `/${provider}/tasks`, this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}
