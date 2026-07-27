package acedatacloud

import (
	"context"
	"fmt"
	"strconv"
	"strings"
	"time"
)

// TaskHandle represents a long-running async task (image/audio/video
// generation) that can be polled until completion.
type TaskHandle struct {
	ID           string
	pollEndpoint string
	transport    *transport
	last         map[string]any
	done         bool
}

// newTaskHandle builds a handle. When the submission already carried the
// artifact (some endpoints answer synchronously), the handle is born complete
// so Wait returns immediately instead of polling for something already here.
func newTaskHandle(id, pollEndpoint string, tr *transport, submitted map[string]any) *TaskHandle {
	h := &TaskHandle{ID: id, pollEndpoint: pollEndpoint, transport: tr}
	if submitted != nil && len(ArtifactURLs(map[string]any{"response": submitted})) > 0 {
		h.last = map[string]any{"response": submitted}
		h.done = true
	}
	return h
}

// Done reports whether the task has already reached a terminal state.
func (h *TaskHandle) Done() bool { return h.done }

// URLs returns the artifact URLs once the task has completed.
func (h *TaskHandle) URLs() []string { return ArtifactURLs(h.last) }

// Progress returns percent complete, or nil when the service does not report it.
func (h *TaskHandle) Progress() *int { return TaskProgress(h.last) }

// Get fetches the current task state from the server.
func (h *TaskHandle) Get(ctx context.Context) (map[string]any, error) {
	state, err := h.transport.do(ctx, requestOpts{
		Method: "POST",
		Path:   h.pollEndpoint,
		Body:   map[string]any{"id": h.ID, "action": "retrieve"},
	})
	if err != nil {
		return nil, err
	}
	h.last = state
	return state, nil
}

// IsCompleted reports whether the task has reached a terminal state
// (“succeeded“ or “failed“). Returns true together with the error
// if the network call fails.
func (h *TaskHandle) IsCompleted(ctx context.Context) (bool, error) {
	state, err := h.Get(ctx)
	if err != nil {
		return false, err
	}
	return terminalStatus(state), nil
}

// Result returns the last observed server response, or nil if Get was
// never called.
func (h *TaskHandle) Result() map[string]any { return h.last }

// Wait polls until the task completes or maxWait elapses.
func (h *TaskHandle) Wait(ctx context.Context, pollInterval, maxWait time.Duration) (map[string]any, error) {
	if pollInterval <= 0 {
		pollInterval = 3 * time.Second
	}
	if maxWait <= 0 {
		maxWait = 10 * time.Minute
	}
	if h.done {
		return h.last, nil
	}
	deadline := time.Now().Add(maxWait)
	for {
		state, err := h.Get(ctx)
		if err != nil {
			return nil, err
		}
		if terminalStatus(state) {
			h.done = true
			return state, nil
		}
		if time.Now().After(deadline) {
			return nil, &TimeoutError{&APIError{
				Message: fmt.Sprintf("task %s did not complete within %s", h.ID, maxWait),
				ErrCode: "task_timeout",
			}}
		}
		select {
		case <-ctx.Done():
			return nil, ctx.Err()
		case <-time.After(pollInterval):
		}
	}
}

var doneWords = map[string]bool{
	"succeed": true, "succeeded": true, "success": true,
	"completed": true, "complete": true, "finished": true,
}

var failedWords = map[string]bool{
	"failed": true, "failure": true, "error": true,
	"cancelled": true, "canceled": true, "rejected": true,
}

// terminalStatus reports whether a poll response describes a finished task.
//
// Services report completion inconsistently — a status word, a state word
// spelled differently, only a finished_at timestamp, or merely the artifact URL
// appearing. Matching Python and TypeScript here matters: this used to accept
// only `status`, so a Go caller polling a service that reports `state: succeed`
// waited forever. A status word outranks the success flag, since a response can
// carry success:false for a retryable hiccup while the task still runs.
func terminalStatus(state map[string]any) bool {
	status := taskStatus(state)
	return status == "succeeded" || status == "failed"
}

// taskStatus reduces a poll response to "succeeded", "failed" or "" (running).
func taskStatus(state map[string]any) string {
	resp := state
	if r, ok := state["response"].(map[string]any); ok {
		resp = r
	}

	words := statusWords(resp, 0)
	for _, w := range words {
		if failedWords[w] {
			return "failed"
		}
	}
	for _, w := range words {
		if doneWords[w] {
			// A terminal word with no artifact means the job produced nothing.
			if len(ArtifactURLs(state)) > 0 {
				return "succeeded"
			}
			return "failed"
		}
	}
	if len(words) > 0 {
		return "" // queued, processing, … — keep waiting
	}

	_, finishedInResp := resp["finished_at"]
	_, finishedInState := state["finished_at"]
	if finishedInResp || finishedInState {
		if ok, _ := resp["success"].(bool); ok {
			return "succeeded"
		}
		if v, present := resp["success"]; present {
			if b, isBool := v.(bool); isBool && !b {
				return "failed"
			}
		}
		if len(ArtifactURLs(state)) > 0 {
			return "succeeded"
		}
	}

	if len(ArtifactURLs(state)) > 0 {
		return "succeeded"
	}
	return ""
}

