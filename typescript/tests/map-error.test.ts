import { APIError } from '../src/runtime/errors';
import { mapError } from '../src/runtime/transport';

describe('mapError body shapes', () => {
  test('error as string is preserved as message', () => {
    const err = mapError(402, { error: 'Facilitator verify returned empty body' });
    expect(err).toBeInstanceOf(APIError);
    expect(err.statusCode).toBe(402);
    expect(err.code).toBe('');
    expect(err.message).toContain('Facilitator verify');
  });

  test('missing error field falls back to empty defaults', () => {
    const err = mapError(500, {});
    expect(err).toBeInstanceOf(APIError);
    expect(err.statusCode).toBe(500);
    expect(err.code).toBe('');
  });

  test('error as dict is used as-is', () => {
    const err = mapError(400, {
      error: { code: 'bad_request', message: 'missing field' },
      trace_id: 't-1',
    });
    expect(err.statusCode).toBe(400);
    expect(err.code).toBe('bad_request');
    expect(err.message).toBe('missing field');
    expect(err.traceId).toBe('t-1');
  });

  test('error as non-dict non-string falls back to empty', () => {
    const err = mapError(502, { error: ['a', 'b'] as unknown });
    expect(err).toBeInstanceOf(APIError);
    expect(err.code).toBe('');
  });

  test.each([
    ['api_error', 'the account may have been offline'],
    ['suno_processing_unavailable', 'Music processing is unavailable. Contact support with the trace ID.'],
    ['suno_model_unavailable', 'The selected model is unavailable for this operation. Contact support with the trace ID.'],
    ['suno_processing_failed', 'Music processing returned no audio. Contact support with the trace ID.'],
  ])('preserves support details for %s', (code, message) => {
    const body = { error: { code, message }, trace_id: 'test-trace' };

    const err = mapError(500, body);

    expect(err).toBeInstanceOf(APIError);
    expect(err.statusCode).toBe(500);
    expect(err.code).toBe(code);
    expect(err.message).toBe(message);
    expect(err.traceId).toBe(body.trace_id);
    expect(err.body).toEqual(body);
  });

  test('error as null falls back to empty', () => {
    const err = mapError(400, { error: null });
    expect(err).toBeInstanceOf(APIError);
    expect(err.message).toBe('');
  });
});
