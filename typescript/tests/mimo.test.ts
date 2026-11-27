import { AiChatModel } from '../src/resources/aichat';
import { OpenAI } from '../src/resources/openai';

describe('prepared MiMo Chat Completions', () => {
  it.each<AiChatModel>(['mimo-v2.6-pro', 'mimo-v2.6-flash'])(
    'preserves %s and its reasoning controls in ordinary and streaming calls',
    async (model) => {
      const request = jest.fn().mockResolvedValue({});
      const requestStream = jest.fn().mockImplementation(async function* () {
        yield '{"choices":[]}';
      });
      const client = new OpenAI({ request, requestStream } as any);
      const opts = {
        model,
        messages: [{ role: 'assistant', content: 'Ready', reasoning_content: 'Captured reasoning' }],
        max_completion_tokens: 64,
        thinking: { type: 'enabled' },
        tool_choice: 'auto',
      };
      await client.chat.completions.create(opts);
      expect(request).toHaveBeenCalledWith('POST', '/openai/chat/completions', { json: opts });
      const stream = await client.chat.completions.create({ ...opts, stream: true });
      const chunks = [];
      for await (const chunk of stream) chunks.push(chunk);
      expect(chunks).toEqual([{ choices: [] }]);
      expect(requestStream).toHaveBeenCalledWith('POST', '/openai/chat/completions', {
        json: { ...opts, stream: true },
      });
    }
  );
});
