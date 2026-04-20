package acedatacloud

import (
	"context"
	"fmt"
	"time"
)

// TaskHandle represents a long-running async task (image/audio/video
// generation) that can be polled until completion.
type TaskHandle struct {
	ID           string
	pollEndpoint string
	transport    *transport
	last         map[string]any
}

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
// (``succeeded`` or ``failed``). Returns true together with the error
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
	deadline := time.Now().Add(maxWait)
	for {
		state, err := h.Get(ctx)
		if err != nil {
			return nil, err
		}
		if terminalStatus(state) {
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

func terminalStatus(state map[string]any) bool {
	resp := state
	if r, ok := state["response"].(map[string]any); ok {
		resp = r
	}
	status, _ := resp["status"].(string)
	return status == "succeeded" || status == "failed"
}
