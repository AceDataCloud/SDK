package acedatacloud

import "context"

// CaptchaResource exposes captcha recognition and token endpoints.
type CaptchaResource struct {
	recognition *CaptchaRecognitionResource
	token       *CaptchaTokenResource
}

// Recognition returns captcha recognition endpoints.
func (r *CaptchaResource) Recognition() *CaptchaRecognitionResource { return r.recognition }

// Token returns captcha token endpoints.
func (r *CaptchaResource) Token() *CaptchaTokenResource { return r.token }

// CaptchaRecognitionResource exposes captcha recognition endpoints.
type CaptchaRecognitionResource struct{ t *transport }

// CaptchaTokenResource exposes captcha token endpoints.
type CaptchaTokenResource struct{ t *transport }

// HCaptchaRecognitionRequest is the request body for /captcha/recognition/hcaptcha.
type HCaptchaRecognitionRequest struct {
	Queries  []string
	Question string
	Async    bool
	Extra    map[string]any
}

// HCaptchaTokenRequest is the request body for /captcha/token/hcaptcha.
type HCaptchaTokenRequest struct {
	WebsiteKey string
	WebsiteURL string
	Rqdata     string
	Proxy      string
	Async      bool
	Extra      map[string]any
}

// HCaptcha submits an hCaptcha recognition request.
func (r *CaptchaRecognitionResource) HCaptcha(ctx context.Context, req HCaptchaRecognitionRequest) (*TaskHandle, map[string]any, error) {
	body := map[string]any{"async": req.Async}
	if req.Queries != nil {
		body["queries"] = req.Queries
	}
	if req.Question != "" {
		body["question"] = req.Question
	}
	mergeExtra(body, req.Extra)
	result, err := r.t.do(ctx, requestOpts{Method: "POST", Path: "/captcha/recognition/hcaptcha", Body: body})
	if err != nil || !req.Async {
		return nil, result, err
	}
	handle := newTaskHandleWithPoll(taskIDFrom(result), "/captcha/tasks", r.t, result, "task_id", nil)
	return handle, result, nil
}

// HCaptcha submits an hCaptcha token request.
func (r *CaptchaTokenResource) HCaptcha(ctx context.Context, req HCaptchaTokenRequest) (*TaskHandle, map[string]any, error) {
	body := map[string]any{
		"website_key": req.WebsiteKey,
		"website_url": req.WebsiteURL,
		"async":       req.Async,
	}
	if req.Rqdata != "" {
		body["rqdata"] = req.Rqdata
	}
	if req.Proxy != "" {
		body["proxy"] = req.Proxy
	}
	mergeExtra(body, req.Extra)
	result, err := r.t.do(ctx, requestOpts{Method: "POST", Path: "/captcha/token/hcaptcha", Body: body})
	if err != nil || !req.Async {
		return nil, result, err
	}
	handle := newTaskHandleWithPoll(taskIDFrom(result), "/captcha/tasks", r.t, result, "task_id", nil)
	return handle, result, nil
}

func mergeExtra(body map[string]any, extra map[string]any) {
	for k, v := range extra {
		if _, ok := body[k]; !ok {
			body[k] = v
		}
	}
}
