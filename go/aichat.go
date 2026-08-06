package acedatacloud

import "context"

type AiChatModel string

const (
	AiChatModelGpt56Luna                      AiChatModel = "gpt-5.6-luna"
	AiChatModelGpt56Terra                     AiChatModel = "gpt-5.6-terra"
	AiChatModelGpt56Sol                       AiChatModel = "gpt-5.6-sol"
	AiChatModelGpt55                          AiChatModel = "gpt-5.5"
	AiChatModelGpt55Pro                       AiChatModel = "gpt-5.5-pro"
	AiChatModelGpt54                          AiChatModel = "gpt-5.4"
	AiChatModelGpt54Mini                      AiChatModel = "gpt-5.4-mini"
	AiChatModelGpt54Nano                      AiChatModel = "gpt-5.4-nano"
	AiChatModelGpt54Pro                       AiChatModel = "gpt-5.4-pro"
	AiChatModelGpt52                          AiChatModel = "gpt-5.2"
	AiChatModelGpt51                          AiChatModel = "gpt-5.1"
	AiChatModelGpt51All                       AiChatModel = "gpt-5.1-all"
	AiChatModelGpt5                           AiChatModel = "gpt-5"
	AiChatModelGpt5Mini                       AiChatModel = "gpt-5-mini"
	AiChatModelGpt5Nano                       AiChatModel = "gpt-5-nano"
	AiChatModelGpt5All                        AiChatModel = "gpt-5-all"
	AiChatModelGpt4                           AiChatModel = "gpt-4"
	AiChatModelGpt4All                        AiChatModel = "gpt-4-all"
	AiChatModelGpt4Turbo                      AiChatModel = "gpt-4-turbo"
	AiChatModelGpt4TurboPreview               AiChatModel = "gpt-4-turbo-preview"
	AiChatModelGpt4VisionPreview              AiChatModel = "gpt-4-vision-preview"
	AiChatModelGpt41                          AiChatModel = "gpt-4.1"
	AiChatModelGpt4120250414                  AiChatModel = "gpt-4.1-2025-04-14"
	AiChatModelGpt41Mini                      AiChatModel = "gpt-4.1-mini"
	AiChatModelGpt41Mini20250414              AiChatModel = "gpt-4.1-mini-2025-04-14"
	AiChatModelGpt41Nano                      AiChatModel = "gpt-4.1-nano"
	AiChatModelGpt41Nano20250414              AiChatModel = "gpt-4.1-nano-2025-04-14"
	AiChatModelGpt45Preview                   AiChatModel = "gpt-4.5-preview"
	AiChatModelGpt45Preview20250227           AiChatModel = "gpt-4.5-preview-2025-02-27"
	AiChatModelGpt4o                          AiChatModel = "gpt-4o"
	AiChatModelGpt4o20240513                  AiChatModel = "gpt-4o-2024-05-13"
	AiChatModelGpt4o20240806                  AiChatModel = "gpt-4o-2024-08-06"
	AiChatModelGpt4o20241120                  AiChatModel = "gpt-4o-2024-11-20"
	AiChatModelGpt4oAll                       AiChatModel = "gpt-4o-all"
	AiChatModelGpt4oImage                     AiChatModel = "gpt-4o-image"
	AiChatModelGpt4oMini                      AiChatModel = "gpt-4o-mini"
	AiChatModelGpt4oMini20240718              AiChatModel = "gpt-4o-mini-2024-07-18"
	AiChatModelGpt4oMiniSearchPreview         AiChatModel = "gpt-4o-mini-search-preview"
	AiChatModelGpt4oMiniSearchPreview20250311 AiChatModel = "gpt-4o-mini-search-preview-2025-03-11"
	AiChatModelGpt4oSearchPreview             AiChatModel = "gpt-4o-search-preview"
	AiChatModelGpt4oSearchPreview20250311     AiChatModel = "gpt-4o-search-preview-2025-03-11"
	AiChatModelO1                             AiChatModel = "o1"
	AiChatModelO120241217                     AiChatModel = "o1-2024-12-17"
	AiChatModelO1All                          AiChatModel = "o1-all"
	AiChatModelO1Mini                         AiChatModel = "o1-mini"
	AiChatModelO1Mini20240912                 AiChatModel = "o1-mini-2024-09-12"
	AiChatModelO1MiniAll                      AiChatModel = "o1-mini-all"
	AiChatModelO1Preview                      AiChatModel = "o1-preview"
	AiChatModelO1Preview20240912              AiChatModel = "o1-preview-2024-09-12"
	AiChatModelO1PreviewAll                   AiChatModel = "o1-preview-all"
	AiChatModelO1Pro                          AiChatModel = "o1-pro"
	AiChatModelO1Pro20250319                  AiChatModel = "o1-pro-2025-03-19"
	AiChatModelO1ProAll                       AiChatModel = "o1-pro-all"
	AiChatModelO3                             AiChatModel = "o3"
	AiChatModelO320250416                     AiChatModel = "o3-2025-04-16"
	AiChatModelO3All                          AiChatModel = "o3-all"
	AiChatModelO3Mini                         AiChatModel = "o3-mini"
	AiChatModelO3Mini20250131                 AiChatModel = "o3-mini-2025-01-31"
	AiChatModelO3Mini20250131High             AiChatModel = "o3-mini-2025-01-31-high"
	AiChatModelO3Mini20250131Low              AiChatModel = "o3-mini-2025-01-31-low"
	AiChatModelO3Mini20250131Medium           AiChatModel = "o3-mini-2025-01-31-medium"
	AiChatModelO3MiniAll                      AiChatModel = "o3-mini-all"
	AiChatModelO3MiniHigh                     AiChatModel = "o3-mini-high"
	AiChatModelO3MiniHighAll                  AiChatModel = "o3-mini-high-all"
	AiChatModelO3MiniLow                      AiChatModel = "o3-mini-low"
	AiChatModelO3MiniMedium                   AiChatModel = "o3-mini-medium"
	AiChatModelO3Pro                          AiChatModel = "o3-pro"
	AiChatModelO3Pro20250610                  AiChatModel = "o3-pro-2025-06-10"
	AiChatModelO4Mini                         AiChatModel = "o4-mini"
	AiChatModelO4Mini20250416                 AiChatModel = "o4-mini-2025-04-16"
	AiChatModelO4MiniAll                      AiChatModel = "o4-mini-all"
	AiChatModelO4MiniHighAll                  AiChatModel = "o4-mini-high-all"
	AiChatModelDeepseekR1                     AiChatModel = "deepseek-r1"
	AiChatModelDeepseekR10528                 AiChatModel = "deepseek-r1-0528"
	AiChatModelDeepseekV3                     AiChatModel = "deepseek-v3"
	AiChatModelDeepseekV3250324               AiChatModel = "deepseek-v3-250324"
	AiChatModelDeepseekV4Flash                AiChatModel = "deepseek-v4-flash"
	AiChatModelGrok45                         AiChatModel = "grok-4.5"
	AiChatModelGrok3                          AiChatModel = "grok-3"
	AiChatModelGlm52                          AiChatModel = "glm-5.2"
	AiChatModelGlm5                           AiChatModel = "glm-5"
	AiChatModelGlm5Turbo                      AiChatModel = "glm-5-turbo"
	AiChatModelGlm51                          AiChatModel = "glm-5.1"
	AiChatModelGlm47                          AiChatModel = "glm-4.7"
	AiChatModelGlm46                          AiChatModel = "glm-4.6"
	AiChatModelGlm3Turbo                      AiChatModel = "glm-3-turbo"
)

