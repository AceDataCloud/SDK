/** Producer music generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type ProducerModel =
  | 'FUZZ-2.0 Pro'
  | 'FUZZ-2.0'
  | 'FUZZ-2.0 Raw'
  | 'FUZZ-1.1 Pro'
  | 'FUZZ-1.0 Pro'
  | 'FUZZ-1.0'
  | 'FUZZ-1.1'
  | 'FUZZ-0.8'
  | (string & {});

export type ProducerAction =
  | 'generate'
  | 'cover'
  | 'extend'
  | 'variation'
  | 'swap_vocals'
  | 'swap_instrumentals'
  | 'replace_section'
  | 'stems'
  | (string & {});

export class Producer {
  constructor(private transport: Transport) {}

  async generate(opts: {
    action: ProducerAction;
    lyric: string;
    prompt: string;
    model?: ProducerModel;
    title?: string;
    custom?: boolean;
    audioId?: string;
    continueAt?: number;
    callbackUrl?: string;
    async?: boolean;
    seed?: string;
    instrumental?: boolean;
    soundStrength?: number;
    lyricsStrength?: number;
    weirdness?: number;
    replaceSectionStart?: number;
    replaceSectionEnd?: number;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const {
      action, lyric, prompt, model, title, custom, audioId, continueAt,
      callbackUrl, seed, instrumental, soundStrength, lyricsStrength,
      weirdness, replaceSectionStart, replaceSectionEnd,
      wait: shouldWait, pollInterval, maxWait, ...rest
    } = opts;
    const body: Record<string, unknown> = { action, lyric, prompt, ...rest };
    if (model !== undefined) body.model = model;
    if (title !== undefined) body.title = title;
    if (custom !== undefined) body.custom = custom;
    if (audioId !== undefined) body.audio_id = audioId;
    if (continueAt !== undefined) body.continue_at = continueAt;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    if (seed !== undefined) body.seed = seed;
    if (instrumental !== undefined) body.instrumental = instrumental;
    if (soundStrength !== undefined) body.sound_strength = soundStrength;
    if (lyricsStrength !== undefined) body.lyrics_strength = lyricsStrength;
    if (weirdness !== undefined) body.weirdness = weirdness;
    if (replaceSectionStart !== undefined) body.replace_section_start = replaceSectionStart;
    if (replaceSectionEnd !== undefined) body.replace_section_end = replaceSectionEnd;
    const result = await this.transport.request('POST', '/producer/audios', { json: body });
    const taskId = result.task_id as string | undefined;
    if (!taskId || (result.data && !shouldWait)) return result;
    const handle = new TaskHandle(taskId, '/producer/tasks', this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }

  async upload(opts: {
    audioUrl: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { audioUrl, ...rest } = opts;
    const body: Record<string, unknown> = { audio_url: audioUrl, ...rest };
    return this.transport.request('POST', '/producer/upload', { json: body });
  }

  async videos(opts: {
    audioId: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { audioId, ...rest } = opts;
    const body: Record<string, unknown> = { audio_id: audioId, ...rest };
    return this.transport.request('POST', '/producer/videos', { json: body });
  }

  async wav(opts: {
    audioId: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { audioId, ...rest } = opts;
    const body: Record<string, unknown> = { audio_id: audioId, ...rest };
    return this.transport.request('POST', '/producer/wav', { json: body });
  }

  async lyrics(opts: {
    prompt: Record<string, unknown> | string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { prompt, ...rest } = opts;
    const body: Record<string, unknown> = { prompt, ...rest };
    return this.transport.request('POST', '/producer/lyrics', { json: body });
  }
}
