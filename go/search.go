package acedatacloud

import "context"

// SearchRequest is the input to search.Google.
type SearchRequest struct {
	// Query is the required search query.
	Query string
	// Type selects the SERP type: "search" (default), "images", "news", etc.
	Type string
	// Country and Language are optional localization hints.
	Country  string
	Language string
	// Page is the optional 1-based result page.
	Page int
	// Extra fields merged into the request body.
	Extra map[string]any
}

// SearchResource groups web search endpoints (“/serp/google“).
type SearchResource struct{ t *transport }

// Google performs a blocking Google search.
func (s *SearchResource) Google(ctx context.Context, req SearchRequest) (map[string]any, error) {
	typ := req.Type
	if typ == "" {
		typ = "search"
	}
	body := map[string]any{"query": req.Query, "type": typ}
	if req.Country != "" {
		body["country"] = req.Country
	}
	if req.Language != "" {
		body["language"] = req.Language
	}
	if req.Page > 0 {
		body["page"] = req.Page
	}
	for k, v := range req.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return s.t.do(ctx, requestOpts{Method: "POST", Path: "/serp/google", Body: body})
}
