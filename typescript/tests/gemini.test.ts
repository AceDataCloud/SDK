import { Gemini } from '../src/resources/providers/gemini';
import { AceDataCloud } from '../src/client';

describe('Gemini provider', () => {
  it('is available from the top-level client', () => {
    expect(new AceDataCloud({ apiToken: 'test' }).gemini).toBeInstanceOf(Gemini);
  });

  it('interpolates the model path parameter without putting it in the body', async () => {
    const request = jest.fn().mockResolvedValue({ success: true });
    const gemini = new Gemini({ request } as any);
    const contents = [{ role: 'user', parts: [{ text: 'Hello' }] }];

    await gemini.model_generatecontent({ model: 'gemini-3.1-flash-lite', contents });

    expect(request).toHaveBeenCalledWith(
      'POST',
      '/v1beta/models/gemini-3.1-flash-lite:generateContent',
      { json: { contents } },
    );
  });
});
