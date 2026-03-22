# AceDataCloud SDK Plan

## 目标

为 AceDataCloud 设计并逐步落地一套官方多语言 SDK 体系，优先覆盖 Python、Node/TypeScript、Go 三种语言，并统一以下能力：

- 认证与请求配置
- 调用面 API 封装
- 平台管理面 API 封装
- 长任务轮询与等待
- 流式响应解析
- 文件上传辅助能力
- 错误模型与重试策略
- 文档、示例、测试与发布流程

本计划遵循以下原则：

- 先规范契约，再生成 SDK，不直接从现有碎片化 OpenAPI 生硬生成产物。
- 采用“生成资源层 + 手写核心运行时”的方式，避免多语言 SDK 维护失控。
- 每个阶段独立通过 PR 推进，阶段完成后再进入下一阶段。

## 当前判断

基于现有代码与文档调研，AceDataCloud 已具备 SDK 化基础，但当前公开契约仍偏向文档驱动和单接口文件驱动，尚未达到直接生成高质量多语言 SDK 的状态。

关键现状：

- 平台同时存在调用面和管理面 API。
- OpenAPI 文件按接口拆分，适合文档同步，不适合直接生成统一 SDK。
- 鉴权核心是 Application + Credential + Gateway，不是简单 API Key 模式。
- `task_id` + `callback_url` + 轮询/流式 是大量服务共享的一等模式。
- MCP 客户端已体现若干可复用抽象，但目前仍是服务内适配层，不是正式 SDK 设计。

## 语言策略

### 第一梯队

- Python
- Node / TypeScript
- Go

### 第二梯队

- Java
- C#
- PHP

### 第三梯队

- Ruby
- Kotlin
- Swift

策略说明：

- 第一梯队优先解决主流后端、脚本自动化、前后端集成场景。
- 第二梯队在第一梯队稳定后扩展企业后端生态。
- 第三梯队由真实需求驱动，不提前摊大饼。

## 目标架构

### 顶层客户端

统一使用一个顶层客户端作为入口，例如：

- Python: `AceDataCloudClient`
- Node: `AceDataCloud`
- Go: `sdk.Client`

顶层客户端负责：

- `base_url`
- `platform_base_url`
- `api_token`
- `timeout`
- `retry`
- `headers`
- `transport`
- `user_agent`

### 子客户端分组

顶层客户端下暴露子客户端：

- `chat`
- `images`
- `audio`
- `video`
- `search`
- `tasks`
- `files`
- `platform`
- `openai`

### 统一抽象

所有语言尽量统一以下抽象：

- `ClientOptions`
- `RequestOptions`
- `TaskHandle` / `Poller`
- `Stream` / iterator / async iterator
- `APIError` 及细分错误类型

## 生成与手写边界

### 生成部分

- 请求参数类型
- 响应结构类型
- 资源方法签名
- URL / method / schema 绑定
- 文档骨架

### 手写部分

- 核心运行时
- HTTP transport 包装
- 重试策略
- 超时策略
- 鉴权注入
- 错误映射
- 流式响应解析
- 长任务等待与轮询
- 文件上传封装
- OpenAI 兼容适配层

## 阶段拆分

## Phase 0: 统一契约层准备

### Phase 0 目标

把当前分散的接口定义整理为 SDK 可消费的规范输入，而不是直接对现有碎片文件做代码生成。

### Phase 0 产物

- SDK canonical API inventory
- 聚合 OpenAPI 方案
- overlays / transforms 方案
- 服务分组和标签规则
- path / path2 归一化规则
- 长任务、流式、上传、错误分类规则

### Phase 0 关键工作

- 盘点 `PlatformBackend/openapi` 中所有公开接口。
- 基于 `PlatformBackend/cost/service_api_mapping.json` 建立服务到能力域映射。
- 设计 canonical spec 的聚合方式。
- 为现有 spec 设计 overlay 修正层，而非直接改源文件结构。
- 定义哪些接口进入 SDK 第一批支持范围。

### Phase 0 验收标准

- 可以明确列出 SDK 第一批覆盖接口。
- 可以明确说明每个接口归属哪个能力域。
- 可以明确说明后续生成器的输入是什么。
- 不依赖人工逐个接口手写 SDK 签名。

### Phase 0 风险

- 现有 OpenAPI 文件粒度太碎，聚合时命名和分组容易混乱。
- 同一服务可能同时存在原生路径和兼容路径，需要定义 canonical route。

## Phase 1: SDK 设计规范冻结

### Phase 1 目标

先确定多语言一致的 SDK 设计规范，再进入任何正式代码生成或运行时实现。

### Phase 1 产物

- SDK design RFC
- 命名规范
- 错误模型规范
- Task / Stream 抽象规范
- Request / Client options 规范
- 版本策略
- 发布与兼容策略

### Phase 1 关键工作

- 定义顶层客户端和子客户端命名。
- 定义错误层级。
- 定义流式接口统一行为。
- 定义长任务对象行为。
- 定义 per-request override 行为。
- 定义语言间一致性的最低要求。

