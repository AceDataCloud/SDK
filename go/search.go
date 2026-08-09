package acedatacloud

import "context"

type SearchType string

const (
	SearchTypeSearch SearchType = "search"
	SearchTypeImages SearchType = "images"
	SearchTypeNews   SearchType = "news"
	SearchTypeMaps   SearchType = "maps"
	SearchTypePlaces SearchType = "places"
	SearchTypeVideos SearchType = "videos"
)

type SearchRange string

const (
	SearchRangeHour  SearchRange = "h"
	SearchRangeDay   SearchRange = "d"
	SearchRangeWeek  SearchRange = "w"
	SearchRangeMonth SearchRange = "m"
	SearchRangeYear  SearchRange = "y"
	SearchRangeQdrH  SearchRange = "qdr:h"
	SearchRangeQdrD  SearchRange = "qdr:d"
	SearchRangeQdrW  SearchRange = "qdr:w"
	SearchRangeQdrM  SearchRange = "qdr:m"
	SearchRangeQdrY  SearchRange = "qdr:y"
)

type SearchImageSize string

const (
	SearchImageSizeLarge  SearchImageSize = "large"
	SearchImageSizeMedium SearchImageSize = "medium"
	SearchImageSizeIcon   SearchImageSize = "icon"
	SearchImageSize2MP    SearchImageSize = "2mp"
	SearchImageSize4MP    SearchImageSize = "4mp"
	SearchImageSize6MP    SearchImageSize = "6mp"
	SearchImageSize8MP    SearchImageSize = "8mp"
	SearchImageSize10MP   SearchImageSize = "10mp"
	SearchImageSize12MP   SearchImageSize = "12mp"
	SearchImageSize15MP   SearchImageSize = "15mp"
	SearchImageSize20MP   SearchImageSize = "20mp"
	SearchImageSize40MP   SearchImageSize = "40mp"
	SearchImageSize70MP   SearchImageSize = "70mp"
)

// SearchRequest is the input to search.Google.
type SearchRequest struct {
	// Query is the required search query.
	Query string
	// Type selects the SERP type: "search" (default), "images", "news", etc.
	Type SearchType
	// Country and Language are optional localization hints.
	Country  string
	Language string
	// Page is the optional 1-based result page.
	Page int
	// Range limits results recency.
	Range SearchRange
	// Number is the requested result count.
	Number int
	// ImageSize filters image search results by size.
	ImageSize SearchImageSize
	// Extra fields merged into the request body.
	Extra map[string]any
}

// SearchResource groups web search endpoints (“/serp/google“).
type SearchResource struct{ t *transport }

// Google performs a blocking Google search.
func (s *SearchResource) Google(ctx context.Context, req SearchRequest) (map[string]any, error) {
	typ := string(req.Type)
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
	if req.Range != "" {
		body["range"] = req.Range
	}
	if req.Number > 0 {
		body["number"] = req.Number
	}
	if req.ImageSize != "" {
		body["image_size"] = req.ImageSize
	}
	for k, v := range req.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return s.t.do(ctx, requestOpts{Method: "POST", Path: "/serp/google", Body: body})
}
