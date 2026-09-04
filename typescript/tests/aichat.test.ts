import type { AiChatModel } from '../src/resources/aichat';

describe('AiChat model typing', () => {
  it('includes newly published model names', () => {
    const modelA: AiChatModel = 'gpt-5.6-sol';
    const modelB: AiChatModel = 'grok-4.5';
    expect(modelA).toBe('gpt-5.6-sol');
    expect(modelB).toBe('grok-4.5');
  });
});
