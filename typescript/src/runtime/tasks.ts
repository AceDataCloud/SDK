/** Task polling abstraction. */

import { Transport } from './transport';

export interface TaskHandleOptions {
  pollInterval?: number;
  maxWait?: number;
}

function taskStatus(state: Record<string, unknown>): 'succeeded' | 'failed' | '' {
  const response = (state.response ?? state) as Record<string, unknown>;
  if (response.status === 'succeeded' || response.status === 'failed') return response.status;
  if (response.status !== undefined && response.status !== null) return '';
  const finished =
    (response.finished_at !== undefined && response.finished_at !== null) ||
    (state.finished_at !== undefined && state.finished_at !== null);
  if (!finished) return '';
  if (response.success === true) return 'succeeded';
  if (response.success === false) return 'failed';
  return '';
}

export class TaskHandle {
  readonly id: string;
  private pollEndpoint: string;
  private transport: Transport;
  private _result: Record<string, unknown> | null = null;

  constructor(taskId: string, pollEndpoint: string, transport: Transport) {
    this.id = taskId;
    this.pollEndpoint = pollEndpoint;
    this.transport = transport;
  }

  async get(): Promise<Record<string, unknown>> {
    return this.transport.request('POST', this.pollEndpoint, {
      json: { id: this.id, action: 'retrieve' },
    });
  }

  async isCompleted(): Promise<boolean> {
    const state = await this.get();
    const status = taskStatus(state);
    return status === 'succeeded' || status === 'failed';
  }

  async wait(opts: TaskHandleOptions = {}): Promise<Record<string, unknown>> {
    const pollInterval = opts.pollInterval ?? 3000;
    const maxWait = opts.maxWait ?? 600_000;
    const start = Date.now();

    while (Date.now() - start < maxWait) {
      const state = await this.get();
      const status = taskStatus(state);

      if (status === 'succeeded' || status === 'failed') {
        this._result = state;
        return state;
      }
      await new Promise((resolve) => setTimeout(resolve, pollInterval));
    }
    throw new Error(`Task ${this.id} did not complete within ${maxWait}ms`);
  }

  get result(): Record<string, unknown> | null {
    return this._result;
  }
}
