import { Acemusic } from '../src/resources/providers/acemusic';
import { TaskHandle, taskStatus } from '../src/runtime/tasks';
import { Transport } from '../src/runtime/transport';

describe('ACE Music', () => {
  it('submits once with a correctly named idempotency header', async () => {
    const request = jest.fn().mockResolvedValue({task_id:'original'});
    const provider = new Acemusic({request} as any);
    const task = await provider.generate({prompt:'folk', idempotencyKey:'stable'});
    expect(task).toBeInstanceOf(TaskHandle);
    expect(task.id).toBe('original');
    expect(request).toHaveBeenCalledWith('POST','/acemusic/audios',{
      json:{action:'generate',prompt:'folk',async:true},
      headers:{'Idempotency-Key':'stable'},
    });
  });
  it('keeps processing groups pending and treats partial failure as terminal', () => {
    const response={data:[{state:'succeeded',audio_url:'https://cdn.acedata.cloud/one.mp3'}]};
    expect(taskStatus({state:'processing',response})).toBe('');
    expect(taskStatus({state:'partial_failed',response})).toBe('failed');
  });
  it('does not retry a lost paid submission', async () => {
    const previous=global.fetch;
    const mock=jest.fn().mockRejectedValue(new Error('lost response'));
    global.fetch=mock as any;
    try {
      const transport=new Transport({apiToken:'token',maxRetries:2});
      await expect(transport.request('POST','/acemusic/audios',{json:{prompt:'folk'}})).rejects.toThrow();
      expect(mock).toHaveBeenCalledTimes(1);
    } finally { global.fetch=previous; }
  });
  it('passes task filters without mixing pagination shapes', async () => {
    const request = jest.fn().mockResolvedValue({items:[],count:0});
    const provider = new Acemusic({request} as any);
    await provider.tasks({action:'list',type:'audios',limit:10,offset:20,createdAtMin:100,createdAtMax:200});
    expect(request).toHaveBeenLastCalledWith('POST','/acemusic/tasks',{json:{
      action:'list',type:'audios',limit:10,offset:20,created_at_min:100,created_at_max:200,
    }});
    await provider.tasks({action:'list',page:2,pageSize:5});
    expect(request).toHaveBeenLastCalledWith('POST','/acemusic/tasks',{json:{action:'list',page:2,page_size:5}});
  });

  it.each([
    [{action:'upload',audioUrl:'https://example.com/reference.mp3'}, {action:'upload',audio_url:'https://example.com/reference.mp3',async:true}],
    [{action:'cover',audioId:'track-a',lyric:'Verse',style:'Folk'}, {action:'cover',audio_id:'track-a',lyric:'Verse',style:'Folk',async:true}],
    [{action:'mashup',mashupAudioIds:['a','b'],lyric:'Verse',style:'Folk',audioInfluence:80}, {action:'mashup',mashup_audio_ids:['a','b'],lyric:'Verse',style:'Folk',audio_influence:80,async:true}],
  ])('does not inject defaults from other actions', async (options, expected) => {
    const request = jest.fn().mockResolvedValue({task_id:'original'});
    const provider = new Acemusic({request} as any);
    await provider.generate(options as any);
    expect(request.mock.calls[0][2].json).toEqual(expected);
  });

});
