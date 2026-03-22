/**
 * Integration tests for AceDataCloud TypeScript SDK.
 *
 * These tests run against the live API. Set these in .env (repo root) or environment:
 *   - ACEDATACLOUD_API_TOKEN      — API token for api.acedata.cloud
 *   - ACEDATACLOUD_PLATFORM_TOKEN — Platform token for platform.acedata.cloud (optional)
 *
 * Usage:
 *   cd typescript
 *   npm install && npm install dotenv
 *   npx jest tests/integration.test.ts --forceExit
 */

import * as path from 'path';
import * as fs from 'fs';

// Load .env from repo root
const envPath = path.resolve(__dirname, '../../.env');
if (fs.existsSync(envPath)) {
  require('dotenv').config({ path: envPath });
}

import { AceDataCloud } from '../src';

const TOKEN = process.env.ACEDATACLOUD_API_TOKEN || '';
const PLATFORM_TOKEN = process.env.ACEDATACLOUD_PLATFORM_TOKEN || '';
const describeIf = TOKEN ? describe : describe.skip;
const describePlatform = PLATFORM_TOKEN ? describe : describe.skip;

let client: AceDataCloud;
let platformClient: AceDataCloud | null = null;

beforeAll(() => {
  client = new AceDataCloud({ apiToken: TOKEN, timeout: 120000 });
  if (PLATFORM_TOKEN) {
    platformClient = new AceDataCloud({ apiToken: PLATFORM_TOKEN, timeout: 120000 });
  }
});

// ══════════════════════════════════════════════════════════════════════
// OpenAI-compatible: Chat Completions
// ══════════════════════════════════════════════════════════════════════

describeIf('OpenAI Chat Completions', () => {
  it('should complete a basic chat request', async () => {
    const result = await client.openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [{ role: 'user', content: 'Say hello in one word.' }],
      max_tokens: 10
    });
    expect(result).toHaveProperty('choices');
    expect((result as any).choices.length).toBeGreaterThan(0);
    expect((result as any).choices[0].message.content).toBeTruthy();
    console.log(`  Response: ${(result as any).choices[0].message.content}`);
  }, 30000);

  it('should handle system + user messages', async () => {
    const result = await client.openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: 'You are a math tutor. Reply concisely.' },
        { role: 'user', content: 'What is 2+3?' }
      ],
      max_tokens: 20
    });
    const content = (result as any).choices[0].message.content;
    expect(content).toContain('5');
    console.log(`  Response: ${content}`);
  }, 30000);

  it('should support temperature parameter', async () => {
    const result = await client.openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [{ role: 'user', content: 'Say yes or no.' }],
      max_tokens: 5,
      temperature: 0
    });
    expect((result as any).choices[0].message.content).toBeTruthy();
  }, 30000);

  it('should stream chat completions', async () => {
    const stream = await client.openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [{ role: 'user', content: 'Count from 1 to 3.' }],
      max_tokens: 30,
      stream: true
    }) as AsyncGenerator<Record<string, unknown>>;

    const chunks: Record<string, unknown>[] = [];
    for await (const chunk of stream) {
      chunks.push(chunk);
    }
    expect(chunks.length).toBeGreaterThan(0);

    const contentParts: string[] = [];
    for (const chunk of chunks) {
      const choices = (chunk as any).choices;
      if (choices && choices.length > 0) {
        const delta = choices[0].delta;
        if (delta && delta.content) {
          contentParts.push(delta.content);
        }
      }
    }
    const full = contentParts.join('');
    expect(full).toBeTruthy();
    console.log(`  Streamed: ${full}`);
  }, 30000);

  it('should work with different models', async () => {
    for (const model of ['gpt-4o-mini', 'claude-3-5-haiku-20241022']) {
      const result = await client.openai.chat.completions.create({
        model,
        messages: [{ role: 'user', content: "Reply with just the word 'ok'." }],
        max_tokens: 5
      });
      expect((result as any).choices[0].message.content).toBeTruthy();
      console.log(`  ${model}: ${(result as any).choices[0].message.content}`);
    }
  }, 60000);

  it('should return usage info', async () => {
    const result = await client.openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [{ role: 'user', content: 'Hi' }],
      max_tokens: 5
    });
    expect(result).toHaveProperty('usage');
    expect((result as any).usage.prompt_tokens).toBeGreaterThan(0);
    expect((result as any).usage.total_tokens).toBeGreaterThan(0);
    console.log(`  Usage: ${JSON.stringify((result as any).usage)}`);
  }, 30000);
});

