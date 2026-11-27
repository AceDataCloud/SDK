import { Tripo } from '../src/resources/providers/tripo';

it('keeps rig checks free of rig options and preserves the retry key', async () => {
  const request = jest.fn().mockResolvedValue({task_id:'original'});
  const provider = new Tripo({request} as any);
  await provider.animations({action:'rig_check', modelId:'asset', idempotencyKey:'stable'});
  const [,path,options] = request.mock.calls[0];
  expect(path).toBe('/tripo/animations');
  expect(options.json).toEqual({action:'rig_check', model_id:'asset', async:true});
  expect(options.headers).toEqual({'Idempotency-Key':'stable'});
});
