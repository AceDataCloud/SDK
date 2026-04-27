package acedatacloud

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"math"
	"math/rand"
	"net/http"
	"net/url"
	"os"
	"strings"
	"time"
)

// Transport performs authenticated HTTP requests to the AceDataCloud API.
type transport struct {
	opts       *options
	httpClient *http.Client
	headers    map[string]string
}

var retryStatus = map[int]bool{408: true, 409: true, 429: true, 500: true, 502: true, 503: true, 504: true}

func newTransport(opts *options) (*transport, error) {
	token := opts.apiToken
	if token == "" {
		token = os.Getenv("ACEDATACLOUD_API_TOKEN")
	}
	if token == "" && opts.paymentHandler == nil {
		return nil, &AuthenticationError{&APIError{
			Message: "api_token is required (or provide a PaymentHandler). Pass WithAPIToken or set ACEDATACLOUD_API_TOKEN.",
			ErrCode: "no_token",
		}}
	}

	client := opts.httpClient
	if client == nil {
		client = &http.Client{Timeout: opts.timeout}
	}

	h := map[string]string{
		"Accept":       "application/json",
		"Content-Type": "application/json",
		"User-Agent":   userAgent,
	}
	for k, v := range opts.extraHeaders {
		h[k] = v
	}
	if token != "" {
		h["Authorization"] = "Bearer " + token
	}

	return &transport{opts: opts, httpClient: client, headers: h}, nil
}

// requestOpts describes a single API call.
type requestOpts struct {
	Method       string
	Path         string
	Body         any
	Query        url.Values
	Platform     bool
	ExtraHeaders map[string]string
}

func backoff(attempt int) time.Duration {
	base := math.Min(math.Pow(2, float64(attempt)), 8)
	//nolint:gosec // non-crypto jitter
	jitter := rand.Float64() * 0.5
	return time.Duration((base + jitter) * float64(time.Second))
}

// do executes a JSON request and parses a JSON map response.
func (t *transport) do(ctx context.Context, r requestOpts) (map[string]any, error) {
	base := t.opts.baseURL
	if r.Platform {
		base = t.opts.platformURL
	}
	fullURL := base + r.Path
	if len(r.Query) > 0 {
		fullURL += "?" + r.Query.Encode()
	}

	var bodyBytes []byte
	if r.Body != nil {
		var err error
		bodyBytes, err = json.Marshal(r.Body)
		if err != nil {
			return nil, fmt.Errorf("marshal body: %w", err)
		}
	}

	extraAuth := map[string]string{}
	paymentAttempted := false

	var lastErr error
	for attempt := 0; attempt <= t.opts.maxRetries; attempt++ {
		req, err := http.NewRequestWithContext(ctx, r.Method, fullURL, bytes.NewReader(bodyBytes))
		if err != nil {
			return nil, fmt.Errorf("build request: %w", err)
		}
		for k, v := range t.headers {
			req.Header.Set(k, v)
		}
		for k, v := range r.ExtraHeaders {
			req.Header.Set(k, v)
		}
		for k, v := range extraAuth {
			req.Header.Set(k, v)
		}

		resp, err := t.httpClient.Do(req)
		if err != nil {
			if errors.Is(err, context.Canceled) || errors.Is(err, context.DeadlineExceeded) {
				return nil, &TimeoutError{&APIError{Message: err.Error(), ErrCode: "timeout"}}
			}
			lastErr = &TransportError{&APIError{Message: err.Error()}}
			if attempt < t.opts.maxRetries {
				time.Sleep(backoff(attempt))
				continue
			}
			return nil, lastErr
		}

		respBody, _ := io.ReadAll(resp.Body)
		_ = resp.Body.Close()

		// Handle 402 Payment Required: invoke handler once, then retry with new headers.
		if resp.StatusCode == http.StatusPaymentRequired && t.opts.paymentHandler != nil && !paymentAttempted {
			var parsed map[string]any
			if err := json.Unmarshal(respBody, &parsed); err != nil {
				return nil, mapError(402, map[string]any{"error": map[string]any{"code": "invalid_402", "message": string(respBody)}})
			}
			rawAccepts, _ := parsed["accepts"].([]any)
			if len(rawAccepts) == 0 {
				return nil, mapError(402, map[string]any{"error": map[string]any{"code": "invalid_402", "message": "No payment requirements"}})
			}
			accepts := make([]PaymentRequirement, 0, len(rawAccepts))
			for _, a := range rawAccepts {
				if m, ok := a.(map[string]any); ok {
					accepts = append(accepts, m)
				}
			}
			pctx := PaymentContext{URL: fullURL, Method: r.Method, Body: r.Body, Accepts: accepts}
			result, err := t.opts.paymentHandler.Handle(ctx, pctx)
			if err != nil {
				return nil, fmt.Errorf("payment handler: %w", err)
			}
			for k, v := range result.Headers {
				extraAuth[k] = v
			}
			paymentAttempted = true
			continue
		}

		if resp.StatusCode >= 400 {
			parsed := map[string]any{}
			if err := json.Unmarshal(respBody, &parsed); err != nil {
				parsed = map[string]any{"error": map[string]any{"code": "unknown", "message": string(respBody)}}
			}
			if retryStatus[resp.StatusCode] && attempt < t.opts.maxRetries {
				time.Sleep(backoff(attempt))
				continue
			}
			return nil, mapError(resp.StatusCode, parsed)
		}

		parsed := map[string]any{}
		if len(respBody) > 0 {
			if err := json.Unmarshal(respBody, &parsed); err != nil {
				return nil, fmt.Errorf("parse response: %w", err)
			}
		}
		return parsed, nil
	}

	if lastErr != nil {
		return nil, lastErr
	}
	return nil, &TransportError{&APIError{Message: "request failed after retries"}}
}

