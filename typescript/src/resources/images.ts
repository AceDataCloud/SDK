/** Image generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type ImageProvider = 'nano-banana' | 'flux' | 'seedream' | (string & {});

export class Images {
  constructor(private transport: Transport) {}

  async generate(opts: {
    prompt: string;
    provider?: ImageProvider;
    action?: 'generate' | 'edit';
    model?: string;
    negativePrompt?: string;
    image?: unknown[];
    imageUrl?: string;
    imageUrls?: string[];
    aspectRatio?: string;
    resolution?: string;
    size?: '1K' | '2K' | '3K' | '4K' | 'adaptive' | (string & {});
    seed?: number;
    guidanceScale?: number;
    responseFormat?: string;
    watermark?: boolean;
    outputFormat?: 'jpeg' | 'png' | (string & {});
    stream?: boolean;
    sequentialImageGeneration?: 'auto' | 'disabled' | (string & {});
    sequentialImageGenerationOptions?: Record<string, unknown>;
    tools?: unknown[];
    optimizePromptOptions?: Record<string, unknown>;
    callbackUrl?: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const { prompt, provider = 'nano-banana', action, model, negativePrompt, image, imageUrl, imageUrls, aspectRatio, resolution, size, seed, guidanceScale, responseFormat, watermark, outputFormat, stream, sequentialImageGeneration, sequentialImageGenerationOptions, tools, optimizePromptOptions, callbackUrl, wait: shouldWait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = { prompt, ...rest };
    if (action !== undefined) body.action = action;
    if (model !== undefined) body.model = model;
    if (negativePrompt !== undefined) body.negative_prompt = negativePrompt;
    if (image !== undefined) body.image = image;
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (imageUrls !== undefined) body.image_urls = imageUrls;
    if (aspectRatio !== undefined) body.aspect_ratio = aspectRatio;
    if (resolution !== undefined) body.resolution = resolution;
    if (size !== undefined) body.size = size;
    if (seed !== undefined) body.seed = seed;
    if (guidanceScale !== undefined) body.guidance_scale = guidanceScale;
    if (responseFormat !== undefined) body.response_format = responseFormat;
    if (watermark !== undefined) body.watermark = watermark;
    if (outputFormat !== undefined) body.output_format = outputFormat;
    if (stream !== undefined) body.stream = stream;
    if (sequentialImageGeneration !== undefined) body.sequential_image_generation = sequentialImageGeneration;
    if (sequentialImageGenerationOptions !== undefined) body.sequential_image_generation_options = sequentialImageGenerationOptions;
    if (tools !== undefined) body.tools = tools;
    if (optimizePromptOptions !== undefined) body.optimize_prompt_options = optimizePromptOptions;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;

    const endpoint = `/${provider}/images`;
    const result = await this.transport.request('POST', endpoint, { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, `/${provider}/tasks`, this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}
