import type { AiChatModel } from '../src/resources/aichat';

describe('AiChat model literals', () => {
  it('includes deepseek-v4-pro', () => {
    const model: AiChatModel = 'deepseek-v4-pro';
    expect(model).toBe('deepseek-v4-pro');
  });
});