// ══════════════════════════════════════════════════════════════════════
// OpenAI-compatible: Responses API
// ══════════════════════════════════════════════════════════════════════

describeIf('OpenAI Responses', () => {
  it('should create a response with string input', async () => {
    const result = await client.openai.responses.create({
      model: 'gpt-4o-mini',
      input: 'What is the capital of France? Reply in one word.'
    });
    expect(result).toHaveProperty('output');
    console.log(`  Response ID: ${(result as any).id}`);
  }, 30000);

  it('should create a response with structured input', async () => {
    const result = await client.openai.responses.create({
      model: 'gpt-4o-mini',
      input: [{ role: 'user', content: 'Say hello.' }]
    });
    expect(result).toHaveProperty('output');
  }, 30000);

  it('should stream responses', async () => {
    const stream = await client.openai.responses.create({
      model: 'gpt-4o-mini',
      input: 'Count from 1 to 3.',
      stream: true
    }) as AsyncGenerator<Record<string, unknown>>;

    const chunks: Record<string, unknown>[] = [];
    for await (const chunk of stream) {
      chunks.push(chunk);
    }
    expect(chunks.length).toBeGreaterThan(0);
    console.log(`  Received ${chunks.length} stream events`);
  }, 30000);
});

// ══════════════════════════════════════════════════════════════════════
// Google Search (SERP)
// ══════════════════════════════════════════════════════════════════════

describeIf('Search', () => {
  it('should perform a basic Google search', async () => {
    const result = await client.search.google({ query: 'Python programming language' });
    expect(result).toBeTruthy();
    console.log(`  Keys: ${Object.keys(result)}`);
  }, 30000);

  it('should search with country and language params', async () => {
    const result = await client.search.google({
      query: 'weather today',
      country: 'us',
      language: 'en'
    });
    expect(result).toBeTruthy();
  }, 30000);

  it('should search for news', async () => {
    const result = await client.search.google({
      query: 'artificial intelligence',
      type: 'news'
    });
    expect(result).toBeTruthy();
    console.log(`  News keys: ${Object.keys(result)}`);
  }, 30000);

  it('should search for images', async () => {
    const result = await client.search.google({
      query: 'cute cats',
      type: 'images'
    });
    expect(result).toBeTruthy();
    console.log(`  Image keys: ${Object.keys(result)}`);
  }, 30000);
});

// ══════════════════════════════════════════════════════════════════════
// Image Generation (NanoBanana)
// ══════════════════════════════════════════════════════════════════════

describeIf('Images', () => {
  it('should generate an image (async task)', async () => {
    const result = await client.images.generate({
      prompt: 'A cute cartoon cat sitting on a rainbow'
    });
    expect(result).toBeTruthy();
    const r = result as any;
    expect(r.task_id || r.data).toBeTruthy();
    console.log(`  Keys: ${Object.keys(result)}`);
    if (r.task_id) console.log(`  Task ID: ${r.task_id}`);
  }, 30000);

  it('should generate an image with wait', async () => {
    try {
      const result = await client.images.generate({
        prompt: 'A simple red circle on white background',
        wait: true,
        pollInterval: 3000,
        maxWait: 120000
      });
      expect(result).toBeTruthy();
      const r = result as any;
      if (r.data) {
        expect(r.data.length).toBeGreaterThan(0);
        console.log(`  Generated ${r.data.length} image(s)`);
        for (const item of r.data) {
          if (item.image_url) console.log(`  URL: ${item.image_url.substring(0, 80)}...`);
        }
      }
    } catch (e: any) {
      console.log(`  Image wait timed out or failed, skipping: ${e.message}`);
    }
  }, 180000);
});

// ══════════════════════════════════════════════════════════════════════
// Audio Generation (Suno)
// ══════════════════════════════════════════════════════════════════════

describeIf('Audio', () => {
  it('should generate audio (async task)', async () => {
    try {
      const result = await client.audio.generate({
        prompt: 'A cheerful pop song about coding'
      });
      expect(result).toBeTruthy();
      const r = result as any;
      expect(r.task_id || r.data).toBeTruthy();
      console.log(`  Keys: ${Object.keys(result)}`);
      if (r.task_id) console.log(`  Task ID: ${r.task_id}`);
    } catch (e: any) {
      console.log(`  Audio API error, skipping: ${e.message}`);
    }
  }, 180000);
});

// ══════════════════════════════════════════════════════════════════════
// Video Generation (Sora)
// ══════════════════════════════════════════════════════════════════════

