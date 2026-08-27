import { OpenAI } from '../src/resources/openai';

describe('OpenAI resource', () => {
  it('calls models endpoint with optional accept header', async () => {
    const request = jest.fn().mockResolvedValue({ object: 'list', data: [{ id: 'gpt-4o-mini' }] });
    const openai = new OpenAI({ request } as any);

    const result = await openai.models.list({ accept: 'application/json' });

    expect(result).toEqual({ object: 'list', data: [{ id: 'gpt-4o-mini' }] });
    expect(request).toHaveBeenCalledWith('GET', '/openai/models', {
      headers: { accept: 'application/json' },
    });
  });
});
