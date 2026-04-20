package acedatacloud

import (
	"context"
	"time"
)

var serviceTaskEndpoints = map[string]string{
	"suno":        "/suno/tasks",
	"producer":    "/producer/tasks",
	"fish":        "/fish/tasks",
	"nano-banana": "/nano-banana/tasks",
	"seedream":    "/seedream/tasks",
	"seedance":    "/seedance/tasks",
	"sora":        "/sora/tasks",
	"midjourney":  "/midjourney/tasks",
	"luma":        "/luma/tasks",
	"veo":         "/veo/tasks",
	"flux":        "/flux/tasks",
	"kling":       "/kling/tasks",
	"hailuo":      "/hailuo/tasks",
	"wan":         "/wan/tasks",
	"pika":        "/pika/tasks",
	"pixverse":    "/pixverse/tasks",
}

// TasksResource groups cross-service task retrieval operations.
type TasksResource struct{ t *transport }

// Get fetches a single task snapshot.
func (r *TasksResource) Get(ctx context.Context, service, taskID string) (map[string]any, error) {
	endpoint := endpointFor(service)
	return r.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   endpoint,
		Body:   map[string]any{"id": taskID, "action": "retrieve"},
	})
}

// Wait polls a task until it reaches a terminal state or maxWait elapses.
func (r *TasksResource) Wait(ctx context.Context, service, taskID string, pollInterval, maxWait time.Duration) (map[string]any, error) {
	handle := &TaskHandle{
		ID:           taskID,
		pollEndpoint: endpointFor(service),
		transport:    r.t,
	}
	return handle.Wait(ctx, pollInterval, maxWait)
}

func endpointFor(service string) string {
	if ep, ok := serviceTaskEndpoints[service]; ok {
		return ep
	}
	return "/" + service + "/tasks"
}
