/** Producer Music Generation resources. */

import { Transport } from '../runtime/transport';

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
  | 'stems';

class ProducerTasks {
  constructor(private transport: Transport) {}

  async retrieve(opts: {
    id?: string;
    [key: string]: unknown;
  } = {}): Promise<Record<string, unknown>> {
    const { id, ...rest } = opts;
    const body: Record<string, unknown> = { action: 'retrieve', ...rest };
    if (id !== undefined) body.id = id;
    return this.transport.request('POST', '/producer/tasks', { json: body });
  }

  async retrieveBatch(opts: {
    ids?: string[];
    [key: string]: unknown;
  } = {}): Promise<Record<string, unknown>> {
    const { ids, ...rest } = opts;
    const body: Record<string, unknown> = { action: 'retrieve_batch', ...rest };
    if (ids !== undefined) body.ids = ids;
    return this.transport.request('POST', '/producer/tasks', { json: body });
  }
}

export class Producer {
  readonly tasks: ProducerTasks;

  constructor(private transport: Transport) {
    this.tasks = new ProducerTasks(transport);
  }

  async generate(opts: {
    lyric: string;
    prompt: string;
    action: ProducerAction;
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
    replaceSectionEnd?: number;
    replaceSectionStart?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { lyric, prompt, action, model, title, custom, audioId, continueAt, callbackUrl, seed, instrumental, soundStrength, lyricsStrength, weirdness, replaceSectionEnd, replaceSectionStart, ...rest } = opts;
    const body: Record<string, unknown> = { lyric, prompt, action, ...rest };
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
    if (replaceSectionEnd !== undefined) body.replace_section_end = replaceSectionEnd;
    if (replaceSectionStart !== undefined) body.replace_section_start = replaceSectionStart;
    return this.transport.request('POST', '/producer/audios', { json: body });
  }

  async upload(opts: {
    audioUrl: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { audioUrl, ...rest } = opts;
    return this.transport.request('POST', '/producer/upload', { json: { audio_url: audioUrl, ...rest } });
  }

  async videos(opts: {
    audioId: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { audioId, ...rest } = opts;
    return this.transport.request('POST', '/producer/videos', { json: { audio_id: audioId, ...rest } });
  }

  async wav(opts: {
    audioId: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { audioId, ...rest } = opts;
    return this.transport.request('POST', '/producer/wav', { json: { audio_id: audioId, ...rest } });
  }

  async lyrics(opts: {
    prompt: Record<string, unknown>;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { prompt, ...rest } = opts;
    return this.transport.request('POST', '/producer/lyrics', { json: { prompt, ...rest } });
  }
}
