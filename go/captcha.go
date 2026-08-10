package acedatacloud

import "context"

// CaptchaResource groups captcha endpoints (“/captcha/*“).
type CaptchaResource struct{ t *transport }

// Recognition returns the captcha recognition namespace.
func (c *CaptchaResource) Recognition() *CaptchaRecognition { return &CaptchaRecognition{t: c.t} }

// Token returns the captcha token namespace.
func (c *CaptchaResource) Token() *CaptchaToken { return &CaptchaToken{t: c.t} }

// Tasks returns the captcha tasks namespace.
func (c *CaptchaResource) Tasks() *CaptchaTasks { return &CaptchaTasks{t: c.t} }

// CaptchaRecognition exposes captcha recognition endpoints.
type CaptchaRecognition struct{ t *transport }

// CaptchaRecognitionHCaptchaRequest is the input to recognition.hcaptcha.
type CaptchaRecognitionHCaptchaRequest struct {
	Queries  []string
	Question string
	Async    bool
	Extra    map[string]any
}

func (r *CaptchaRecognitionHCaptchaRequest) toBody() map[string]any {
	body := map[string]any{}
	if len(r.Queries) > 0 {
		body["queries"] = r.Queries
	}
	if r.Question != "" {
		body["question"] = r.Question
	}
	if r.Async {
		body["async"] = true
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// HCaptcha calls POST /captcha/recognition/hcaptcha.
func (r *CaptchaRecognition) HCaptcha(ctx context.Context, req CaptchaRecognitionHCaptchaRequest) (map[string]any, error) {
	return r.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/captcha/recognition/hcaptcha",
		Body:   req.toBody(),
	})
}

// Recaptcha2 calls POST /captcha/recognition/recaptcha2.
func (r *CaptchaRecognition) Recaptcha2(ctx context.Context, image, question string, extra map[string]any) (map[string]any, error) {
	body := map[string]any{"image": image, "question": question}
	for k, v := range extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return r.t.do(ctx, requestOpts{Method: "POST", Path: "/captcha/recognition/recaptcha2", Body: body})
}

// CaptchaToken exposes captcha token endpoints.
type CaptchaToken struct{ t *transport }

// CaptchaTokenHCaptchaRequest is the input to token.hcaptcha.
type CaptchaTokenHCaptchaRequest struct {
	WebsiteKey string
	WebsiteURL string
	RQData     string
	Proxy      string
	Async      bool
	Extra      map[string]any
}

func (r *CaptchaTokenHCaptchaRequest) toBody() map[string]any {
	body := map[string]any{
		"website_key": r.WebsiteKey,
		"website_url": r.WebsiteURL,
	}
	if r.RQData != "" {
		body["rqdata"] = r.RQData
	}
	if r.Proxy != "" {
		body["proxy"] = r.Proxy
	}
	if r.Async {
		body["async"] = true
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// HCaptcha calls POST /captcha/token/hcaptcha.
func (r *CaptchaToken) HCaptcha(ctx context.Context, req CaptchaTokenHCaptchaRequest) (map[string]any, error) {
	return r.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/captcha/token/hcaptcha",
		Body:   req.toBody(),
	})
}

// Recaptcha2 calls POST /captcha/token/recaptcha2.
func (r *CaptchaToken) Recaptcha2(ctx context.Context, websiteKey, websiteURL string, extra map[string]any) (map[string]any, error) {
	body := map[string]any{"website_key": websiteKey, "website_url": websiteURL}
	for k, v := range extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return r.t.do(ctx, requestOpts{Method: "POST", Path: "/captcha/token/recaptcha2", Body: body})
}

// Recaptcha3 calls POST /captcha/token/recaptcha3.
func (r *CaptchaToken) Recaptcha3(ctx context.Context, websiteKey, websiteURL, pageAction string, extra map[string]any) (map[string]any, error) {
	body := map[string]any{"website_key": websiteKey, "website_url": websiteURL, "page_action": pageAction}
	for k, v := range extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return r.t.do(ctx, requestOpts{Method: "POST", Path: "/captcha/token/recaptcha3", Body: body})
}

// CaptchaTasks exposes captcha task retrieval.
type CaptchaTasks struct{ t *transport }

// Retrieve calls POST /captcha/tasks.
func (r *CaptchaTasks) Retrieve(ctx context.Context, taskID string, extra map[string]any) (map[string]any, error) {
	body := map[string]any{"task_id": taskID}
	for k, v := range extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return r.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/captcha/tasks",
		Body:   body,
	})
}
