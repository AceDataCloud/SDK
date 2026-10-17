# Make 的 Suno 集成，由 Ace Data Cloud 提供

用自己的 **Ace Data Cloud API Token** 在 Make 提交 Suno 音乐任务，再查询**同一个任务 ID**取得最终音频。本独立 App 包含 **Generate Suno music**、**Get a Suno task** 和通用接口模块；它不是 Suno 官方应用，也不表示第三方授权或合作关系。

[English](README.md) · [当前服务与价格](https://platform.acedata.cloud/models?utm_source=make&utm_medium=integration&utm_campaign=evergreen&utm_content=suno_make_zh_pricing)

## 1. 从正确入口安装

**Make 官方安装链接尚未生成；未部署、未审核、未公开上架。** 获批后从正式链接进入，核对集成提供者为 **Ace Data Cloud**，安装到目标组织，再在场景添加模块。不能仅因其他应用名称含 Suno 就当作本集成。

开发者使用[私有配对步骤](../README.md#set-up-a-private-testing-app)，选择本目录的 `makecomapp.json`，先查是否已有本 Suno 测试 App，避免重复创建。Suno 与聊天项目分别部署，不要把此 manifest 指向原聊天 App。真实区域、App ID、组织和邀请链接仍待配对。

![Make 官方私有模块选择器原图](./_assets/tutorial/make-official-module-picker.png)

这是 Make 官方 **Geocodify** 教程原图，2026-10-17 下载，拍摄日期和版本未标明；只说明真实模块选择器的操作位置，不证明 Ace/Suno 已安装。[来源](ASSET_SOURCES.md)。

## 2. 注册、登录并取得专用 Token

1. 打开 [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=make&utm_medium=integration&utm_campaign=evergreen&utm_content=suno_make_zh_api_key)，注册/登录。若缺少 **General application**，先点 **Initialize General Application**。
2. 在 General application 或可访问 Suno 的应用中复制 API Key，或通过 **Manage Keys → Create** 创建 `Make Suno` 专用 Key。检查有效期、用量限制、服务权限、当前余额与价格。生成需 `/suno/audios`，查询需 `/suno/tasks`；Connection 还读取 `/v1/models` 验证认证，受限 Key 需有该读取权限，不要盲目放宽权限。

![复制 API Key 或打开 Manage Keys](./_assets/tutorial/get-api-key-en.png)

![创建带可选权限和用量限制的 Key](./_assets/tutorial/create-api-key-en.png)

截图复用固定版本的 SunoDify 图文教程，2026-10-18 取回，凭据已遮挡；它们是 Ace 控制台界面，不是 Make 安装证据。

3. 在已安装的 Make Suno 模块中点 **Create a connection**，把原始 Token 粘到 **Ace Data Cloud API token**，不加 `Bearer `，不用 `platform-...` 管理 Token，也不用 Make 开发 Key。
4. 保存后只读取 `GET /v1/models`；认证通过不代表 Suno 可生成或余额充足。Token 不得出现在提示词、分享蓝图或截图里。

## 3. 生成一次，查询同一 ID

安装并获准使用生成额度后：

1. 添加 **Generate Suno music**，明确选择当前账户可用且已核价的模型，填写 **Music description**，选择是否 **Instrumental only**。它提交一次计费请求，固定 `async=true`、`action=generate`、`custom=false`，返回 `task_id` 和 `pending`；第一版只覆盖文字描述生成，不包含自定义歌词和高级编辑。
2. 添加 **Get a Suno task**，用变量选择器把上一模块的 **Task ID** 映射进来。该模块只向 `/suno/tasks` 发送 `action=retrieve`。仍在处理中时，用单独的“仅查询”场景继续查询同一 ID，不要重跑生成路线。
3. 只有 **Status=succeeded** 且 **Terminal success=true** 才使用 **Completed audio URLs**。未结束任务、预览、部分曲目成功或失败均不会通过此字段输出媒体。核对同一次生成的唯一账单；Make 操作 Credits 与 Ace API Credits 不是同一账目。

第一版不自动循环轮询，不自动重试付费请求；查询安排由用户控制，仍会消耗 Make 操作额度。采用平台内置表达式，不依赖需要另行开通的 custom IML functions。离线通过不等于 Make 中已运行。

## 4. 免费验收与常见问题

先用 **Make an API call → GET /v1/models**；再对自己已有的成功任务运行 **Get a Suno task**。本轮没有新发收费生成。没有已有任务就保留待验收，不填其他人的 ID。

- 401/连接失败：检查 Token 完整值、有效期、允许 API、Suno 权限、用量限制和余额。
- `pending`/空音频：查询同一 ID；预览不等于终态，不重新生成。
- 429/超时/5xx：先查[请求记录](https://platform.acedata.cloud/console/usages?utm_source=make&utm_medium=integration&utm_campaign=evergreen&utm_content=suno_make_zh_usages)，避免重复扣费。场景重放和传输错误仍可能造成重复请求。
- 返回字符串或未知结构：模块拒绝不支持的返回结构，先检查合同，不猜成功。
- 公开安装入口缺失：当前仍是待发布源项目，不能宣称已搜索安装。

发布前需完成真实场景、日志脱敏、终态与唯一账单验收，以及 [官方发布材料](PUBLICATION.md)中所列资格、名称和商标确认。公开发布不可撤回，本项目未执行此操作。
