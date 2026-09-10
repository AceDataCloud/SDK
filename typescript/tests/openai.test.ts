import { OpenAI } from '../src/resources/openai';

describe('OpenAI resource', () => {
  it.each(['gpt-image-2.5-flare:official', 'gpt-image-2.5-sunburst:official'] as const)(
    'sends %s to both image endpoints',
    async (model) => {
      const request = jest.fn().mockResolvedValue({ data: [] });
      const openai = new OpenAI({ request } as any);

      await openai.images.generate({ prompt: 'A cat', model });
      await openai.images.edit({ image: 'https://example.com/cat.png', prompt: 'Add a hat', model });

      expect(request).toHaveBeenNthCalledWith(1, 'POST', '/openai/images/generations', {
        json: { prompt: 'A cat', model },
      });
      expect(request).toHaveBeenNthCalledWith(2, 'POST', '/openai/images/edits', {
        json: { image: 'https://example.com/cat.png', prompt: 'Add a hat', model },
      });
    }
  );
});
