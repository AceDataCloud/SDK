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

// CaptchaRecognitionImage2TextRequest is the input to recognition.image2text.
type CaptchaRecognitionImage2TextRequest struct {
	Image string
	Async bool
	Extra map[string]any
}

func (r *CaptchaRecognitionImage2TextRequest) toBody() map[string]any {
	body := map[string]any{
		"image": r.Image,
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

// Image2Text calls POST /captcha/recognition/image2text.
func (r *CaptchaRecognition) Image2Text(ctx context.Context, req CaptchaRecognitionImage2TextRequest) (map[string]any, error) {
	return r.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/captcha/recognition/image2text",
		Body:   req.toBody(),
	})
}

// CaptchaRecognitionRecaptcha2Request is the input to recognition.recaptcha2.
type CaptchaRecognitionRecaptcha2Request struct {
	Image    string
	Question string
	Async    bool
	Extra    map[string]any
}

func (r *CaptchaRecognitionRecaptcha2Request) toBody() map[string]any {
	body := map[string]any{
		"image":    r.Image,
		"question": r.Question,
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

// Recaptcha2 calls POST /captcha/recognition/recaptcha2.
func (r *CaptchaRecognition) Recaptcha2(ctx context.Context, req CaptchaRecognitionRecaptcha2Request) (map[string]any, error) {
	return r.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/captcha/recognition/recaptcha2",
		Body:   req.toBody(),
	})
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

// CaptchaTokenRecaptcha2Request is the input to token.recaptcha2.
type CaptchaTokenRecaptcha2Request struct {
	WebsiteKey string
	WebsiteURL string
	Proxy      string
	Async      bool
	Extra      map[string]any
}

func (r *CaptchaTokenRecaptcha2Request) toBody() map[string]any {
	body := map[string]any{
		"website_key": r.WebsiteKey,
		"website_url": r.WebsiteURL,
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

// Recaptcha2 calls POST /captcha/token/recaptcha2.
func (r *CaptchaToken) Recaptcha2(ctx context.Context, req CaptchaTokenRecaptcha2Request) (map[string]any, error) {
	return r.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/captcha/token/recaptcha2",
		Body:   req.toBody(),
	})
}

// CaptchaTokenRecaptcha3Request is the input to token.recaptcha3.
type CaptchaTokenRecaptcha3Request struct {
	PageAction string
	WebsiteKey string
	WebsiteURL string
	Async      bool
	Extra      map[string]any
}

func (r *CaptchaTokenRecaptcha3Request) toBody() map[string]any {
	body := map[string]any{
		"page_action": r.PageAction,
		"website_key": r.WebsiteKey,
		"website_url": r.WebsiteURL,
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

// Recaptcha3 calls POST /captcha/token/recaptcha3.
func (r *CaptchaToken) Recaptcha3(ctx context.Context, req CaptchaTokenRecaptcha3Request) (map[string]any, error) {
	return r.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/captcha/token/recaptcha3",
		Body:   req.toBody(),
	})
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
