// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"


// Localization is the localization provider client.
type Localization struct {
	t *transport
}

// LocalizationTranslateRequest is the input to localization.Translate.
type LocalizationTranslateRequest struct {
	// Please provide the content that needs to be translated.
	Input map[string]any
	// The target language area to be translated to.
	Locale string
	// The file type of the input text (such as `json` or `md`).
	Extension string
	// The large language model used for translation is `gpt-3.5` by default.
	Model string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r LocalizationTranslateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["input"] = r.Input
	body["locale"] = r.Locale
	body["extension"] = r.Extension
	if r.Model != "" {
		body["model"] = r.Model
	}
	if r.CallbackURL != "" {
		body["callback_url"] = r.CallbackURL
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// Translate Translate a JSON input into any localized file
func (c *Localization) Translate(ctx context.Context, req LocalizationTranslateRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/localization/translate",
		Body:   req.toBody(),
	})
}
