/** Top-level AceDataCloud client for TypeScript. */

import { Transport, TransportOptions } from './runtime/transport';
import type { PaymentHandler } from './runtime/payment';
import { AiChat } from './resources/aichat';
import { Chat } from './resources/chat';
import { Images } from './resources/images';
import { Audio } from './resources/audio';
import { Video } from './resources/video';
import { Search } from './resources/search';
import { Tasks } from './resources/tasks';
import { Files } from './resources/files';
import { Platform } from './resources/platform';
import { OpenAI } from './resources/openai';
import { Glm } from './resources/glm';
import { Veo } from './resources/veo';
import { Kling } from './resources/kling';
import { WebExtrator } from './resources/webextrator';
import { Suno } from './resources/suno';

export interface AceDataCloudOptions {
  apiToken?: string;
  baseURL?: string;
  platformBaseURL?: string;
  timeout?: number;
  maxRetries?: number;
  headers?: Record<string, string>;
  /**
   * Optional payment handler invoked when the API returns `402 Payment
   * Required`. Use `createX402PaymentHandler` from
   * `@acedatacloud/x402-client` to enable on-chain payments via X402.
   */
  paymentHandler?: PaymentHandler;
}

export class AceDataCloud {
  readonly aichat: AiChat;
  readonly chat: Chat;
  readonly images: Images;
  readonly audio: Audio;
  readonly video: Video;
  readonly search: Search;
  readonly tasks: Tasks;
  readonly files: Files;
  readonly platform: Platform;
  readonly openai: OpenAI;
  readonly glm: Glm;
  readonly veo: Veo;
  readonly kling: Kling;
  readonly webextrator: WebExtrator;
  readonly suno: Suno;

  private transport: Transport;

  constructor(opts: AceDataCloudOptions = {}) {
    this.transport = new Transport({
      apiToken: opts.apiToken,
      baseURL: opts.baseURL,
      platformBaseURL: opts.platformBaseURL,
      timeout: opts.timeout,
      maxRetries: opts.maxRetries,
      headers: opts.headers,
      paymentHandler: opts.paymentHandler,
    });

    this.aichat = new AiChat(this.transport);
    this.chat = new Chat(this.transport);
    this.images = new Images(this.transport);
    this.audio = new Audio(this.transport);
    this.video = new Video(this.transport);
    this.search = new Search(this.transport);
    this.tasks = new Tasks(this.transport);
    this.files = new Files(this.transport);
    this.platform = new Platform(this.transport);
    this.openai = new OpenAI(this.transport);
    this.glm = new Glm(this.transport);
    this.veo = new Veo(this.transport);
    this.kling = new Kling(this.transport);
    this.webextrator = new WebExtrator(this.transport);
    this.suno = new Suno(this.transport);
  }
}
