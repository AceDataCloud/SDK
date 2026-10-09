import { AiChat, AiChatModel } from '../src/resources/aichat';
import { Chat } from '../src/resources/chat';
import { OpenAI } from '../src/resources/openai';
import { NanoBanana, NanoBananaGenerateOptions } from '../src/resources/providers/nano-banana';
import { TaskHandle } from '../src/runtime/tasks';

const solFastModel: AiChatModel = 'gpt-5.6-sol-fast';

describe('GPT-5.6 Sol Fast', () => {
  it.each(['completions', 'responses', 'messages', 'aichat'])(
    'preserves the public model ID in %s requests',
    async (operation) => {
      const request = jest.fn().mockResolvedValue({});
      const transport = { request } as any;
      const openai = new OpenAI(transport);
      const messages = [{ role: 'user', content: 'Hello' }];
      let path: string;
      let body: Record<string, unknown>;
      switch (operation) {
        case 'completions':
          path = '/openai/chat/completions';
          body = { model: solFastModel, messages };
          await openai.chat.completions.create({ model: solFastModel, messages });
          break;
        case 'responses':
          path = '/openai/responses';
          body = { model: solFastModel, input: 'Hello' };
          await openai.responses.create({ model: solFastModel, input: 'Hello' });
          break;
        case 'messages':
          path = '/v1/messages';
          body = { model: solFastModel, messages, max_tokens: 64 };
          await new Chat(transport).messages.create({ model: solFastModel, messages, maxTokens: 64 });
          break;
        default:
          path = '/aichat/conversations';
          body = { model: solFastModel, question: 'Hello' };
          await new AiChat(transport).create({ model: solFastModel, question: 'Hello' });
      }
      expect(request).toHaveBeenCalledTimes(1);
      expect(request).toHaveBeenCalledWith('POST', path, { json: body });
    }
  );

  it.each(['completions', 'responses', 'messages'])(
    'preserves the public model ID in streaming %s requests',
    async (operation) => {
      const requestStream = jest.fn().mockImplementation(async function* () {});
      const transport = { requestStream } as any;
      const openai = new OpenAI(transport);
      const messages = [{ role: 'user', content: 'Hello' }];
      const stream = operation === 'completions'
        ? await openai.chat.completions.create({ model: solFastModel, messages, stream: true })
        : operation === 'responses'
          ? await openai.responses.create({ model: solFastModel, input: 'Hello', stream: true })
          : await new Chat(transport).messages.create({ model: solFastModel, messages, maxTokens: 64, stream: true });
      for await (const chunk of stream) {
        throw new Error(`Unexpected chunk: ${JSON.stringify(chunk)}`);
      }
      const path = operation === 'completions' ? '/openai/chat/completions'
        : operation === 'responses' ? '/openai/responses' : '/v1/messages';
      const body = operation === 'responses' ? { input: 'Hello' }
        : operation === 'messages' ? { messages, max_tokens: 64 } : { messages };
      expect(requestStream).toHaveBeenCalledTimes(1);
      expect(requestStream).toHaveBeenCalledWith('POST', path, {
        json: { model: solFastModel, ...body, stream: true },
      });
    }
  );
});

describe('Nano Banana 2.1', () => {
  it.each(['generate', 'edit'] as const)(
    'serializes %s at every supported resolution',
    async (action) => {
      for (const resolution of ['1K', '2K', '4K'] as const) {
        const request = jest.fn().mockResolvedValue({});
        const nanoBanana = new NanoBanana({ request } as any);
        const options: NanoBananaGenerateOptions = {
          action,
          model: 'nano-banana-2.1',
          prompt: 'A vase',
          resolution,
          aspectRatio: '1:1',
        };
        if (action === 'edit') options.imageUrls = ['https://example.com/vase.png'];

        const task = await nanoBanana.generate(options);

        expect(task).toBeInstanceOf(TaskHandle);
        expect(request).toHaveBeenCalledTimes(1);
        expect(request).toHaveBeenCalledWith('POST', '/nano-banana/images', {
          json: {
            action,
            model: 'nano-banana-2.1',
            prompt: 'A vase',
            resolution,
            aspect_ratio: '1:1',
            ...(action === 'edit' ? { image_urls: options.imageUrls } : {}),
            count: 1,
            async: true,
          },
        });
      }
    }
  );

  it('preserves backend defaults and only advertises published variants', async () => {
    type Model = NanoBananaGenerateOptions['model'];
    const official21IsSupported: 'nano-banana-2.1:official' extends Model ? true : false = false;
    const official2: Model = 'nano-banana-2:official';
    expect(official21IsSupported).toBe(false);
    expect(official2).toBe('nano-banana-2:official');
    const request = jest.fn().mockResolvedValue({});

    await new NanoBanana({ request } as any).generate({ action: 'generate', prompt: 'A vase' });

    expect(request.mock.calls[0][2].json).not.toHaveProperty('model');
    expect(request.mock.calls[0][2].json).not.toHaveProperty('resolution');
  });
});

describe('OpenAI resource', () => {
  it.each(['text-embedding-3-small', 'text-embedding-3-large'])(
    'sends supported embedding model %s and optional parameters',
    async (model) => {
      const request = jest.fn().mockResolvedValue({});
      const openai = new OpenAI({ request } as any);

      await openai.embeddings.create({
        model,
        input: ['Hello!', 'Goodbye!'],
        encodingFormat: 'base64',
        dimensions: 256,
      });

      expect(request).toHaveBeenCalledWith('POST', '/openai/embeddings', {
        json: {
          model,
          input: ['Hello!', 'Goodbye!'],
          encoding_format: 'base64',
          dimensions: 256,
        },
      });
    }
  );

  it.each(['gpt-image-2.5-flare:official', 'gpt-image-2.5-sunburst:official', 'nano-banana-2.1'] as const)(
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

  it('keeps dynamically discovered image model IDs compatible', async () => {
    const request = jest.fn().mockResolvedValue({ data: [] });
    const openai = new OpenAI({ request } as any);
    const model: string = 'future-image-model';

    await openai.images.generate({ prompt: 'A cat', model });

    expect(request).toHaveBeenCalledWith('POST', '/openai/images/generations', {
      json: { prompt: 'A cat', model },
    });
  });
});
