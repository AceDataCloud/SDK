import { AceDataCloud } from '../src/client';

describe('generated providers', () => {
  it('attaches newly added provider namespaces', () => {
    const client = new AceDataCloud({ apiToken: 'test-token' }) as unknown as Record<string, unknown>;

    for (const name of ['drawai', 'gemini', 'grok', 'midjourney', 'qrart', 'qwenimage']) {
      expect(client[name]).toBeDefined();
    }
  });
});
