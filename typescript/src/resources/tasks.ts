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
  luma: '/luma/tasks',
  veo: '/veo/tasks',
  flux: '/flux/tasks',
  kling: '/kling/tasks',
  hailuo: '/hailuo/tasks',
  wan: '/wan/tasks',
  pika: '/pika/tasks',
  pixverse: '/pixverse/tasks',
  webextrator: '/webextrator/tasks',
  captcha: '/captcha/tasks',
};

export class Tasks {
  constructor(private transport: Transport) {}

  async get(taskId: string, opts: { service?: string } = {}): Promise<Record<string, unknown>> {
    const service = opts.service ?? 'suno';
    const endpoint = SERVICE_TASK_ENDPOINTS[service] ?? `/${service}/tasks`;
    if (service === 'captcha') {
      return this.transport.request('POST', endpoint, { json: { task_id: taskId } });
    }
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
    if (service === 'captcha') {
      const handle = new TaskHandle(taskId, endpoint, this.transport, undefined, {
        pollIdField: 'task_id',
        pollAction: null,
      });
      return handle.wait({ pollInterval: opts.pollInterval, maxWait: opts.maxWait });
    }
    const handle = new TaskHandle(taskId, endpoint, this.transport);
    return handle.wait({ pollInterval: opts.pollInterval, maxWait: opts.maxWait });
  }
}
