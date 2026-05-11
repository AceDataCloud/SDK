/** AI Chat v2 resources — aichat2/conversations endpoint. */

import { Transport } from '../runtime/transport';

export type AiChat2Model =
  | 'gpt-4'
  | 'gpt-4.1'
  | 'gpt-4.1-mini'
  | 'gpt-4.1-nano'
  | 'gpt-4o'
  | 'gpt-4o-2024-05-13'
  | 'gpt-4o-all'
  | 'gpt-4o-image'
  | 'gpt-4o-mini'
  | 'gpt-5-all'
  | 'gpt-5.1-all'
  | 'gpt-5.2-pro'
  | 'gpt-5.4-mini'
  | 'gpt-5.4-nano'
  | 'gpt-image-1'
  | 'claude-3-5-haiku-20241022'
  | 'claude-3-5-sonnet-20240620'
  | 'claude-3-5-sonnet-20241022'
  | 'claude-3-7-sonnet-20250219'
  | 'claude-3-haiku-20240307'
  | 'claude-3-opus-20240229'
  | 'claude-3-sonnet-20240229'
  | 'claude-haiku-4-5-20251001'
  | 'claude-opus-4-1-20250805'
  | 'claude-opus-4-20250514'
  | 'claude-opus-4-5-20251101'
  | 'claude-opus-4-6'
  | 'claude-opus-4-7'
  | 'claude-sonnet-4-20250514'
  | 'claude-sonnet-4-5-20250929'
  | 'claude-sonnet-4-6'
  | 'gemini-2.0-flash-lite'
  | 'gemini-2.5-flash-lite'
  | 'gemini-3-pro-preview'
  | 'gemini-3.1-flash-image-preview'
  | 'gemini-3.1-flash-lite-preview'
  | 'gemini-3.1-pro'
  | 'gemini-3.1-pro-preview'
  | 'grok-2-vision'
  | 'grok-2-vision-1212'
  | 'grok-3'
  | 'grok-3-fast'
  | 'grok-3-mini'
  | 'grok-3-mini-fast'
  | 'grok-4'
  | 'grok-4-0709'
  | 'grok-4-1-fast'
  | 'grok-4-1-fast-non-reasoning'
  | 'grok-4-1-fast-reasoning'
  | 'deepseek-chat'
  | 'deepseek-r1'
  | 'deepseek-r1-0528'
  | 'deepseek-reasoner'
  | 'deepseek-v3'
  | 'deepseek-v3-250324'
  | 'deepseek-v3.2-exp'
  | 'deepseek-v4-flash'
  | 'kimi-k2-0711-preview'
  | 'kimi-k2-0905-preview'
  | 'kimi-k2-instruct-0905'
  | 'kimi-k2-thinking'
  | 'kimi-k2-thinking-turbo'
  | 'kimi-k2-turbo-preview'
  | 'kimi-k2.5'
  | 'glm-3-turbo'
  | 'glm-4-air'
  | 'glm-4-flash'
  | 'glm-4-plus'
  | 'glm-4.5'
  | 'glm-4.5-air'
  | 'glm-4.5v'
  | 'glm-4.6'
  | 'glm-4.7'
  | 'glm-5'
  | 'glm-5-turbo'
  | 'glm-5.1'
  | 'o1'
  | 'o1-mini'
  | 'o1-pro'
  | 'o3'
  | 'o3-mini'
  | 'o3-pro'
  | 'o4-mini'
  | (string & {});

export class AiChat2 {
  constructor(private transport: Transport) {}

  async create(opts: {
    model: AiChat2Model;
    action?: string;
    id?: string;
    question?: string;
    message?: unknown;
    stateful?: boolean;
    references?: string[];
    preset?: string;
    maxTurns?: number;
    toolResults?: unknown[];
    messages?: unknown[];
    title?: string;
    userId?: string;
    applicationId?: string;
    modelGroup?: string;
    offset?: number;
    limit?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const {
      model, action, id, question, message, stateful, references, preset,
      maxTurns, toolResults, messages, title, userId, applicationId,
      modelGroup, offset, limit, ...rest
    } = opts;
    const body: Record<string, unknown> = { model, ...rest };
    if (action !== undefined) body.action = action;
    if (id !== undefined) body.id = id;
    if (question !== undefined) body.question = question;
    if (message !== undefined) body.message = message;
    if (stateful !== undefined) body.stateful = stateful;
    if (references !== undefined) body.references = references;
    if (preset !== undefined) body.preset = preset;
    if (maxTurns !== undefined) body.max_turns = maxTurns;
    if (toolResults !== undefined) body.tool_results = toolResults;
    if (messages !== undefined) body.messages = messages;
    if (title !== undefined) body.title = title;
    if (userId !== undefined) body.user_id = userId;
    if (applicationId !== undefined) body.application_id = applicationId;
    if (modelGroup !== undefined) body.model_group = modelGroup;
    if (offset !== undefined) body.offset = offset;
    if (limit !== undefined) body.limit = limit;
    return this.transport.request('POST', '/aichat2/conversations', { json: body });
  }
}
