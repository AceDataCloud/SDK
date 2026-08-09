package acedatacloud

import (
	"context"
	"fmt"
	"strings"
)

// SearchType is a supported Google SERP result type.
type SearchType string

const (
	SearchTypeSearch SearchType = "search"
	SearchTypeImages SearchType = "images"
	SearchTypeNews   SearchType = "news"
	SearchTypeMaps   SearchType = "maps"
	SearchTypePlaces SearchType = "places"
	SearchTypeVideos SearchType = "videos"
)

// SearchRange is a supported Google SERP recency filter.
type SearchRange string

const (
	SearchRangeHour     SearchRange = "h"
	SearchRangeDay      SearchRange = "d"
	SearchRangeWeek     SearchRange = "w"
	SearchRangeMonth    SearchRange = "m"
	SearchRangeYear     SearchRange = "y"
	SearchRangeQDRHour  SearchRange = "qdr:h"
	SearchRangeQDRDay   SearchRange = "qdr:d"
	SearchRangeQDRWeek  SearchRange = "qdr:w"
	SearchRangeQDRMonth SearchRange = "qdr:m"
	SearchRangeQDRYear  SearchRange = "qdr:y"
)

// ImageSize is a supported Google Images size filter.
type ImageSize string

const (
	ImageSizeLarge  ImageSize = "large"
	ImageSizeMedium ImageSize = "medium"
	ImageSizeIcon   ImageSize = "icon"
	ImageSize2MP    ImageSize = "2mp"
	ImageSize4MP    ImageSize = "4mp"
	ImageSize6MP    ImageSize = "6mp"
	ImageSize8MP    ImageSize = "8mp"
	ImageSize10MP   ImageSize = "10mp"
	ImageSize12MP   ImageSize = "12mp"
	ImageSize15MP   ImageSize = "15mp"
	ImageSize20MP   ImageSize = "20mp"
	ImageSize40MP   ImageSize = "40mp"
	ImageSize70MP   ImageSize = "70mp"
)

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
	// Range is the optional result recency filter.
	Range SearchRange
	// Number is the optional number of results to return.
	Number int
	// ImageSize filters image results by size.
	ImageSize ImageSize
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
	if err := validateSearchRequest(req, typ); err != nil {
		return nil, err
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

func validateSearchRequest(req SearchRequest, typ string) error {
	if len(req.Query) < 1 || len(req.Query) > 2048 || strings.TrimSpace(req.Query) == "" {
		return fmt.Errorf("query must be 1 to 2048 characters and contain at least one non-whitespace character")
	}
	if !isSearchType(typ) {
		return fmt.Errorf("unsupported search type: %s", typ)
	}
	if req.Page < 0 || req.Page > 100 {
		return fmt.Errorf("page must be between 1 and 100")
	}
	if req.Number < 0 || req.Number > 100 {
		return fmt.Errorf("number must be between 1 and 100")
	}
	if req.Range != "" && !isSearchRange(req.Range) {
		return fmt.Errorf("unsupported search range: %s", req.Range)
	}
	if (len(req.Country) > 0 && len(req.Country) > 32) || (len(req.Language) > 0 && len(req.Language) > 32) {
		return fmt.Errorf("country and language must be 1 to 32 characters")
	}
	if req.ImageSize != "" && !isImageSize(req.ImageSize) {
		return fmt.Errorf("unsupported image size: %s", req.ImageSize)
	}
	if req.ImageSize != "" && typ != string(SearchTypeImages) {
		return fmt.Errorf("image_size is only valid when type is %q", SearchTypeImages)
	}
	return nil
}

func isSearchType(value string) bool {
	switch SearchType(value) {
	case SearchTypeSearch, SearchTypeImages, SearchTypeNews, SearchTypeMaps, SearchTypePlaces, SearchTypeVideos:
		return true
	}
	return false
}

func isSearchRange(value SearchRange) bool {
	switch value {
	case SearchRangeHour, SearchRangeDay, SearchRangeWeek, SearchRangeMonth, SearchRangeYear, SearchRangeQDRHour, SearchRangeQDRDay, SearchRangeQDRWeek, SearchRangeQDRMonth, SearchRangeQDRYear:
		return true
	}
	return false
}

func isImageSize(value ImageSize) bool {
	switch value {
	case ImageSizeLarge, ImageSizeMedium, ImageSizeIcon, ImageSize2MP, ImageSize4MP, ImageSize6MP, ImageSize8MP, ImageSize10MP, ImageSize12MP, ImageSize15MP, ImageSize20MP, ImageSize40MP, ImageSize70MP:
		return true
	}
	return false
}
