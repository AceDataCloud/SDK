import test from "node:test";
import assert from "node:assert/strict";
import { fetchTracks } from "./tasks.js";
test("retrieves only the existing task and preserves partial results",async()=>{
 const result=await fetchTracks("example","abc",async(url,request)=>{
   assert.equal(url,"https://api.acedata.cloud/acemusic/tasks");
   assert.deepEqual(JSON.parse(request.body),{action:"retrieve",id:"abc"});
   return Response.json({id:"abc",response:{task_id:"abc",status:"partial_failed",data:[{title:"Track",audio_url:"https://example.com/song.mp3",duration:2}]}});
 });
 assert.equal(result.state,"partial_failed");assert.equal(result.tracks[0].durationMs,2000);
});
test("rejects a task identity mismatch",async()=>{
 await assert.rejects(fetchTracks("example","abc",async()=>Response.json({id:"def"})),/ID differs/);
});
test("generation uses an explicit request key and returns the original task ID", async () => {
  const { generateTrack } = await import("./tasks.js");
  const id = await generateTrack("example", " Jazz ", "one-action", async (url, request) => {
    assert.equal(url, "https://api.acedata.cloud/acemusic/audios");
    const body = JSON.parse(request.body);
    assert.equal(body.prompt, "Jazz");
    assert.equal(request.headers["Idempotency-Key"], "one-action");
    assert.equal(body.idempotency_key, undefined);
    assert.equal(body.async, true);
    return Response.json({ task_id: "owned" });
  });
  assert.equal(id, "owned");
});