type AiChat2Model string

const (
	AiChat2ModelGpt4                      AiChat2Model = "gpt-4"
	AiChat2ModelGpt41                     AiChat2Model = "gpt-4.1"
	AiChat2ModelGpt41Mini                 AiChat2Model = "gpt-4.1-mini"
	AiChat2ModelGpt41Nano                 AiChat2Model = "gpt-4.1-nano"
	AiChat2ModelGpt4o                     AiChat2Model = "gpt-4o"
	AiChat2ModelGpt4o20240513             AiChat2Model = "gpt-4o-2024-05-13"
	AiChat2ModelGpt4oAll                  AiChat2Model = "gpt-4o-all"
	AiChat2ModelGpt4oImage                AiChat2Model = "gpt-4o-image"
	AiChat2ModelGpt4oMini                 AiChat2Model = "gpt-4o-mini"
	AiChat2ModelGpt5All                   AiChat2Model = "gpt-5-all"
	AiChat2ModelGpt51All                  AiChat2Model = "gpt-5.1-all"
	AiChat2ModelGpt52Pro                  AiChat2Model = "gpt-5.2-pro"
	AiChat2ModelGpt54Mini                 AiChat2Model = "gpt-5.4-mini"
	AiChat2ModelGpt54Nano                 AiChat2Model = "gpt-5.4-nano"
	AiChat2ModelGptImage1                 AiChat2Model = "gpt-image-1"
	AiChat2ModelClaude35Haiku20241022     AiChat2Model = "claude-3-5-haiku-20241022"
	AiChat2ModelClaude35Sonnet20240620    AiChat2Model = "claude-3-5-sonnet-20240620"
	AiChat2ModelClaude35Sonnet20241022    AiChat2Model = "claude-3-5-sonnet-20241022"
	AiChat2ModelClaude37Sonnet20250219    AiChat2Model = "claude-3-7-sonnet-20250219"
	AiChat2ModelClaude3Haiku20240307      AiChat2Model = "claude-3-haiku-20240307"
	AiChat2ModelClaude3Opus20240229       AiChat2Model = "claude-3-opus-20240229"
	AiChat2ModelClaude3Sonnet20240229     AiChat2Model = "claude-3-sonnet-20240229"
	AiChat2ModelClaudeHaiku4520251001     AiChat2Model = "claude-haiku-4-5-20251001"
	AiChat2ModelClaudeOpus4120250805      AiChat2Model = "claude-opus-4-1-20250805"
	AiChat2ModelClaudeOpus420250514       AiChat2Model = "claude-opus-4-20250514"
	AiChat2ModelClaudeOpus4520251101      AiChat2Model = "claude-opus-4-5-20251101"
	AiChat2ModelClaudeOpus46              AiChat2Model = "claude-opus-4-6"
	AiChat2ModelClaudeFable5              AiChat2Model = "claude-fable-5"
	AiChat2ModelClaudeOpus5               AiChat2Model = "claude-opus-5"
	AiChat2ModelClaudeOpus48              AiChat2Model = "claude-opus-4-8"
	AiChat2ModelClaudeOpus47              AiChat2Model = "claude-opus-4-7"
	AiChat2ModelClaudeSonnet420250514     AiChat2Model = "claude-sonnet-4-20250514"
	AiChat2ModelClaudeSonnet4520250929    AiChat2Model = "claude-sonnet-4-5-20250929"
	AiChat2ModelClaudeSonnet46            AiChat2Model = "claude-sonnet-4-6"
	AiChat2ModelClaudeSonnet5             AiChat2Model = "claude-sonnet-5"
	AiChat2ModelGemini20FlashLite         AiChat2Model = "gemini-2.0-flash-lite"
	AiChat2ModelGemini25FlashLite         AiChat2Model = "gemini-2.5-flash-lite"
	AiChat2ModelGemini3ProPreview         AiChat2Model = "gemini-3-pro-preview"
	AiChat2ModelGemini31FlashImagePreview AiChat2Model = "gemini-3.1-flash-image-preview"
	AiChat2ModelGemini31FlashLitePreview  AiChat2Model = "gemini-3.1-flash-lite-preview"
	AiChat2ModelGemini31Pro               AiChat2Model = "gemini-3.1-pro"
	AiChat2ModelGemini31ProPreview        AiChat2Model = "gemini-3.1-pro-preview"
	AiChat2ModelGrok3                     AiChat2Model = "grok-3"
	AiChat2ModelGrok3Fast                 AiChat2Model = "grok-3-fast"
	AiChat2ModelGrok4                     AiChat2Model = "grok-4"
	AiChat2ModelGrok45                    AiChat2Model = "grok-4.5"
	AiChat2ModelGrok40709                 AiChat2Model = "grok-4-0709"
	AiChat2ModelDeepseekChat              AiChat2Model = "deepseek-chat"
	AiChat2ModelDeepseekR1                AiChat2Model = "deepseek-r1"
	AiChat2ModelDeepseekR10528            AiChat2Model = "deepseek-r1-0528"
	AiChat2ModelDeepseekReasoner          AiChat2Model = "deepseek-reasoner"
	AiChat2ModelDeepseekV3                AiChat2Model = "deepseek-v3"
	AiChat2ModelDeepseekV3250324          AiChat2Model = "deepseek-v3-250324"
	AiChat2ModelDeepseekV32Exp            AiChat2Model = "deepseek-v3.2-exp"
	AiChat2ModelDeepseekV4Flash           AiChat2Model = "deepseek-v4-flash"
	AiChat2ModelKimiK2Thinking            AiChat2Model = "kimi-k2-thinking"
	AiChat2ModelKimiK2ThinkingTurbo       AiChat2Model = "kimi-k2-thinking-turbo"
	AiChat2ModelKimiK3                    AiChat2Model = "kimi-k3"
	AiChat2ModelKimiK26                   AiChat2Model = "kimi-k2.6"
	AiChat2ModelKimiK25                   AiChat2Model = "kimi-k2.5"
	AiChat2ModelGlm3Turbo                 AiChat2Model = "glm-3-turbo"
	AiChat2ModelGlm45                     AiChat2Model = "glm-4.5"
	AiChat2ModelGlm45v                    AiChat2Model = "glm-4.5v"
	AiChat2ModelGlm46                     AiChat2Model = "glm-4.6"
	AiChat2ModelGlm47                     AiChat2Model = "glm-4.7"
	AiChat2ModelGlm5                      AiChat2Model = "glm-5"
	AiChat2ModelGlm5Turbo                 AiChat2Model = "glm-5-turbo"
	AiChat2ModelGlm52                     AiChat2Model = "glm-5.2"
	AiChat2ModelGlm51                     AiChat2Model = "glm-5.1"
	AiChat2ModelO1                        AiChat2Model = "o1"
	AiChat2ModelO1Mini                    AiChat2Model = "o1-mini"
	AiChat2ModelO1Pro                     AiChat2Model = "o1-pro"
	AiChat2ModelO3                        AiChat2Model = "o3"
	AiChat2ModelO3Mini                    AiChat2Model = "o3-mini"
	AiChat2ModelO3Pro                     AiChat2Model = "o3-pro"
	AiChat2ModelO4Mini                    AiChat2Model = "o4-mini"
)

