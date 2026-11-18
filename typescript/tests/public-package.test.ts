import { execFileSync } from 'child_process';
import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from 'fs';
import { tmpdir } from 'os';
import { join, resolve } from 'path';

it('exposes typed ACE Music requests through the built package root', () => {
  const root = resolve(__dirname, '..');
  const temporary = mkdtempSync(join(tmpdir(), 'acedatacloud-public-package-'));
  try {
    execFileSync(process.execPath, [join(root, 'node_modules/tsup/dist/cli-default.js')], {
      cwd: root,
      stdio: 'pipe',
    });
    const packed = JSON.parse(execFileSync('npm', [
      'pack', '--ignore-scripts', '--json', '--pack-destination', temporary,
    ], { cwd: root, encoding: 'utf8' }))[0] as { filename: string };
    const installed = join(temporary, 'node_modules/@acedatacloud/sdk');
    mkdirSync(installed, { recursive: true });
    execFileSync('tar', [
      '-xzf', join(temporary, packed.filename), '-C', installed, '--strip-components=1',
    ]);
    const consumer = join(temporary, 'consumer.ts');
    writeFileSync(consumer, `
      import {
        AceDataCloud, Acemusic,
        type AcemusicGenerateOptions, type AcemusicLyricsOptions, type AcemusicTasksOptions,
      } from '@acedatacloud/sdk';
      const client = new AceDataCloud({ apiToken: 'offline' });
      const provider: Acemusic = client.acemusic;
      const upload: AcemusicGenerateOptions = {
        action: 'upload', audioUrl: 'https://example.test/owned.mp3', audioId: 'owned-anchor',
      };
      const cover: AcemusicGenerateOptions = {
        action: 'cover', audioId: 'owned-one', lyric: '[Verse] Offline', style: 'pop', audioInfluence: 60,
      };
      const mashup: AcemusicGenerateOptions = {
        action: 'mashup', mashupAudioIds: ['owned-one', 'owned-two'], lyric: '[Verse] Offline', style: 'pop',
      };
      const lyrics: AcemusicLyricsOptions = { prompt: 'Offline lyrics' };
      const tasks: AcemusicTasksOptions = { action: 'retrieve', id: 'existing-task' };
      void provider.generate(upload);
      void client.acemusic.generate(cover);
      void client.acemusic.generate(mashup);
      void provider.lyrics(lyrics);
      void provider.tasks(tasks);
      // @ts-expect-error Reference action names remain a closed union.
      const invalid: AcemusicGenerateOptions = { action: 'unsupported' };
      void invalid;
    `);
    execFileSync(process.execPath, [
      join(root, 'node_modules/typescript/bin/tsc'),
      '--noEmit', '--strict', '--skipLibCheck', '--target', 'ES2020',
      '--moduleResolution', 'node', '--module', 'commonjs', consumer,
    ], { cwd: temporary, stdio: 'pipe' });
  } finally {
    rmSync(temporary, { recursive: true, force: true });
  }
}, 60_000);
