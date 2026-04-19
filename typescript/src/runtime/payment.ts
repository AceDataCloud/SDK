/**
 * Pluggable payment handler hook for the SDK transport.
 *
 * When the API returns `402 Payment Required`, the transport calls the
 * configured `PaymentHandler` to produce the extra headers (typically
 * `X-Payment`) to attach to the retry. This keeps the SDK free of any
 * chain-specific signing logic, and lets callers plug in a real x402
 * implementation such as `@acedatacloud/x402-client`.
 */

/** Payment requirement as returned by the server in a 402 response. */
export interface PaymentRequirement {
  scheme: string;
  network: string;
  maxAmountRequired: string;
  maxTimeoutSeconds?: number;
  resource?: string;
  description?: string;
  payTo: string;
  asset: string;
  extra?: Record<string, unknown>;
}

/** Shape of a 402 response body. */
export interface PaymentRequiredBody {
  x402Version?: number;
  accepts: PaymentRequirement[];
  error?: string;
}

/** Context passed to a payment handler when a 402 is observed. */
export interface PaymentHandlerContext {
  url: string;
  method: string;
  body?: unknown;
  accepts: PaymentRequirement[];
}

/** Result a payment handler must return. */
export interface PaymentHandlerResult {
  /** Extra headers to attach to the retry (must include `X-Payment`). */
  headers: Record<string, string>;
}

/** A callable that signs/settles a payment and returns retry headers. */
export type PaymentHandler = (
  ctx: PaymentHandlerContext
) => Promise<PaymentHandlerResult> | PaymentHandlerResult;
