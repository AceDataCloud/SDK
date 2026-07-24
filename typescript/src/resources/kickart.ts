/** Kickart e-commerce video resources. */

import { Transport } from '../runtime/transport';

export class Kickart {
  constructor(private transport: Transport) {}

  async videos(opts: {
    duration: 15 | 30 | 45 | 60;
    mode?: 'fast' | 'pro';
    type?: 'intro' | 'main';
    templateId?: string;
    productUrl?: string;
    productId?: string;
    userImages?: string[];
    userVideos?: string[];
    aspectRatio?: '9:16' | '16:9' | '3:4' | '4:3' | '1:1';
    language?: 'zh' | 'en' | 'en-us' | 'pt-br' | 'ja' | 'es-mx' | 'id' | 'ms' | 'tl';
    purpose?: string;
    prompt?: string;
    nleSubtitleEnabled?: boolean;
    useSubtitleErasure?: boolean;
    watermark?: boolean;
    callbackUrl?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { duration, mode, type, templateId, productUrl, productId, userImages, userVideos, aspectRatio, language, purpose, prompt, nleSubtitleEnabled, useSubtitleErasure, watermark, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { duration, ...rest };
    if (mode !== undefined) body.mode = mode;
    if (type !== undefined) body.type = type;
    if (templateId !== undefined) body.template_id = templateId;
    if (productUrl !== undefined) body.product_url = productUrl;
    if (productId !== undefined) body.product_id = productId;
    if (userImages !== undefined) body.user_images = userImages;
    if (userVideos !== undefined) body.user_videos = userVideos;
    if (aspectRatio !== undefined) body.aspect_ratio = aspectRatio;
    if (language !== undefined) body.language = language;
    if (purpose !== undefined) body.purpose = purpose;
    if (prompt !== undefined) body.prompt = prompt;
    if (nleSubtitleEnabled !== undefined) body.nle_subtitle_enabled = nleSubtitleEnabled;
    if (useSubtitleErasure !== undefined) body.use_subtitle_erasure = useSubtitleErasure;
    if (watermark !== undefined) body.watermark = watermark;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/kickart/videos', { json: body });
  }

  async viralVideos(opts: {
    refVideo: string;
    language: 'zh' | 'en' | 'en-us' | 'pt-br' | 'ja' | 'es-mx' | 'id' | 'ms' | 'tl';
    mode?: 'pro' | 'advanced';
    templateId?: string;
    productUrl?: string;
    productId?: string;
    productImages?: string[];
    modelImages?: string[];
    aiProductAnalysis?: boolean;
    similarity?: 'high' | 'medium';
    nleSubtitleEnabled?: boolean;
    useSubtitleErasure?: boolean;
    prompt?: string;
    locationImages?: string[];
    watermark?: boolean;
    callbackUrl?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { refVideo, language, mode, templateId, productUrl, productId, productImages, modelImages, aiProductAnalysis, similarity, nleSubtitleEnabled, useSubtitleErasure, prompt, locationImages, watermark, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { ref_video: refVideo, language, ...rest };
    if (mode !== undefined) body.mode = mode;
    if (templateId !== undefined) body.template_id = templateId;
    if (productUrl !== undefined) body.product_url = productUrl;
    if (productId !== undefined) body.product_id = productId;
    if (productImages !== undefined) body.product_images = productImages;
    if (modelImages !== undefined) body.model_images = modelImages;
    if (aiProductAnalysis !== undefined) body.ai_product_analysis = aiProductAnalysis;
    if (similarity !== undefined) body.similarity = similarity;
    if (nleSubtitleEnabled !== undefined) body.nle_subtitle_enabled = nleSubtitleEnabled;
    if (useSubtitleErasure !== undefined) body.use_subtitle_erasure = useSubtitleErasure;
    if (prompt !== undefined) body.prompt = prompt;
    if (locationImages !== undefined) body.location_images = locationImages;
    if (watermark !== undefined) body.watermark = watermark;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/kickart/viral-videos', { json: body });
  }

  async templateVideos(opts: {
    templateId: string;
    resourceList: Array<Record<string, unknown>>;
    resolution?: string;
    watermark?: boolean;
    callbackUrl?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { templateId, resourceList, resolution, watermark, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { template_id: templateId, resource_list: resourceList, ...rest };
    if (resolution !== undefined) body.resolution = resolution;
    if (watermark !== undefined) body.watermark = watermark;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/kickart/template-videos', { json: body });
  }
}
