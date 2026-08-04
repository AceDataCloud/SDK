import { Suno } from '../src/resources/providers/suno';

describe('Suno provider', () => {
  it('lists personas with query params', async () => {
    const request = jest.fn().mockResolvedValue({ items: [], count: 0 });
    const suno = new Suno({ request } as any);

    await suno.personaList({ userId: 'user-1', limit: 10, offset: 5 });

    expect(request).toHaveBeenCalledWith('GET', '/suno/persona', {
      params: { user_id: 'user-1', limit: '10', offset: '5' },
    });
  });

  it('deletes a persona with query params', async () => {
    const request = jest.fn().mockResolvedValue({ success: true });
    const suno = new Suno({ request } as any);

    await suno.personaDelete({ personaId: 'p-1', userId: 'user-1' });

    expect(request).toHaveBeenCalledWith('DELETE', '/suno/persona', {
      params: { persona_id: 'p-1', user_id: 'user-1' },
    });
  });
});
