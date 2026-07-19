import { Kimi } from '../src/resources/kimi';

describe('Kimi resource', () => {
  it('uses /kimi/chat/completions for non-stream requests', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'chatcmpl-kimi' });
    const kimi = new Kimi({ request } as any);

    await kimi.chat.completions.create({
      model: 'kimi-k3',
      messages: [{ role: 'user', content: 'Hello' }],
      temperature: 0.2,
    });

    expect(request).toHaveBeenCalledWith('POST', '/kimi/chat/completions', {
      json: {
        model: 'kimi-k3',
        messages: [{ role: 'user', content: 'Hello' }],
        temperature: 0.2,
      },
    });
  });
});
