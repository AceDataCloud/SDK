package acedatacloud

import (
	"context"
	"net/url"
	"strconv"
)

// DiscordResource provides access to the Discord Agent Proxy API.
type DiscordResource struct{ t *transport }

func (r *DiscordResource) request(ctx context.Context, method, path string, body any, query url.Values) (map[string]any, error) {
	return r.t.do(ctx, requestOpts{Method: method, Path: path, Body: body, Query: query})
}
func (r *DiscordResource) Whoami(ctx context.Context) (map[string]any, error) {
	return r.request(ctx, "GET", "/api/whoami", nil, nil)
}
func (r *DiscordResource) Guilds(ctx context.Context) (map[string]any, error) {
	return r.request(ctx, "GET", "/api/guilds", nil, nil)
}
func (r *DiscordResource) CreateChannel(ctx context.Context, guildID, name string) (map[string]any, error) {
	return r.request(ctx, "POST", "/api/guilds/"+guildID+"/channels", map[string]any{"name": name}, nil)
}
func (r *DiscordResource) Members(ctx context.Context, guildID string, limit *int) (map[string]any, error) {
	q := url.Values{}
	if limit != nil {
		q.Set("limit", strconv.Itoa(*limit))
	}
	return r.request(ctx, "GET", "/api/guilds/"+guildID+"/members", nil, q)
}
func (r *DiscordResource) SendMessage(ctx context.Context, channelID, content, replyTo string) (map[string]any, error) {
	b := map[string]any{"channel_id": channelID, "content": content}
	if replyTo != "" {
		b["reply_to"] = replyTo
	}
	return r.request(ctx, "POST", "/api/messages", b, nil)
}
func (r *DiscordResource) Messages(ctx context.Context, channelID string, limit *int) (map[string]any, error) {
	q := url.Values{}
	if limit != nil {
		q.Set("limit", strconv.Itoa(*limit))
	}
	return r.request(ctx, "GET", "/api/channels/"+channelID+"/messages", nil, q)
}
func (r *DiscordResource) SearchMessages(ctx context.Context, channelID, q string, limit *int) (map[string]any, error) {
	v := url.Values{"q": {q}}
	if limit != nil {
		v.Set("limit", strconv.Itoa(*limit))
	}
	return r.request(ctx, "GET", "/api/channels/"+channelID+"/messages/search", nil, v)
}
func (r *DiscordResource) DeleteMessage(ctx context.Context, channelID, messageID string) (map[string]any, error) {
	return r.request(ctx, "DELETE", "/api/channels/"+channelID+"/messages/"+messageID, nil, nil)
}
func (r *DiscordResource) AddReaction(ctx context.Context, channelID, messageID, emoji string) (map[string]any, error) {
	return r.request(ctx, "POST", "/api/channels/"+channelID+"/messages/"+messageID+"/reactions", map[string]any{"emoji": emoji}, nil)
}
func (r *DiscordResource) PinMessage(ctx context.Context, channelID, messageID string) (map[string]any, error) {
	return r.request(ctx, "POST", "/api/channels/"+channelID+"/messages/"+messageID+"/pin", nil, nil)
}
func (r *DiscordResource) CreateDM(ctx context.Context, recipientID string) (map[string]any, error) {
	return r.request(ctx, "POST", "/api/dms", map[string]any{"recipient_id": recipientID}, nil)
}
func (r *DiscordResource) SendDM(ctx context.Context, recipientID, content string) (map[string]any, error) {
	return r.request(ctx, "POST", "/api/dms/send", map[string]any{"recipient_id": recipientID, "content": content}, nil)
}
