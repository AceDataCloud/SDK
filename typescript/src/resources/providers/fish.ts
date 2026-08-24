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
  /** Fish Tts Text */
  text: string;
  /** Fish Tts Reference Id */
  referenceId?: string;
  /** Fish Tts Format */
  format?: "mp3" | "wav" | "pcm";
  /** Fish Tts Sample Rate */
  sampleRate?: number;
  /** Fish Tts Mp3 Bitrate */
  mp3Bitrate?: number;
  /** Fish Tts Latency */
  latency?: "normal" | "balanced";
  /** Fish Tts Chunk Length */
  chunkLength?: number;
  /** Fish Tts Min Chunk Length */
  minChunkLength?: number;
  /** Fish Tts Temperature */
  temperature?: number;
  /** Fish Tts Top P */
  topP?: number;
  /** Fish Tts Repetition Penalty */
  repetitionPenalty?: number;
  /** Fish Tts Max New Tokens */
  maxNewTokens?: number;
  /** Fish Tts Normalize */
  normalize?: boolean;
  /** Fish Tts Prosody */
  prosody?: Record<string, unknown>;
  /** Fish Tts References */
  references?: Array<Record<string, unknown>>;
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

  /** Fish Tts */
  async generate(options: FishGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["text"] = options.text;
    if (options.referenceId !== undefined) body["reference_id"] = options.referenceId;
    if (options.format !== undefined) body["format"] = options.format;
    if (options.sampleRate !== undefined) body["sample_rate"] = options.sampleRate;
    if (options.mp3Bitrate !== undefined) body["mp3_bitrate"] = options.mp3Bitrate;
    if (options.latency !== undefined) body["latency"] = options.latency;
    if (options.chunkLength !== undefined) body["chunk_length"] = options.chunkLength;
    if (options.minChunkLength !== undefined) body["min_chunk_length"] = options.minChunkLength;
    if (options.temperature !== undefined) body["temperature"] = options.temperature;
    if (options.topP !== undefined) body["top_p"] = options.topP;
    if (options.repetitionPenalty !== undefined) body["repetition_penalty"] = options.repetitionPenalty;
    if (options.maxNewTokens !== undefined) body["max_new_tokens"] = options.maxNewTokens;
    if (options.normalize !== undefined) body["normalize"] = options.normalize;
    if (options.prosody !== undefined) body["prosody"] = options.prosody;
    if (options.references !== undefined) body["references"] = options.references;
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
