import { Chat } from '../src/resources/chat';
import { Transport } from '../src/runtime/transport';

describe('Claude Messages', () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('sends the documented output configuration', async () => {
    const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ id: 'msg-123' }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      })
    );
    const chat = new Chat(new Transport({ apiToken: 'test-token', maxRetries: 0 }));

    await chat.messages.create({
      model: 'claude-opus-5',
      messages: [{ role: 'user', content: 'Hello' }],
      maxTokens: 1024,
      outputConfig: { effort: 'max' },
    });

    expect(JSON.parse(fetchMock.mock.calls[0][1]?.body as string)).toEqual({
      model: 'claude-opus-5',
      messages: [{ role: 'user', content: 'Hello' }],
      max_tokens: 1024,
      output_config: { effort: 'max' },
    });
  });
});
