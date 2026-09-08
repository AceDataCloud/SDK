/**
 * Localization (localization) — generated from the platform OpenAPI spec.
 *
 * Do not edit by hand: run `python scripts/generate_providers.py`. Parameter
 * names, types, enums and required-ness all come from the live spec.
 */

import { Transport } from '../../runtime/transport';


export interface LocalizationTranslateOptions {
  /** Localization Translate Input */
  input: string | Record<string, unknown>;
  /** Localization Translate Locale */
  locale: "en" | "de" | "pt" | "es" | "fr" | "zh-CN" | "zh-TW" | "it" | "ko" | "ja" | "ru" | "pl" | "fi" | "sv" | "el" | "uk" | "ar" | "sr";
  /** Localization Translate Extension */
  extension: "md" | "json";
  /** Localization Translate Model */
  model?: "gpt-3.5" | "gpt-4";
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

/** localization client. */
export class Localization {
  constructor(private transport: Transport) {}

  /** Translate a JSON input into any localized file */
  async translate(options: LocalizationTranslateOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["input"] = options.input;
    body["locale"] = options.locale;
    body["extension"] = options.extension;
    if (options.model !== undefined) body["model"] = options.model;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "extension", "input", "locale", "maxWait", "model", "pollInterval", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/localization/translate", { json: body })) as Record<string, unknown>;
  }

}
