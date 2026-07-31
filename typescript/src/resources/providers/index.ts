/** Provider-axis clients, generated from the platform OpenAPI specs. */

export { Captcha } from './captcha';
export { Digitalhuman } from './digitalhuman';
export { DrawAI } from './drawai';
export { Dreamina } from './dreamina';
export { Fish } from './fish';
export { Flux } from './flux';
export { Gemini } from './gemini';
export { Grok } from './grok';
export { Hailuo } from './hailuo';
export { Happyhorse } from './happyhorse';
export { Localization } from './localization';
export { Luma } from './luma';
export { Maestro } from './maestro';
export { Midjourney } from './midjourney';
export { NanoBanana } from './nano-banana';
export { Producer } from './producer';
export { QRart } from './qrart';
export { Seedance } from './seedance';
export { Seedream } from './seedream';
export { Sora } from './sora';
export { Suno } from './suno';
export { Wan } from './wan';

import { Transport } from '../../runtime/transport';
import { Captcha } from './captcha';
import { Digitalhuman } from './digitalhuman';
import { DrawAI } from './drawai';
import { Dreamina } from './dreamina';
import { Fish } from './fish';
import { Flux } from './flux';
import { Gemini } from './gemini';
import { Grok } from './grok';
import { Hailuo } from './hailuo';
import { Happyhorse } from './happyhorse';
import { Localization } from './localization';
import { Luma } from './luma';
import { Maestro } from './maestro';
import { Midjourney } from './midjourney';
import { NanoBanana } from './nano-banana';
import { Producer } from './producer';
import { QRart } from './qrart';
import { Seedance } from './seedance';
import { Seedream } from './seedream';
import { Sora } from './sora';
import { Suno } from './suno';
import { Wan } from './wan';

/** Bind every generated provider client onto `client`. */
export function attachProviders(client: Record<string, unknown>, transport: Transport): void {
  client.captcha = new Captcha(transport);
  client.digitalhuman = new Digitalhuman(transport);
  client.drawai = new DrawAI(transport);
  client.dreamina = new Dreamina(transport);
  client.fish = new Fish(transport);
  client.flux = new Flux(transport);
  client.gemini = new Gemini(transport);
  client.grok = new Grok(transport);
  client.hailuo = new Hailuo(transport);
  client.happyhorse = new Happyhorse(transport);
  client.localization = new Localization(transport);
  client.luma = new Luma(transport);
  client.maestro = new Maestro(transport);
  client.midjourney = new Midjourney(transport);
  client.nanobanana = new NanoBanana(transport);
  client.producer = new Producer(transport);
  client.qrart = new QRart(transport);
  client.seedance = new Seedance(transport);
  client.seedream = new Seedream(transport);
  client.sora = new Sora(transport);
  client.suno = new Suno(transport);
  client.wan = new Wan(transport);
}
