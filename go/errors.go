package acedatacloud

import "fmt"

// Error is the base interface for all typed SDK errors.
type Error interface {
	error
	StatusCode() int
	Code() string
	TraceID() string
	Body() map[string]any
}

// APIError is returned for API-level errors.
type APIError struct {
	Message    string
	Status     int
	ErrCode    string
	Trace      string
	RawBody    map[string]any
	Underlying error
}

func (e *APIError) Error() string {
	if e.Trace != "" {
		return fmt.Sprintf("acedatacloud: %s (status=%d code=%s trace_id=%s)", e.Message, e.Status, e.ErrCode, e.Trace)
	}
	return fmt.Sprintf("acedatacloud: %s (status=%d code=%s)", e.Message, e.Status, e.ErrCode)
}

func (e *APIError) Unwrap() error         { return e.Underlying }
func (e *APIError) StatusCode() int       { return e.Status }
func (e *APIError) Code() string          { return e.ErrCode }
func (e *APIError) TraceID() string       { return e.Trace }
func (e *APIError) Body() map[string]any  { return e.RawBody }

// Typed error wrappers. All embed *APIError.
type (
	AuthenticationError     struct{ *APIError }
	TokenMismatchError      struct{ *APIError }
	PermissionError         struct{ *APIError }
	RateLimitError          struct{ *APIError }
	ValidationError         struct{ *APIError }
	InsufficientBalanceError struct{ *APIError }
	ResourceDisabledError   struct{ *APIError }
	ModerationError         struct{ *APIError }
	TimeoutError            struct{ *APIError }
	InternalServerError     struct{ *APIError }
	TransportError          struct{ *APIError }
)

// mapError converts an HTTP status code + parsed body into a typed error.
func mapError(status int, body map[string]any) error {
	var (
		code    string
		message string
		trace   string
	)
	trace, _ = body["trace_id"].(string)

	// "error" may be a dict, string, or missing — normalize.
	switch v := body["error"].(type) {
	case map[string]any:
		code, _ = v["code"].(string)
		message, _ = v["message"].(string)
	case string:
		message = v
	}

	base := &APIError{
		Message: message,
		Status:  status,
		ErrCode: code,
		Trace:   trace,
		RawBody: body,
	}

	switch code {
	case "invalid_token", "token_expired", "no_token":
		return &AuthenticationError{base}
	case "token_mismatched":
		return &TokenMismatchError{base}
	case "used_up":
		return &InsufficientBalanceError{base}
	case "disabled":
		return &ResourceDisabledError{base}
	case "too_many_requests":
		return &RateLimitError{base}
	case "bad_request":
		return &ValidationError{base}
	}

	switch status {
	case 401:
		return &AuthenticationError{base}
	case 403:
		return &ModerationError{base}
	case 429:
		return &RateLimitError{base}
	case 400:
		return &ValidationError{base}
	}
	return base
}
