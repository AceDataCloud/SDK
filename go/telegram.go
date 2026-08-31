package acedatacloud

import (
	"context"
	"net/url"
	"strconv"
)

// TelegramResource provides access to the Telegram Account Proxy API.
type TelegramResource struct{ t *transport }

func (r *TelegramResource) request(ctx context.Context, method, path string, body any, query url.Values) (map[string]any, error) {
	return r.t.do(ctx, requestOpts{Method: method, Path: path, Body: body, Query: query})
}
func (r *TelegramResource) CreateQR(ctx context.Context) (map[string]any, error) {
	return r.request(ctx, "POST", "/api/auth/qr", nil, nil)
}
func (r *TelegramResource) AuthStatus(ctx context.Context) (map[string]any, error) {
	return r.request(ctx, "GET", "/api/auth/status", nil, nil)
}
func (r *TelegramResource) SubmitPassword(ctx context.Context, password string) (map[string]any, error) {
	return r.request(ctx, "POST", "/api/auth/password", map[string]any{"password": password}, nil)
}
func (r *TelegramResource) Logout(ctx context.Context) (map[string]any, error) {
	return r.request(ctx, "POST", "/api/auth/logout", nil, nil)
}
func (r *TelegramResource) Whoami(ctx context.Context) (map[string]any, error) {
	return r.request(ctx, "GET", "/api/whoami", nil, nil)
}
func (r *TelegramResource) Chats(ctx context.Context, limit *int, unreadOnly string) (map[string]any, error) {
	q := url.Values{}
	if limit != nil {
		q.Set("limit", strconv.Itoa(*limit))
	}
	if unreadOnly != "" {
		q.Set("unread_only", unreadOnly)
	}
	return r.request(ctx, "GET", "/api/chats", nil, q)
}
func (r *TelegramResource) Contacts(ctx context.Context) (map[string]any, error) {
	return r.request(ctx, "GET", "/api/contacts", nil, nil)
}
func (r *TelegramResource) Messages(ctx context.Context, target string, limit *int) (map[string]any, error) {
	q := url.Values{}
	if limit != nil {
		q.Set("limit", strconv.Itoa(*limit))
	}
	return r.request(ctx, "GET", "/api/chats/"+target+"/messages", nil, q)
}
func (r *TelegramResource) SearchMessages(ctx context.Context, q, target string, limit *int) (map[string]any, error) {
	v := url.Values{"q": {q}}
	if target != "" {
		v.Set("target", target)
	}
	if limit != nil {
		v.Set("limit", strconv.Itoa(*limit))
	}
	return r.request(ctx, "GET", "/api/messages/search", nil, v)
}
func (r *TelegramResource) SendMessage(ctx context.Context, target, text, replyTo string) (map[string]any, error) {
	b := map[string]any{"target": target, "text": text}
	if replyTo != "" {
		b["reply_to"] = replyTo
	}
	return r.request(ctx, "POST", "/api/messages", b, nil)
}
func (r *TelegramResource) DeleteMessage(ctx context.Context, target, messageID string) (map[string]any, error) {
	return r.request(ctx, "DELETE", "/api/chats/"+target+"/messages/"+messageID, nil, nil)
}
func (r *TelegramResource) AddReaction(ctx context.Context, target, messageID, emoji string) (map[string]any, error) {
	return r.request(ctx, "POST", "/api/chats/"+target+"/messages/"+messageID+"/reactions", map[string]any{"emoji": emoji}, nil)
}
func (r *TelegramResource) MarkRead(ctx context.Context, target string) (map[string]any, error) {
	return r.request(ctx, "POST", "/api/chats/"+target+"/read", nil, nil)
}
