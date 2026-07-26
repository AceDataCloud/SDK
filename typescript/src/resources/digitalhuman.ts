/** Digital Human generation resources (`/digital-human/*`). */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export class DigitalHuman {
  constructor(private transport: Transport) {}

  async videos(opts: {
    videoUrl?: string;
    imageUrl?: string;
    audioUrl?: string;
    text?: string;
    voiceId?: string;
    engine?: 'latentsync' | 'heygem' | (string & {});
    guidance?: number;
    steps?: number;
    seamFix?: boolean;
    speed?: number;
    resolution?: '720p' | '540p' | (string & {});
    callbackUrl?: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const { videoUrl, imageUrl, audioUrl, text, voiceId, engine, guidance, steps, seamFix, speed, resolution, callbackUrl, wait: shouldWait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (videoUrl !== undefined) body.video_url = videoUrl;
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (audioUrl !== undefined) body.audio_url = audioUrl;
    if (text !== undefined) body.text = text;
    if (voiceId !== undefined) body.voice_id = voiceId;
    if (engine !== undefined) body.engine = engine;
    if (guidance !== undefined) body.guidance = guidance;
    if (steps !== undefined) body.steps = steps;
    if (seamFix !== undefined) body.seam_fix = seamFix;
    if (speed !== undefined) body.speed = speed;
    if (resolution !== undefined) body.resolution = resolution;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    if (opts.async !== undefined) body.async = opts.async;

    const result = await this.transport.request('POST', '/digital-human/videos', { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.video_url && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, '/digital-human/tasks', this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }

  async voices(opts: {
    audioUrl: string;
    lang?: 'zh' | 'en' | (string & {});
    name?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { audioUrl, lang, name, ...rest } = opts;
    const body: Record<string, unknown> = { audio_url: audioUrl, ...rest };
    if (lang !== undefined) body.lang = lang;
    if (name !== undefined) body.name = name;
    if (opts.async !== undefined) body.async = opts.async;
    return this.transport.request('POST', '/digital-human/voices', { json: body });
  }
}
