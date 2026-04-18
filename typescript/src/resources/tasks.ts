/** Cross-service task retrieval. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

const SERVICE_TASK_ENDPOINTS: Record<string, string> = {
  suno: '/suno/tasks',
  producer: '/producer/tasks',
  fish: '/fish/tasks',
  'nano-banana': '/nano-banana/tasks',
  seedream: '/seedream/tasks',
  seedance: '/seedance/tasks',
  sora: '/sora/tasks',
  midjourney: '/midjourney/tasks',
  luma: '/luma/tasks',
  veo: '/veo/tasks',
  flux: '/flux/tasks',
  kling: '/kling/tasks',
  hailuo: '/hailuo/tasks',
  wan: '/wan/tasks',
  pika: '/pika/tasks',
  pixverse: '/pixverse/tasks',
};

export class Tasks {
  constructor(private transport: Transport) {}

  async get(taskId: string, opts: { service?: string } = {}): Promise<Record<string, unknown>> {
    const service = opts.service ?? 'suno';
    const endpoint = SERVICE_TASK_ENDPOINTS[service] ?? `/${service}/tasks`;
    return this.transport.request('POST', endpoint, {
      json: { id: taskId, action: 'retrieve' },
    });
  }

  async wait(
    taskId: string,
    opts: { service?: string; pollInterval?: number; maxWait?: number } = {}
  ): Promise<Record<string, unknown>> {
    const service = opts.service ?? 'suno';
    const endpoint = SERVICE_TASK_ENDPOINTS[service] ?? `/${service}/tasks`;
    const handle = new TaskHandle(taskId, endpoint, this.transport);
    return handle.wait({ pollInterval: opts.pollInterval, maxWait: opts.maxWait });
  }
}
