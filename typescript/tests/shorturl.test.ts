import { ShortUrl } from '../src/resources/shorturl';

describe('ShortUrl resource', () => {
  it('sends content to /shorturl', async () => {
    const request = jest.fn().mockResolvedValue({ success: true });
    const shorturl = new ShortUrl({ request } as any);

    await shorturl.create({ content: 'https://platform.acedata.cloud/documents/x' });

    expect(request).toHaveBeenCalledWith('POST', '/shorturl', {
      json: { content: 'https://platform.acedata.cloud/documents/x' },
    });
  });

  it('maps legacy url to content', async () => {
    const request = jest.fn().mockResolvedValue({ success: true });
    const shorturl = new ShortUrl({ request } as any);

    await shorturl.create({ url: 'https://platform.acedata.cloud/documents/x' });

    expect(request).toHaveBeenCalledWith('POST', '/shorturl', {
      json: { content: 'https://platform.acedata.cloud/documents/x' },
    });
  });
});
