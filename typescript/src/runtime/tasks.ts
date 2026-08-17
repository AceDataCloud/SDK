/**
 * Task polling for long-running operations.
 *
 * A generation call always returns a handle, never sometimes a handle and
 * sometimes a plain object — the caller decides whether to wait. When the server
 * answers synchronously (some endpoints do for fast or cached results) the
 * handle is born already complete, so `wait()` returns immediately rather than
 * polling for something that has already arrived.
 *
 * Kept behaviourally identical to the Python and Go implementations; a
 * divergence here is a cross-language bug that only shows up in production.
 */

import { Transport } from './transport';

export interface TaskHandleOptions {
  pollInterval?: number;
  maxWait?: number;
}

const DONE = new Set(['succeed', 'succeeded', 'success', 'completed', 'complete', 'finished']);
const FAILED = new Set(['failed', 'failure', 'error', 'cancelled', 'canceled', 'rejected']);

function statusWords(node: unknown, depth = 0): string[] {
  if (depth > 6) return [];
  const out: string[] = [];
  if (Array.isArray(node)) {
    for (const item of node) out.push(...statusWords(item, depth + 1));
  } else if (node && typeof node === 'object') {
    for (const [key, value] of Object.entries(node as Record<string, unknown>)) {
      if ((key === 'state' || key === 'status') && typeof value === 'string') {
        out.push(value.toLowerCase());
      } else {
        out.push(...statusWords(value, depth + 1));
      }
    }
  }
  return out;
}

function collectUrls(node: unknown, out: string[], depth = 0): void {
  if (depth > 6) return;
  if (Array.isArray(node)) {
    for (const item of node) collectUrls(item, out, depth + 1);
  } else if (node && typeof node === 'object') {
    for (const [key, value] of Object.entries(node as Record<string, unknown>)) {
      const looksLikeUrl = key.endsWith('_url') || key === 'url' || key.endsWith('_urls');
      if (typeof value === 'string' && value.startsWith('http') && looksLikeUrl) {
        out.push(value);
      } else {
        collectUrls(value, out, depth + 1);
      }
    }
  }
}

/**
 * Every artifact URL in a task response, outermost first.
 *
 * Where the artifact lives is not derivable from the OpenAPI spec — `response`
 * is typed as a bare object and the key differs per service (`video_url`,
 * `image_url`, `data[].image_url`). Rather than keep a per-service table that
 * goes stale, collect anything URL-shaped.
 */
export function artifactUrls(state: Record<string, unknown> | null): string[] {
  if (!state) return [];
  const found: string[] = [];
  collectUrls(state.response ?? state, found);
  return [...new Set(found)];
}

/** Percent complete when the service reports it, else null. */
export function taskProgress(state: Record<string, unknown> | null): number | null {
  if (!state) return null;
  for (const value of findKeys(state.response ?? state, ['progress', 'percent', 'percentage'])) {
    if (typeof value === 'boolean') continue;
    if (typeof value === 'number') {
      const pct = value > 0 && value <= 1 ? Math.round(value * 100) : Math.round(value);
      return Math.max(0, Math.min(100, pct));
    }
    if (typeof value === 'string') {
      const parsed = Number.parseFloat(value.trim().replace(/%$/, ''));
      if (!Number.isNaN(parsed)) return Math.max(0, Math.min(100, Math.round(parsed)));
    }
  }
  return null;
}

function* findKeys(node: unknown, names: string[], depth = 0): Generator<unknown> {
  if (depth > 6) return;
  if (Array.isArray(node)) {
    for (const item of node) yield* findKeys(item, names, depth + 1);
  } else if (node && typeof node === 'object') {
    for (const [key, value] of Object.entries(node as Record<string, unknown>)) {
      if (names.includes(key)) yield value;
      else yield* findKeys(value, names, depth + 1);
    }
  }
}

/** The upstream's own words for why a task failed. */
export function failureReason(state: Record<string, unknown> | null): string {
  if (!state) return 'Task failed.';
  const response = (state.response ?? state) as Record<string, unknown>;
  const error = response.error;
  if (error && typeof error === 'object') {
    const message = (error as Record<string, unknown>).message ?? (error as Record<string, unknown>).detail;
    if (typeof message === 'string' && message) return message;
  } else if (typeof error === 'string' && error) {
    return error;
  }
  for (const key of ['message', 'failure_reason', 'fail_reason']) {
    const value = response[key];
    if (typeof value === 'string' && value) return value;
  }
  return 'Task failed.';
}