### Phase 1 验收标准

- Python、Node、Go 三种语言都能遵守同一份设计规范。
- 不再出现“某语言一个风格，另一语言另一套抽象”的情况。

## Phase 2: 生成器 POC

### Phase 2 目标

验证“聚合 spec + overlay + 代码生成 + 手写 runtime”路线可行。

### Phase 2 产物

- TypeScript SDK POC
- Python SDK POC
- 生成配置文件
- 生成物目录结构样例

### Phase 2 第一批接口范围

- chat
- images
- tasks
- files
- platform.applications
- platform.credentials

### Phase 2 验收标准

- POC 可完成真实请求调用。
- 生成代码和手写 runtime 的边界清晰。
- 后续新增接口可以按相同方式扩展。

## Phase 3: 统一运行时实现

### Phase 3 目标

实现多语言 SDK 共通的运行时策略，确保后续资源层扩展成本可控。

### Phase 3 产物

- transport abstraction
- retry abstraction
- timeout abstraction
- auth injection
- request hooks
- trace / telemetry hooks
- stream parser
- task poller
- upload helper

### Phase 3 验收标准

- 不同资源层共享同一套运行时。
- 同一语言内部不出现重复 transport 逻辑。
- task / stream / upload 都有统一可复用实现。

## Phase 4: Python SDK 首发

### Phase 4 目标

交付功能最完整的 Python SDK，作为第一份正式参考实现。

### Phase 4 覆盖能力

- OpenAI compatible chat
- Responses streaming
- image generation
- audio generation
- video generation
- search
- task polling
- file upload
- applications / credentials
- typed exceptions

### Phase 4 验收标准

- 提供 sync + async 两套 client。
- 提供类型化模型。
- 提供完整 examples 和基础集成测试。

## Phase 5: Node / TypeScript SDK 首发

### Phase 5 目标

交付 TypeScript 一等公民体验的 SDK，并兼顾 Node 服务端与前端/Edge 场景。

### Phase 5 重点

- ESM first
- TypeScript types
- async iterator streams
- AbortSignal
- Node / browser transport boundary
- tree-shake friendly exports

### Phase 5 验收标准

- Node 场景可稳定使用。
- 浏览器受限能力有明确边界。
- 文档示例面向 TS 用户友好。

## Phase 6: Go SDK 首发

### Phase 6 目标

交付适合后端生产场景的 Go SDK。

### Phase 6 重点

- `context.Context`
- typed error unwrap
- io 流上传
- poller
- 可替换 `http.Client`

### Phase 6 验收标准

- 在 Go 服务端场景中具备自然可用的 API。
- 超时、取消、重试行为符合 Go 生态惯例。

## Phase 7: 管理面 SDK 完整化

### Phase 7 目标

把平台对象管理能力纳入正式 SDK，而不是只提供调用面。

### Phase 7 覆盖能力

- services
- applications
- credentials
- platform tokens
- usage
- orders / balances
- config
- models

### Phase 7 验收标准

- 开发者可以通过 SDK 完成“开通服务 -> 创建凭证 -> 调用接口”的完整链路。

## Phase 8: 文档、示例、测试与发布自动化

### Phase 8 目标

将 SDK 从“可用”提升为“可规模维护和发布”。

### Phase 8 产物

- quickstart examples
- scenario examples
- mock tests
- smoke tests
- CI publish workflow
- versioning strategy
- changelog strategy

### Phase 8 验收标准

- 每种首发语言都有最小可用示例。
- 发布流程自动化。
- 版本升级对外可追踪。

## 第一批接口建议范围

### 调用面

- Chat / OpenAI compatible chat
- Responses
- Images
- Audio
- Video
- Search
- Tasks
- Files

### 管理面

- Services
- Applications
- Credentials
- Models
- Config

说明：

- Usage / Orders / Balances 可在第一梯队 SDK 稳定后继续补齐。
- X402 可单独评估是否作为独立扩展模块。

## PR 推进方式

每个阶段至少遵循以下规则：

- 一阶段一 PR，尽量不要把多个阶段混进同一个 PR。
- 每个 PR 都包含明确的阶段目标和验收结果。
- 先搭基础再铺接口，不要反过来。
- 每次只扩大一层复杂度，避免大爆炸式推进。

建议 PR 顺序：

1. Phase 0 契约准备与范围冻结
2. Phase 1 SDK 设计规范
3. Phase 2 生成器 POC
4. Phase 3 统一运行时
5. Phase 4 Python SDK
6. Phase 5 TypeScript SDK
7. Phase 6 Go SDK
8. Phase 7 管理面完整化
9. Phase 8 发布自动化与示例

## 当前执行顺序

当前从 Phase 0 开始，优先产出：

- 统一阶段计划
- Phase 0 交付物清单
- 第一批 SDK 覆盖范围
- canonical spec 组织方向

Phase 0 完成后，进入 Phase 1，冻结 SDK 设计规范。
