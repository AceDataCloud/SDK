/** Task polling abstraction. */

import { Transport } from './transport';

export interface TaskHandleOptions {
  pollInterval?: number;
  maxWait?: number;
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
    const response = (state.response ?? state) as Record<string, unknown>;
    const status = response.status as string;
    return status === 'succeeded' || status === 'failed';
  }

  async wait(opts: TaskHandleOptions = {}): Promise<Record<string, unknown>> {
    const pollInterval = opts.pollInterval ?? 3000;
    const maxWait = opts.maxWait ?? 600_000;
    const start = Date.now();

    while (Date.now() - start < maxWait) {
      const state = await this.get();
      const response = (state.response ?? state) as Record<string, unknown>;
      const status = response.status as string;

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