type AiChat2Action string

const (
	AiChat2ActionChat          AiChat2Action = "chat"
	AiChat2ActionRetrieve      AiChat2Action = "retrieve"
	AiChat2ActionRetrieveBatch AiChat2Action = "retrieve_batch"
	AiChat2ActionUpdate        AiChat2Action = "update"
	AiChat2ActionDelete        AiChat2Action = "delete"
)

type AiChat2ModelGroup string

const (
	AiChat2ModelGroupChatgpt  AiChat2ModelGroup = "chatgpt"
	AiChat2ModelGroupClaude   AiChat2ModelGroup = "claude"
	AiChat2ModelGroupGemini   AiChat2ModelGroup = "gemini"
	AiChat2ModelGroupGrok     AiChat2ModelGroup = "grok"
	AiChat2ModelGroupKimi     AiChat2ModelGroup = "kimi"
	AiChat2ModelGroupGlm      AiChat2ModelGroup = "glm"
	AiChat2ModelGroupDeepseek AiChat2ModelGroup = "deepseek"
)

// AiChatResource exposes /aichat/conversations.
type AiChatResource struct{ t *transport }

// AiChatCreateRequest is the input to AiChat.Create.
type AiChatCreateRequest struct {
	Model      AiChatModel
	Question   string
	ID         string
	Preset     string
	Stateful   *bool
	References []string
	Extra      map[string]any
}

