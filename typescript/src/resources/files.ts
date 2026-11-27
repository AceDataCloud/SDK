/** File upload resources. */

import { Transport } from '../runtime/transport';
import * as fs from 'fs';
import * as path from 'path';

export class Files {
  constructor(private transport: Transport) {}

  async upload(
    file: string | Buffer | Uint8Array,
    opts: { filename?: string } = {}
  ): Promise<Record<string, unknown>> {
    let data: Buffer | Uint8Array;
    let filename: string;

    if (typeof file === 'string') {
      data = fs.readFileSync(file);
      filename = opts.filename ?? path.basename(file);
    } else {
      data = file;
      filename = opts.filename ?? 'upload';
    }

    return this.transport.upload('/api/v1/files/', data, filename);
  }
}