/**
 * Reduce a poll response to succeeded | failed | '' (still running).
 *
 * Services report completion inconsistently. A status word is the strongest
 * signal and outranks the `success` flag, since a response can carry
 * `success: false` for a retryable hiccup while the task is still running.
 * This normaliser is deliberately broad; narrowing it silently hangs whichever
 * service it drops.
 */
export function taskStatus(state: Record<string, unknown>): 'succeeded' | 'failed' | '' {
  const response = (state.response ?? state) as Record<string, unknown> | null;
  if (!response || typeof response !== 'object') return '';

  const words = statusWords(response);
  if (words.some((w) => FAILED.has(w))) return 'failed';
  if (words.some((w) => DONE.has(w))) {
    // A terminal word with no artifact means the job ended without output.
    return artifactUrls(state).length > 0 ? 'succeeded' : 'failed';
  }
  if (words.length > 0) return '';

  // `success: false` alone is ambiguous — some services set it for a transient
  // hiccup mid-run, alongside a bare string, and carry on. A *structured* error
  // (a dict with a code) is the upstream's final answer: hailuo reports an
  // unavailable model that way, with no finished_at, and treating it as still
  // running makes the caller poll until timeout instead of showing the reason.
  if (response.success === false) {
    const error = response.error as Record<string, unknown> | undefined;
    const structured = !!error && typeof error === 'object' && !!error.code;
    if (artifactUrls(state).length > 0 || structured) return 'failed';
  }

  const finished =
    (response.finished_at !== undefined && response.finished_at !== null) ||
    (state.finished_at !== undefined && state.finished_at !== null);
  if (finished) {
    if (response.success === true) return 'succeeded';
    if (response.success === false) return 'failed';
    if (artifactUrls(state).length > 0) return 'succeeded';
  }

  return artifactUrls(state).length > 0 ? 'succeeded' : '';
}

export class TaskHandle {
  readonly id: string;
  private pollEndpoint: string;
  private transport: Transport;
  private _result: Record<string, unknown> | null = null;

  constructor(
    taskId: string,
    pollEndpoint: string,
    transport: Transport,
    submitted?: Record<string, unknown>,
  ) {
    this.id = taskId;
    this.pollEndpoint = pollEndpoint;
    this.transport = transport;
    // A synchronous submission is already terminal, including failures that
    // have no artifact URL. The caller should not have to skip wait().
    if (submitted) {
      const state = { response: submitted };
      if (taskStatus(state) !== '') this._result = state;
    }
  }

  get done(): boolean {
    return this._result !== null;
  }

  /** Artifact URLs, once completed. */
  urls(): string[] {
    return artifactUrls(this._result);
  }

  progress(): number | null {
    return taskProgress(this._result);
  }

  /**
   * Fetch current task state, remembering it once terminal.
   *
   * A caller that drives its own poll loop — checking status between polls so it
   * can report progress — only ever calls this. Without recording here, urls()
   * and result() stay empty after the task has plainly finished.
   */
  async get(): Promise<Record<string, unknown>> {
    const state = await this.transport.request('POST', this.pollEndpoint, {
      json: { id: this.id, action: 'retrieve' },
    });
    this.accept(state);
    return state;
  }

  private accept(state: Record<string, unknown>): void {
    const status = taskStatus(state);
    if (status === 'succeeded' || status === 'failed') {
      this._result = state;
    }
  }

  async isCompleted(): Promise<boolean> {
    if (this.done) return true;
    await this.get(); // records a terminal state as a side effect
    return this.done;
  }

  async wait(opts: TaskHandleOptions = {}): Promise<Record<string, unknown>> {
    if (this._result !== null) return this._result;

    const pollInterval = opts.pollInterval ?? 3000;
    const maxWait = opts.maxWait ?? 600_000;
    const start = Date.now();

    while (Date.now() - start < maxWait) {
      const state = await this.get();
      if (this.done) return state;
      await new Promise((resolve) => setTimeout(resolve, pollInterval));
    }
    throw new Error(`Task ${this.id} did not complete within ${maxWait}ms`);
  }

  get result(): Record<string, unknown> | null {
    return this._result;
  }
}