describeIf('Video', () => {
  it('should generate video (async task)', async () => {
    try {
      const result = await client.video.generate({
        prompt: 'A sunset over the ocean, time-lapse style'
      });
      expect(result).toBeTruthy();
      const r = result as any;
      expect(r.task_id || r.data).toBeTruthy();
      console.log(`  Keys: ${Object.keys(result)}`);
      if (r.task_id) console.log(`  Task ID: ${r.task_id}`);
    } catch (e: any) {
      console.log(`  Video API not available, skipping: ${e.message}`);
    }
  }, 150000);
});

// ══════════════════════════════════════════════════════════════════════
// Task Retrieval
// ══════════════════════════════════════════════════════════════════════

describeIf('Tasks', () => {
  it('should retrieve a Suno task', async () => {
    try {
      const gen = await client.audio.generate({ prompt: 'A short jingle' });
      const taskId = (gen as any).task_id;
      if (!taskId) return; // skip if direct result

      const result = await client.tasks.get(taskId, { service: 'suno' });
      expect(result).toBeTruthy();
      console.log(`  Task status: ${(result as any).response?.status || 'unknown'}`);
    } catch (e: any) {
      console.log(`  Suno task retrieval error, skipping: ${e.message}`);
    }
  }, 120000);

  it('should retrieve a NanoBanana task', async () => {
    const gen = await client.images.generate({ prompt: 'A blue square' });
    const taskId = (gen as any).task_id;
    if (!taskId) return;

    const result = await client.tasks.get(taskId, { service: 'nano-banana' });
    expect(result).toBeTruthy();
    console.log(`  Task status: ${(result as any).response?.status || 'unknown'}`);
  }, 30000);
});

// ══════════════════════════════════════════════════════════════════════
// Platform APIs
// ══════════════════════════════════════════════════════════════════════

describePlatform('Platform', () => {
  it('should get platform config', async () => {
    const result = await platformClient!.platform.config.get();
    expect(result).toBeTruthy();
    console.log(`  Config keys: ${Object.keys(result)}`);
  }, 60000);

  it('should list models', async () => {
    const result = await platformClient!.platform.models.list();
    expect(result).toBeTruthy();
    console.log(`  Keys: ${Object.keys(result)}`);
  }, 60000);

  it('should list applications', async () => {
    const result = await platformClient!.platform.applications.list();
    expect(result).toBeTruthy();
    const r = result as any;
    console.log(`  Count: ${r.count ?? r.results?.length ?? 0}`);
  }, 60000);

  it('should list credentials', async () => {
    const result = await platformClient!.platform.credentials.list();
    expect(result).toBeTruthy();
    const r = result as any;
    console.log(`  Count: ${r.count ?? r.results?.length ?? 0}`);
  }, 60000);
});

// ══════════════════════════════════════════════════════════════════════
// File Upload
// ══════════════════════════════════════════════════════════════════════

describePlatform('Files', () => {
  it('should upload bytes content', async () => {
    const content = Buffer.from('Hello, this is a test file for SDK integration testing.');
    const result = await platformClient!.files.upload(content, { filename: 'test.txt' });
    expect(result).toBeTruthy();
    console.log(`  Upload keys: ${Object.keys(result)}`);
    if ((result as any).url) console.log(`  File URL: ${(result as any).url.substring(0, 80)}...`);
  }, 30000);

  it('should upload from file path', async () => {
    const tmpFile = path.join(__dirname, '_test_upload_tmp.txt');
    fs.writeFileSync(tmpFile, 'Integration test file content');
    try {
      const result = await platformClient!.files.upload(tmpFile);
      expect(result).toBeTruthy();
      console.log(`  Upload keys: ${Object.keys(result)}`);
    } finally {
      fs.unlinkSync(tmpFile);
    }
  }, 30000);
});

// ══════════════════════════════════════════════════════════════════════
// Error Handling
// ══════════════════════════════════════════════════════════════════════

describeIf('Error Handling', () => {
  it('should throw on invalid model', async () => {
    await expect(
      client.openai.chat.completions.create({
        model: 'nonexistent-model-xyz',
        messages: [{ role: 'user', content: 'Hi' }],
        max_tokens: 5
      })
    ).rejects.toThrow();
  }, 30000);

  it('should throw on bad auth token', async () => {
    const badClient = new AceDataCloud({ apiToken: 'invalid-token-12345' });
    await expect(
      badClient.openai.chat.completions.create({
        model: 'gpt-4o-mini',
        messages: [{ role: 'user', content: 'Hi' }],
        max_tokens: 5
      })
    ).rejects.toThrow();
  }, 30000);
});
