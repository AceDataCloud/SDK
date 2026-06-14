/** ADSL Direct Connection Proxy resources. */

import { Transport } from '../runtime/transport';

export class Adsl {
  constructor(private transport: Transport) {}

  async extract(opts: {
    isp?: '电信' | '联通' | '移动' | (string & {});
    city?: string;
    type?: 'http' | 'socks';
    dedup?: boolean;
    number?: number;
    duration?: 60 | 180 | 300;
    province?: string;
    [key: string]: unknown;
  } = {}): Promise<Record<string, unknown>> {
    const { isp, city, type, dedup, number, duration, province, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (isp !== undefined) body.isp = isp;
    if (city !== undefined) body.city = city;
    if (type !== undefined) body.type = type;
    if (dedup !== undefined) body.dedup = dedup;
    if (number !== undefined) body.number = number;
    if (duration !== undefined) body.duration = duration;
    if (province !== undefined) body.province = province;
    return this.transport.request('POST', '/adsl/extract', { json: body });
  }

  async whitelist(opts: {
    ip?: string;
    action?: 'add' | 'delete';
    [key: string]: unknown;
  } = {}): Promise<Record<string, unknown>> {
    const { ip, action, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (ip !== undefined) body.ip = ip;
    if (action !== undefined) body.action = action;
    return this.transport.request('POST', '/adsl/whitelist', { json: body });
  }
}
