package acedatacloud

import (
	"net/http"
	"time"
)

const (
	defaultAPIBase      = "https://api.acedata.cloud"
	defaultPlatformBase = "https://platform.acedata.cloud"
	defaultTimeout      = 300 * time.Second
	defaultMaxRetries   = 2
	userAgent           = "acedatacloud-go/0.1.0"
)

// Option configures a Client.
type Option func(*options)

type options struct {
	apiToken       string
	baseURL        string
	platformURL    string
	timeout        time.Duration
	maxRetries     int
	extraHeaders   map[string]string
	paymentHandler PaymentHandler
	httpClient     *http.Client
}

func defaultOptions() *options {
	return &options{
		baseURL:      defaultAPIBase,
		platformURL:  defaultPlatformBase,
		timeout:      defaultTimeout,
		maxRetries:   defaultMaxRetries,
		extraHeaders: map[string]string{},
	}
}

// WithAPIToken sets the Bearer token. If omitted, the SDK reads
// ``ACEDATACLOUD_API_TOKEN`` from the environment.
func WithAPIToken(token string) Option { return func(o *options) { o.apiToken = token } }

// WithBaseURL overrides the API gateway base URL.
func WithBaseURL(url string) Option { return func(o *options) { o.baseURL = url } }

// WithPlatformURL overrides the management plane base URL.
func WithPlatformURL(url string) Option { return func(o *options) { o.platformURL = url } }

// WithTimeout sets the per-request timeout.
func WithTimeout(d time.Duration) Option { return func(o *options) { o.timeout = d } }

// WithMaxRetries sets the number of retry attempts for transient errors.
func WithMaxRetries(n int) Option { return func(o *options) { o.maxRetries = n } }

// WithHeaders adds static headers to every request.
func WithHeaders(h map[string]string) Option {
	return func(o *options) {
		for k, v := range h {
			o.extraHeaders[k] = v
		}
	}
}

// WithPaymentHandler installs a handler invoked on 402 Payment Required.
func WithPaymentHandler(h PaymentHandler) Option {
	return func(o *options) { o.paymentHandler = h }
}

// WithHTTPClient overrides the underlying *http.Client.
func WithHTTPClient(c *http.Client) Option {
	return func(o *options) { o.httpClient = c }
}
