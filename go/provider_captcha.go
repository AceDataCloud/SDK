package acedatacloud

import "context"

// Captcha is the captcha provider client.
type Captcha struct {
	t *transport
}

// CaptchaRecognitionHcaptchaRequest is the input to captcha.RecognitionHcaptcha.
type CaptchaRecognitionHcaptchaRequest struct {
	// Base64-encoded challenge image tiles.
	Queries []string
	// The challenge question text.
	Question string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r CaptchaRecognitionHcaptchaRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Queries != nil {
		body["queries"] = r.Queries
	}
	if r.Question != "" {
		body["question"] = r.Question
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// RecognitionHcaptcha solves an hCaptcha image recognition challenge.
func (c *Captcha) RecognitionHcaptcha(ctx context.Context, req CaptchaRecognitionHcaptchaRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/captcha/recognition/hcaptcha",
		Body:   req.toBody(),
	})
}

// CaptchaTokenHcaptchaRequest is the input to captcha.TokenHcaptcha.
type CaptchaTokenHcaptchaRequest struct {
	// The site key of the hCaptcha widget.
	WebsiteKey string
	// The URL of the page with the hCaptcha widget.
	WebsiteURL string
	// Optional HTTP(S) proxy string.
	Proxy string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r CaptchaTokenHcaptchaRequest) toBody() map[string]any {
	body := map[string]any{}
	body["website_key"] = r.WebsiteKey
	body["website_url"] = r.WebsiteURL
	if r.Proxy != "" {
		body["proxy"] = r.Proxy
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// TokenHcaptcha solves an hCaptcha token challenge.
func (c *Captcha) TokenHcaptcha(ctx context.Context, req CaptchaTokenHcaptchaRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/captcha/token/hcaptcha",
		Body:   req.toBody(),
	})
}

// CaptchaTasksRequest is the input to captcha.Tasks.
type CaptchaTasksRequest struct {
	// Task ID returned by a prior request.
	TaskID string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r CaptchaTasksRequest) toBody() map[string]any {
	body := map[string]any{}
	body["task_id"] = r.TaskID
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// Tasks retrieves a captcha task result.
func (c *Captcha) Tasks(ctx context.Context, req CaptchaTasksRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/captcha/tasks",
		Body:   req.toBody(),
	})
}