// stream executes a POST and yields SSE data chunks via the returned channel.
// The channel is closed when the stream ends or an error occurs; errors are
// reported via the returned error channel.
func (t *transport) stream(ctx context.Context, path string, body any) (<-chan []byte, <-chan error) {
	out := make(chan []byte)
	errCh := make(chan error, 1)

	go func() {
		defer close(out)
		defer close(errCh)

		fullURL := t.opts.baseURL + path
		var bodyBytes []byte
		if body != nil {
			var err error
			bodyBytes, err = json.Marshal(body)
			if err != nil {
				errCh <- err
				return
			}
		}

		req, err := http.NewRequestWithContext(ctx, http.MethodPost, fullURL, bytes.NewReader(bodyBytes))
		if err != nil {
			errCh <- err
			return
		}
		for k, v := range t.headers {
			req.Header.Set(k, v)
		}
		req.Header.Set("Accept", "text/event-stream")

		resp, err := t.httpClient.Do(req)
		if err != nil {
			errCh <- err
			return
		}
		defer resp.Body.Close()

		if resp.StatusCode >= 400 {
			respBody, _ := io.ReadAll(resp.Body)
			parsed := map[string]any{}
			if e := json.Unmarshal(respBody, &parsed); e != nil {
				parsed = map[string]any{"error": map[string]any{"code": "unknown", "message": string(respBody)}}
			}
			errCh <- mapError(resp.StatusCode, parsed)
			return
		}

		reader := resp.Body
		buf := make([]byte, 0, 4096)
		tmp := make([]byte, 4096)
		for {
			n, err := reader.Read(tmp)
			if n > 0 {
				buf = append(buf, tmp[:n]...)
				for {
					idx := bytes.IndexByte(buf, '\n')
					if idx < 0 {
						break
					}
					line := strings.TrimRight(string(buf[:idx]), "\r")
					buf = buf[idx+1:]
					if !strings.HasPrefix(line, "data: ") {
						continue
					}
					data := strings.TrimPrefix(line, "data: ")
					if data == "[DONE]" {
						return
					}
					select {
					case out <- []byte(data):
					case <-ctx.Done():
						return
					}
				}
			}
			if err != nil {
				if err != io.EOF {
					errCh <- err
				}
				return
			}
		}
	}()

	return out, errCh
}
