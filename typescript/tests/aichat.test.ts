import type { AiChatModel } from '../src';

describe('AiChatModel', () => {
  it('includes the latest models', () => {
    const models: AiChatModel[] = [
      'gpt-5.6-luna',
      'gpt-5.6-terra',
      'gpt-5.6-sol',
      'gpt-5.4-mini',
      'gpt-5.4-nano',
      'grok-4.5',
      'glm-5.2',
      'glm-5',
      'glm-5-turbo',
    ];

    expect(models).toHaveLength(9);
  });
});
