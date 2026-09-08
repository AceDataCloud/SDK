import { Localization } from '../src/resources/providers/localization';

describe('Localization provider', () => {
  it('serializes markdown string input', async () => {
    const request = jest.fn().mockResolvedValue({ locale: 'de', data: '# Titel' });
    const localization = new Localization({ request } as any);

    await localization.translate({
      input: '# Title',
      locale: 'de',
      extension: 'md',
    });

    expect(request).toHaveBeenCalledWith('POST', '/localization/translate', {
      json: {
        input: '# Title',
        locale: 'de',
        extension: 'md',
      },
    });
  });
});
