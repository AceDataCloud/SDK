import { Minimax } from '../src/resources/providers/minimax';
import { TaskHandle } from '../src/runtime/tasks';

describe('Minimax provider', () => {
  it('posts the Docs request shape and returns a task handle', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'minimax-1' });
    const minimax = new Minimax({ request } as never);

    const handle = await minimax.generate({
      model: 'MiniMax-H3',
      content: [
        { type: 'text', text: 'let the subject move naturally' },
        {
          type: 'image_url',
          image_url: { url: 'https://cdn.example.com/frame.png' },
          role: 'first_frame',
        },
      ],
      resolution: '2K',
      duration: 5,
      ratio: 'adaptive',
      aigcWatermark: false,
    });

    expect(handle).toBeInstanceOf(TaskHandle);
    expect(handle.id).toBe('minimax-1');
    expect(request).toHaveBeenCalledWith('POST', '/minimax/videos', {
      json: {
        model: 'MiniMax-H3',
        content: [
          { type: 'text', text: 'let the subject move naturally' },
          {
            type: 'image_url',
            image_url: { url: 'https://cdn.example.com/frame.png' },
            role: 'first_frame',
          },
        ],
        resolution: '2K',
        duration: 5,
        ratio: 'adaptive',
        aigc_watermark: false,
      },
    });
  });
});
