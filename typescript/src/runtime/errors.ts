/** AceDataCloud SDK errors. */

export class AceDataCloudError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'AceDataCloudError';
  }
}

export class TransportError extends AceDataCloudError {
  constructor(message: string) {
    super(message);
    this.name = 'TransportError';
  }
}

export class APIError extends AceDataCloudError {
  statusCode: number;
  code: string;
  traceId?: string;
  body: Record<string, unknown>;

  constructor(opts: {
    message: string;
    statusCode: number;
    code: string;
    traceId?: string;
    body?: Record<string, unknown>;
  }) {
    super(opts.message);
    this.name = 'APIError';
    this.statusCode = opts.statusCode;
    this.code = opts.code;
    this.traceId = opts.traceId;
    this.body = opts.body ?? {};
  }
}

export class AuthenticationError extends APIError {
  constructor(opts: ConstructorParameters<typeof APIError>[0]) {
    super(opts);
    this.name = 'AuthenticationError';
  }
}

export class TokenMismatchError extends APIError {
  constructor(opts: ConstructorParameters<typeof APIError>[0]) {
    super(opts);
    this.name = 'TokenMismatchError';
  }
}

export class RateLimitError extends APIError {
  constructor(opts: ConstructorParameters<typeof APIError>[0]) {
    super(opts);
    this.name = 'RateLimitError';
  }
}

export class ValidationError extends APIError {
  constructor(opts: ConstructorParameters<typeof APIError>[0]) {
    super(opts);
    this.name = 'ValidationError';
  }
}

export class InsufficientBalanceError extends APIError {
  constructor(opts: ConstructorParameters<typeof APIError>[0]) {
    super(opts);
    this.name = 'InsufficientBalanceError';
  }
}

export class ResourceDisabledError extends APIError {
  constructor(opts: ConstructorParameters<typeof APIError>[0]) {
    super(opts);
    this.name = 'ResourceDisabledError';
  }
}

export class ModerationError extends APIError {
  constructor(opts: ConstructorParameters<typeof APIError>[0]) {
    super(opts);
    this.name = 'ModerationError';
  }
}

export class TimeoutError extends APIError {
  constructor(opts: ConstructorParameters<typeof APIError>[0]) {
    super(opts);
    this.name = 'TimeoutError';
  }
}
