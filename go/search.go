package acedatacloud

import (
	"context"
	"fmt"
	"strings"
	"unicode/utf8"
)

// SearchRange restricts Google results by recency.
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

// SearchImageSize selects an image size filter.
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
	Type string
	// Country and Language are optional localization hints.
	Country  string
	Language string
	// Page and Number default to 1 and 10.
	Page   int
	Number int
	// Range and ImageSize are optional filters.
	Range     SearchRange
	ImageSize SearchImageSize
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r SearchRequest) toBody() (map[string]any, error) {
	if strings.TrimSpace(r.Query) == "" || utf8.RuneCountInString(r.Query) > 2048 {
		return nil, fmt.Errorf("query must contain 1 to 2048 characters and cannot be blank")
	}
	page := r.Page
	if page == 0 {
		page = 1
	}
	if page < 1 || page > 100 {
		return nil, fmt.Errorf("page must be between 1 and 100")
	}
	number := r.Number
	if number == 0 {
		number = 10
	}
	if number < 1 || number > 100 {
		return nil, fmt.Errorf("number must be between 1 and 100")
	}
	if r.Country != "" {
		length := utf8.RuneCountInString(r.Country)
		if length < 1 || length > 32 {
			return nil, fmt.Errorf("country must contain 1 to 32 characters")
		}
	}
	if r.Language != "" {
		length := utf8.RuneCountInString(r.Language)
		if length < 1 || length > 32 {
			return nil, fmt.Errorf("language must contain 1 to 32 characters")
		}
	}
	if r.Range != "" && !validSearchRange(r.Range) {
		return nil, fmt.Errorf("range is invalid")
	}
	if r.ImageSize != "" && !validSearchImageSize(r.ImageSize) {
		return nil, fmt.Errorf("image size is invalid")
	}

	typ := r.Type
	if typ == "" {
		typ = "search"
	}
	body := map[string]any{
		"query":  r.Query,
		"type":   typ,
		"page":   page,
		"number": number,
	}
	if r.Country != "" {
		body["country"] = r.Country
	}
	if r.Language != "" {
		body["language"] = r.Language
	}
	if r.Range != "" {
		body["range"] = string(r.Range)
	}
	if r.ImageSize != "" {
		body["image_size"] = string(r.ImageSize)
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body, nil
}

func validSearchRange(value SearchRange) bool {
	switch value {
	case SearchRangeHour, SearchRangeDay, SearchRangeWeek, SearchRangeMonth, SearchRangeYear,
		SearchRangeQDRHour, SearchRangeQDRDay, SearchRangeQDRWeek, SearchRangeQDRMonth, SearchRangeQDRYear:
		return true
	default:
		return false
	}
}

func validSearchImageSize(value SearchImageSize) bool {
	switch value {
	case SearchImageSizeLarge, SearchImageSizeMedium, SearchImageSizeIcon, SearchImageSize2MP,
		SearchImageSize4MP, SearchImageSize6MP, SearchImageSize8MP, SearchImageSize10MP,
		SearchImageSize12MP, SearchImageSize15MP, SearchImageSize20MP, SearchImageSize40MP,
		SearchImageSize70MP:
		return true
	default:
		return false
	}
}

// SearchResource groups web search endpoints (“/serp/google“).
type SearchResource struct{ t *transport }

// Google performs a blocking Google search.
func (s *SearchResource) Google(ctx context.Context, req SearchRequest) (map[string]any, error) {
	body, err := req.toBody()
	if err != nil {
		return nil, err
	}
	return s.t.do(ctx, requestOpts{Method: "POST", Path: "/serp/google", Body: body})
}
