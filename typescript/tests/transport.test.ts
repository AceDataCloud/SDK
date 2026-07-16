import { Transport } from '../src/runtime/transport';
import { TimeoutError } from '../src/runtime/errors';

describe('Transport API base URL', () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('uses the dedicated X402 host by default', async () => {
    const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ ok: true }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      })
    );
    const transport = new Transport({ apiToken: 'test-token', maxRetries: 0 });

    await transport.request('POST', '/openai/chat/completions', { json: { model: 'test' } });

    expect(fetchMock).toHaveBeenCalledWith(
      'https://x402.acedata.cloud/openai/chat/completions',
      expect.any(Object)
    );
  });

  it('preserves an explicit API base URL override', async () => {
    const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ ok: true }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      })
    );
    const transport = new Transport({
      apiToken: 'test-token',
      baseURL: 'https://api.acedata.cloud/',
      maxRetries: 0,
    });

    await transport.request('GET', '/openai/models');

    expect(fetchMock).toHaveBeenCalledWith('https://api.acedata.cloud/openai/models', expect.any(Object));
  });

  it('maps aborted requests to the SDK TimeoutError', async () => {
    jest.spyOn(global, 'fetch').mockRejectedValue(new DOMException('aborted', 'AbortError'));
    const transport = new Transport({ apiToken: 'test-token', maxRetries: 0 });

    await expect(transport.request('GET', '/openai/models')).rejects.toBeInstanceOf(TimeoutError);
  });

  it('retries once with payment headers when maxRetries is zero', async () => {
    const paymentHandler = jest.fn().mockResolvedValue({
      headers: { 'X-Payment': 'signed-payment' },
    });
    const fetchMock = jest
      .spyOn(global, 'fetch')
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ accepts: [{ network: 'base', scheme: 'exact' }] }), { status: 402 })
      )
      .mockResolvedValueOnce(new Response(JSON.stringify({ ok: true }), { status: 200 }));
    const transport = new Transport({ paymentHandler, maxRetries: 0 });

    await transport.request('POST', '/openai/chat/completions', { json: { model: 'test' } });

    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(fetchMock.mock.calls[1][1]?.headers).toMatchObject({ 'X-Payment': 'signed-payment' });
  });

  it('does not retry a paid request with the same signature', async () => {
    const paymentHandler = jest.fn().mockResolvedValue({
      headers: { 'X-Payment': 'signed-payment' },
    });
    const fetchMock = jest
      .spyOn(global, 'fetch')
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ accepts: [{ network: 'base', scheme: 'exact' }] }), { status: 402 })
      )
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ error: { message: 'upstream failed' } }), { status: 500 })
      )
      .mockResolvedValueOnce(new Response(JSON.stringify({ ok: true }), { status: 200 }));
    const transport = new Transport({ paymentHandler, maxRetries: 2 });

    await expect(
      transport.request('POST', '/openai/chat/completions', { json: { model: 'test' } })
    ).rejects.toThrow('upstream failed');

    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it.each([null, [], 'error', { accepts: 'base' }, { accepts: [null] }])(
    'rejects malformed payment requirements: %p',
    async (body) => {
      const paymentHandler = jest.fn();
      jest.spyOn(global, 'fetch').mockResolvedValue(
        new Response(JSON.stringify(body), { status: 402 })
      );
      const transport = new Transport({ paymentHandler, maxRetries: 0 });

      await expect(
        transport.request('POST', '/openai/chat/completions', { json: { model: 'test' } })
      ).rejects.toMatchObject({ code: 'invalid_402' });

      expect(paymentHandler).not.toHaveBeenCalled();
    }
  );

  it('retries streaming requests with payment headers', async () => {
    const paymentHandler = jest.fn().mockResolvedValue({
      headers: { 'X-Payment': 'signed-payment' },
    });
    const fetchMock = jest
      .spyOn(global, 'fetch')
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ accepts: [{ network: 'base', scheme: 'exact' }] }), { status: 402 })
      )
      .mockResolvedValueOnce(
        new Response('data: {"delta":"ok"}\n\ndata: [DONE]\n\n', {
          status: 200,
          headers: { 'content-type': 'text/event-stream' },
        })
      );
    const transport = new Transport({ paymentHandler, maxRetries: 0 });

    const chunks: string[] = [];
    for await (const chunk of transport.requestStream('POST', '/openai/chat/completions', {
      json: { model: 'test', stream: true },
    })) {
      chunks.push(chunk);
    }

    expect(chunks).toEqual(['{"delta":"ok"}']);
    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(fetchMock.mock.calls[1][1]?.headers).toMatchObject({ 'X-Payment': 'signed-payment' });
    expect(fetchMock.mock.calls[1][1]?.signal).not.toBe(fetchMock.mock.calls[0][1]?.signal);
  });

  it('cancels a paid stream when the consumer exits early', async () => {
    const paymentHandler = jest.fn().mockResolvedValue({
      headers: { 'X-Payment': 'signed-payment' },
    });
    const cancel = jest.fn();
    const streamBody = new ReadableStream<Uint8Array>({
      start(controller) {
        controller.enqueue(new TextEncoder().encode('data: {"delta":"ok"}\n\n'));
      },
      cancel,
    });
    jest
      .spyOn(global, 'fetch')
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ accepts: [{ network: 'base', scheme: 'exact' }] }), { status: 402 })
      )
      .mockResolvedValueOnce(new Response(streamBody, { status: 200 }));
    const transport = new Transport({ paymentHandler, maxRetries: 0 });

    for await (const _chunk of transport.requestStream('POST', '/openai/chat/completions', {
      json: { model: 'test', stream: true },
    })) {
      break;
    }

    expect(cancel).toHaveBeenCalledTimes(1);
  });

  it('resets the idle timeout after each stream chunk', async () => {
    const encoder = new TextEncoder();
    const streamBody = new ReadableStream<Uint8Array>({
      async start(controller) {
        await new Promise((resolve) => setTimeout(resolve, 5));
        controller.enqueue(encoder.encode('data: {"delta":"one"}\n\n'));
        await new Promise((resolve) => setTimeout(resolve, 5));
        controller.enqueue(encoder.encode('data: {"delta":"two"}\n\ndata: [DONE]\n\n'));
        controller.close();
      },
    });
    jest.spyOn(global, 'fetch').mockResolvedValue(new Response(streamBody, { status: 200 }));
    const transport = new Transport({ apiToken: 'test-token', maxRetries: 0 });

    const chunks: string[] = [];
    for await (const chunk of transport.requestStream('POST', '/openai/chat/completions', {
      json: { model: 'test', stream: true },
      timeout: 8,
    })) {
      chunks.push(chunk);
    }

    expect(chunks).toEqual(['{"delta":"one"}', '{"delta":"two"}']);
  });

  it('preserves TimeoutError when stream cancellation also fails', async () => {
    jest.useFakeTimers();
    const cancel = jest.fn().mockRejectedValue(new DOMException('aborted', 'AbortError'));
    const reader = {
      read: jest.fn().mockImplementation(
        () => new Promise((_, reject) => setTimeout(() => reject(new DOMException('aborted', 'AbortError')), 10))
      ),
      cancel,
    };
    const body = { getReader: () => reader } as unknown as ReadableStream<Uint8Array>;
    jest.spyOn(global, 'fetch').mockResolvedValue({ status: 200, body } as Response);
    const transport = new Transport({ apiToken: 'test-token', maxRetries: 0 });

    const result = (async () => {
      for await (const _chunk of transport.requestStream('GET', '/stream', { timeout: 5 })) {
        // No chunks expected.
      }
    })();
    const assertion = expect(result).rejects.toBeInstanceOf(TimeoutError);
    await jest.advanceTimersByTimeAsync(10);

    await assertion;
    expect(cancel).toHaveBeenCalledTimes(1);
    jest.useRealTimers();
  });

  it('maps aborted uploads to the SDK TimeoutError', async () => {
    jest.spyOn(global, 'fetch').mockRejectedValue(new DOMException('aborted', 'AbortError'));
    const transport = new Transport({ apiToken: 'test-token', maxRetries: 0 });

    await expect(transport.upload('/api/v1/files/', new Uint8Array([1]), 'test.txt')).rejects.toBeInstanceOf(
      TimeoutError
    );
  });
});