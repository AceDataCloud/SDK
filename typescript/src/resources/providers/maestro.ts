import { Transport } from '../../runtime/transport';
import { TaskHandle } from '../../runtime/tasks';

export interface MaestroGenerateOptions {
  prompt: string;
  action?: "generate" | "remix" | "edit" | "extend";
  refTaskId?: string;
  fileUrls?: string[];
  langs?: string[];
  aspect?: "9:16" | "16:9" | "1:1";
  duration?: number;
  quality?: "lite" | "standard" | "pro";
  scenario?: "auto" | "narrated" | "captions" | "avatar" | "drama";
  style?: "auto" | "cinematic" | "glass" | "luxury" | "swiss" | "modern" | "editorial" | "warm" | "vibrant" | "neon" | "mono" | "pastel" | "bold" | "industrial" | "futuristic" | "retro";
  voice?: "auto" | "warm-female" | "bright-female" | "anchor-female" | "clean-female" | "calm-male" | "deep-male" | "documentary-male" | "energetic-male" | "storyteller-male";
  async?: boolean;
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  callbackUrl?: string;
}

function taskId(result: Record<string, unknown>): string {
  if (typeof result.task_id === 'string') return result.task_id;
  const data = result.data as Record<string, unknown> | undefined;
  if (data && typeof data.task_id === 'string') return data.task_id;
  return typeof result.id === 'string' ? result.id : '';
}

function bodyFor(options: MaestroGenerateOptions): Record<string, unknown> {
  const action = options.action ?? 'generate';
  const quality = options.quality ?? 'standard';
  const scenario = options.scenario ?? 'auto';
  const duration = options.duration ?? 30;
  const langs = options.langs ?? ['zh-cn'];
  if (!['generate', 'remix', 'edit', 'extend'].includes(action)) throw new Error('action must be generate, remix, edit, or extend');
  if (!['lite', 'standard', 'pro'].includes(quality)) throw new Error('quality must be lite, standard, or pro');
  if (action !== 'generate' && !options.refTaskId) throw new Error('refTaskId is required when action is remix, edit, or extend');
  if (!langs.length || langs.length > 4) throw new Error('langs must contain between 1 and 4 languages');
  if (!Number.isInteger(duration) || duration < 5 || duration > 300) throw new Error('duration must be an integer between 5 and 300');
  if (quality === 'lite' && (duration > 30 || !['generate', 'edit'].includes(action))) throw new Error('lite supports generate/edit actions and durations up to 30 seconds');
  if (quality === 'standard' && (duration > 120 || action === 'extend')) throw new Error('standard supports generate/remix/edit actions and durations up to 120 seconds');
  const scenarios = { lite: ['auto', 'narrated', 'captions'], standard: ['auto', 'narrated', 'captions', 'avatar'], pro: ['auto', 'narrated', 'captions', 'avatar', 'drama'] };
  if (!['auto', 'narrated', 'captions', 'avatar', 'drama'].includes(scenario)) throw new Error('scenario must be auto, narrated, captions, avatar, or drama');
  if (!scenarios[quality].includes(scenario)) throw new Error(`${scenario} scenario requires a higher quality tier`);
  if (['captions', 'avatar'].includes(scenario) && !options.fileUrls?.length) throw new Error(`fileUrls is required for the ${scenario} scenario`);
  return {
    prompt: options.prompt, action, langs, aspect: options.aspect ?? '9:16', duration, quality, scenario,
    style: options.style ?? 'auto', voice: options.voice ?? 'auto', async: options.async ?? true,
    ...(options.refTaskId !== undefined && { ref_task_id: options.refTaskId }),
    ...(options.fileUrls !== undefined && { file_urls: options.fileUrls }),
    ...(options.callbackUrl !== undefined && { callback_url: options.callbackUrl }),
  };
}

export class Maestro {
  constructor(private transport: Transport) {}

  async generate(options: MaestroGenerateOptions): Promise<TaskHandle> {
    const result = await this.transport.request('POST', '/maestro/videos', { json: bodyFor(options) }) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/maestro/tasks', this.transport, result);
    if (options.wait) await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    return handle;
  }
}
