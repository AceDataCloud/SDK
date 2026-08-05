import { Seedream } from '../src/resources/providers/seedream';

describe('Seedream provider', () => {
  it('serializes the current Seedream schema', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-seedream' });
    const seedream = new Seedream({ request } as any);

    await seedream.generate({
      model: 'doubao-seedream-5-0-pro-260628',
      prompt: 'a cat',
      image: ['https://example.com/reference.png'],
      sequentialImageGeneration: 'auto',
      sequentialImageGenerationOptions: { max_images: 2 },
      responseFormat: 'b64_json',
      tools: [{ type: 'web_search' }],
    });

    const body = request.mock.calls[0][2].json;
    expect(body).toMatchObject({
      model: 'doubao-seedream-5-0-pro-260628',
      sequential_image_generation: 'auto',
      sequential_image_generation_options: { max_images: 2 },
      response_format: 'b64_json',
    });
    expect(body).not.toHaveProperty('seed');
    expect(body).not.toHaveProperty('guidance_scale');
  });
});
