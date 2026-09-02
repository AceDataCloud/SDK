/**
 * Fish (fish) — generated from the platform OpenAPI spec.
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

export interface FishGenerateOptions {
  /** Text content to be synthesized. Required, must be a non-empty string. */
  text: string;
  /** Top-p nucleus sampling parameter, controls output diversity. */
  topP?: number;
  /** Output audio format, default is `mp3`. */
  format?: "mp3" | "wav" | "pcm";
  /** Delay mode. The upstream rejects null values, and defaults to `normal` when omitted. */
  latency?: "normal" | "balanced";
  /** Rhythm coverage parameters, forwarded as is to upstream (such as speech rate, volume, etc.). */
  prosody?: Record<string, unknown>;
  /** Is the input text subjected to text normalization processing by the upstream? */
  normalize?: boolean;
  /** Inline reference audio samples will be forwarded upstream as is, for zero-shot voice cloning. */
  references?: Array<Record<string, unknown>>;
  /** MP3 bitrate when `format=mp3`. */
  mp3Bitrate?: number;
  /** Output the audio sampling rate (e.g., 16000, 22050, 44100). */
  sampleRate?: number;
  /** Sampling temperature (0.0–1.0). The higher the value, the more diverse the output; the lower the value, the more stable and consistent it is. */
  temperature?: number;
  /** The chunk length passed to the upstream synthesizer. */
  chunkLength?: number;
  /** Voice model ID (single speaker). A string array can also be passed in multi-speaker scenarios. */
  referenceId?: string;
  /** Maximum number of new tokens generated. */
  maxNewTokens?: number;
  /** Minimum block length. */
  minChunkLength?: number;
  /** The repetition penalty coefficient applied during the generation process. */
  repetitionPenalty?: number;
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

/** fish client. */
export class Fish {
  constructor(private transport: Transport) {}

  /** Fish Audio text-to-speech API — convert text into natural speech using a chosen voice model. */
  async generate(options: FishGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["text"] = options.text;
    if (options.topP !== undefined) body["top_p"] = options.topP;
    if (options.format !== undefined) body["format"] = options.format;
    if (options.latency !== undefined) body["latency"] = options.latency;
    if (options.prosody !== undefined) body["prosody"] = options.prosody;
    if (options.normalize !== undefined) body["normalize"] = options.normalize;
    if (options.references !== undefined) body["references"] = options.references;
    if (options.mp3Bitrate !== undefined) body["mp3_bitrate"] = options.mp3Bitrate;
    if (options.sampleRate !== undefined) body["sample_rate"] = options.sampleRate;
    if (options.temperature !== undefined) body["temperature"] = options.temperature;
    if (options.chunkLength !== undefined) body["chunk_length"] = options.chunkLength;
    if (options.referenceId !== undefined) body["reference_id"] = options.referenceId;
    if (options.maxNewTokens !== undefined) body["max_new_tokens"] = options.maxNewTokens;
    if (options.minChunkLength !== undefined) body["min_chunk_length"] = options.minChunkLength;
    if (options.repetitionPenalty !== undefined) body["repetition_penalty"] = options.repetitionPenalty;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "chunkLength", "format", "latency", "maxNewTokens", "maxWait", "minChunkLength", "mp3Bitrate", "normalize", "pollInterval", "prosody", "referenceId", "references", "repetitionPenalty", "sampleRate", "temperature", "text", "topP", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/fish/tts", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/fish/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