func (r AiChatCreateRequest) toBody() map[string]any {
	body := map[string]any{"model": r.Model, "question": r.Question}
	if r.ID != "" {
		body["id"] = r.ID
	}
	if r.Preset != "" {
		body["preset"] = r.Preset
	}
	if r.Stateful != nil {
		body["stateful"] = *r.Stateful
	}
	if r.References != nil {
		body["references"] = r.References
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// Create posts a conversation request to /aichat/conversations.
func (c *AiChatResource) Create(ctx context.Context, req AiChatCreateRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{Method: "POST", Path: "/aichat/conversations", Body: req.toBody()})
}

// AiChat2Resource exposes /aichat2/conversations.
type AiChat2Resource struct{ t *transport }

// AiChat2MessagePart describes a structured text, image_url, or file_url message part.
type AiChat2MessagePart map[string]any

// AiChat2ToolResult is a tool output sent back to an AI chat v2 conversation.
type AiChat2ToolResult struct {
	ToolUseID string
	Output    string
	IsError   *bool
}

func (r AiChat2ToolResult) toBody() map[string]any {
	body := map[string]any{"tool_use_id": r.ToolUseID, "output": r.Output}
	if r.IsError != nil {
		body["is_error"] = *r.IsError
	}
	return body
}

// AiChat2UnattendedPolicy constrains unattended tool/MCP access.
type AiChat2UnattendedPolicy struct {
	AllowedSkills     []string
	AllowedMCPServers []string
	ExpiresAt         int
	Extra             map[string]any
}

func (p AiChat2UnattendedPolicy) toBody() map[string]any {
	body := map[string]any{}
	if p.AllowedSkills != nil {
		body["allowed_skills"] = p.AllowedSkills
	}
	if p.AllowedMCPServers != nil {
		body["allowed_mcp_servers"] = p.AllowedMCPServers
	}
	if p.ExpiresAt != 0 {
		body["expires_at"] = p.ExpiresAt
	}
	for k, v := range p.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// AiChat2CreateRequest is the input to AiChat2.Create.
type AiChat2CreateRequest struct {
	Model             AiChat2Model
	Action            AiChat2Action
	ID                string
	Question          string
	Message           any
	Stateful          *bool
	References        []string
	Preset            string
	MaxTurns          int
	Async             *bool
	CallbackURL       string
	AllowedSkills     []string
	AllowedMCPServers []string
	UnattendedPolicy  *AiChat2UnattendedPolicy
	ToolResults       []AiChat2ToolResult
	Messages          []map[string]any
	Title             string
	UserID            string
	ApplicationID     string
	ModelGroup        AiChat2ModelGroup
	Offset            *int
	Limit             *int
}

func (r AiChat2CreateRequest) toBody() map[string]any {
	body := map[string]any{"model": r.Model}
	if r.Action != "" {
		body["action"] = r.Action
	}
	if r.ID != "" {
		body["id"] = r.ID
	}
	if r.Question != "" {
		body["question"] = r.Question
	}
	if r.Message != nil {
		body["message"] = r.Message
	}
	if r.Stateful != nil {
		body["stateful"] = *r.Stateful
	}
	if r.References != nil {
		body["references"] = r.References
	}
	if r.Preset != "" {
		body["preset"] = r.Preset
	}
	if r.MaxTurns != 0 {
		body["max_turns"] = r.MaxTurns
	}
	if r.Async != nil {
		body["async"] = *r.Async
	}
	if r.CallbackURL != "" {
		body["callback_url"] = r.CallbackURL
	}
	if r.AllowedSkills != nil {
		body["allowed_skills"] = r.AllowedSkills
	}
	if r.AllowedMCPServers != nil {
		body["allowed_mcp_servers"] = r.AllowedMCPServers
	}
	if r.UnattendedPolicy != nil {
		body["unattended_policy"] = r.UnattendedPolicy.toBody()
	}
	if r.ToolResults != nil {
		items := make([]map[string]any, 0, len(r.ToolResults))
		for _, item := range r.ToolResults {
			items = append(items, item.toBody())
		}
		body["tool_results"] = items
	}
	if r.Messages != nil {
		body["messages"] = r.Messages
	}
	if r.Title != "" {
		body["title"] = r.Title
	}
	if r.UserID != "" {
		body["user_id"] = r.UserID
	}
	if r.ApplicationID != "" {
		body["application_id"] = r.ApplicationID
	}
	if r.ModelGroup != "" {
		body["model_group"] = r.ModelGroup
	}
	if r.Offset != nil {
		body["offset"] = *r.Offset
	}
	if r.Limit != nil {
		body["limit"] = *r.Limit
	}
	return body
}

// Create posts a conversation request to /aichat2/conversations.
func (c *AiChat2Resource) Create(ctx context.Context, req AiChat2CreateRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{Method: "POST", Path: "/aichat2/conversations", Body: req.toBody()})
}
