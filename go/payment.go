package acedatacloud

import "context"

// PaymentRequirement describes a single entry in the server's 402 ``accepts`` list.
//
// Using map[string]any keeps the SDK free of chain-specific types — the
// companion x402-client package is responsible for interpreting the
// ``extra`` field and producing an ``X-Payment`` envelope.
type PaymentRequirement = map[string]any

// PaymentContext is passed to a PaymentHandler when the transport
// receives a 402 Payment Required response.
type PaymentContext struct {
	URL     string
	Method  string
	Body    any
	Accepts []PaymentRequirement
}

// PaymentResult is what a PaymentHandler must return: the headers to
// attach to the retried request (typically ``X-Payment``).
type PaymentResult struct {
	Headers map[string]string
}

// PaymentHandler is the hook the SDK calls on 402. Implementations
// typically sign an EIP-3009 authorization (EVM) or submit a
// TransferChecked transaction (Solana) and return an ``X-Payment``
// header.
type PaymentHandler interface {
	Handle(ctx context.Context, pctx PaymentContext) (PaymentResult, error)
}

// PaymentHandlerFunc adapts a plain function into a PaymentHandler.
type PaymentHandlerFunc func(ctx context.Context, pctx PaymentContext) (PaymentResult, error)

// Handle implements PaymentHandler.
func (f PaymentHandlerFunc) Handle(ctx context.Context, pctx PaymentContext) (PaymentResult, error) {
	return f(ctx, pctx)
}