func statusWords(node any, depth int) []string {
	if depth > 6 {
		return nil
	}
	var out []string
	switch v := node.(type) {
	case map[string]any:
		for key, value := range v {
			if s, ok := value.(string); ok && (key == "state" || key == "status") {
				out = append(out, strings.ToLower(s))
			} else {
				out = append(out, statusWords(value, depth+1)...)
			}
		}
	case []any:
		for _, item := range v {
			out = append(out, statusWords(item, depth+1)...)
		}
	}
	return out
}

// ArtifactURLs returns every artifact URL in a task response.
//
// Where the artifact lives is not derivable from the OpenAPI spec — response is
// typed as a bare object and the key differs per service (video_url, image_url,
// data[].image_url). Rather than keep a per-service table that goes stale,
// collect anything URL-shaped.
func ArtifactURLs(state map[string]any) []string {
	if state == nil {
		return nil
	}
	var node any = state
	if r, ok := state["response"]; ok {
		node = r
	}
	var found []string
	collectURLs(node, &found, 0)

	seen := map[string]bool{}
	var out []string
	for _, u := range found {
		if !seen[u] {
			seen[u] = true
			out = append(out, u)
		}
	}
	return out
}

func collectURLs(node any, out *[]string, depth int) {
	if depth > 6 {
		return
	}
	switch v := node.(type) {
	case map[string]any:
		for key, value := range v {
			s, isString := value.(string)
			looksLikeURL := strings.HasSuffix(key, "_url") || key == "url" || strings.HasSuffix(key, "_urls")
			if isString && looksLikeURL && strings.HasPrefix(s, "http") {
				*out = append(*out, s)
			} else {
				collectURLs(value, out, depth+1)
			}
		}
	case []any:
		for _, item := range v {
			collectURLs(item, out, depth+1)
		}
	}
}

// TaskProgress returns percent complete when the service reports it.
//
// A nil return means unknown — a caller rendering a bar should show "working"
// rather than a bar stuck at zero, which reads as broken.
func TaskProgress(state map[string]any) *int {
	if state == nil {
		return nil
	}
	var node any = state
	if r, ok := state["response"]; ok {
		node = r
	}
	for _, value := range findKeys(node, []string{"progress", "percent", "percentage"}, 0) {
		switch v := value.(type) {
		case bool:
			continue
		case float64:
			pct := int(v)
			if v > 0 && v <= 1 {
				pct = int(v * 100)
			}
			pct = clampPercent(pct)
			return &pct
		case int:
			pct := clampPercent(v)
			return &pct
		case string:
			trimmed := strings.TrimSuffix(strings.TrimSpace(v), "%")
			if f, err := strconv.ParseFloat(trimmed, 64); err == nil {
				pct := clampPercent(int(f))
				return &pct
			}
		}
	}
	return nil
}

func clampPercent(v int) int {
	if v < 0 {
		return 0
	}
	if v > 100 {
		return 100
	}
	return v
}

func findKeys(node any, names []string, depth int) []any {
	if depth > 6 {
		return nil
	}
	var out []any
	switch v := node.(type) {
	case map[string]any:
		for key, value := range v {
			matched := false
			for _, n := range names {
				if key == n {
					matched = true
					break
				}
			}
			if matched {
				out = append(out, value)
			} else {
				out = append(out, findKeys(value, names, depth+1)...)
			}
		}
	case []any:
		for _, item := range v {
			out = append(out, findKeys(item, names, depth+1)...)
		}
	}
	return out
}

// FailureReason returns the upstream's own words for why a task failed.
func FailureReason(state map[string]any) string {
	if state == nil {
		return "Task failed."
	}
	resp := state
	if r, ok := state["response"].(map[string]any); ok {
		resp = r
	}
	switch e := resp["error"].(type) {
	case map[string]any:
		for _, key := range []string{"message", "detail"} {
			if s, ok := e[key].(string); ok && s != "" {
				return s
			}
		}
	case string:
		if e != "" {
			return e
		}
	}
	for _, key := range []string{"message", "failure_reason", "fail_reason"} {
		if s, ok := resp[key].(string); ok && s != "" {
			return s
		}
	}
	return "Task failed."
}
