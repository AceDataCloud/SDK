import { OpenAI } from '../src/resources/openai';

describe('OpenAI resource', () => {
  it('uses the documented openai images edit request shape', async () => {
    const request = jest.fn().mockResolvedValue({ data: [] });
    const openai = new OpenAI({ request } as any);

    await openai.images.edit({
      image: 'https://example.com/input.png',
      prompt: 'Turn this into a watercolor',
      model: 'gpt-image-1',
      n: 2,
      background: 'auto',
      inputFidelity: 'high',
      outputFormat: 'webp',
      outputCompression: 80,
      quality: 'high',
      size: '1024x1024',
      responseFormat: 'b64_json',
      callbackUrl: 'https://example.com/callback',
      async: true,
    });

    expect(request).toHaveBeenCalledWith('POST', '/openai/images/edits', {
      json: {
        image: 'https://example.com/input.png',
        prompt: 'Turn this into a watercolor',
        model: 'gpt-image-1',
        n: 2,
        background: 'auto',
        input_fidelity: 'high',
        output_format: 'webp',
        output_compression: 80,
        quality: 'high',
        size: '1024x1024',
        response_format: 'b64_json',
        callback_url: 'https://example.com/callback',
        async: true,
      },
    });
  });
});
