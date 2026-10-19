# Make 的 Nano Banana 集成，由 Ace Data Cloud 提供

独立服务App源项目：**Generate a Nano Banana image**、**Get a Nano Banana task**、**Make an API call**。使用自己的Ace应用Token，不冒充第三方官方。[English](README.md)。

**Community目录名称按当前表单填写 `Nano Banana`，不把开发者公司名加进App名称；Ace Data Cloud身份放在描述、提供者和landing页。** README标题只是说明集成提供者，不是已批准目录名。[2026-10-19核验的投稿规则](../COMMUNITY_SUBMISSION.md)。

## 1. 正确安装入口

**官方Make安装链接待发布，尚未部署、审核或上架。** 发布后核对提供者为Ace Data Cloud，再装到目标组织。开发者用本目录manifest配对自己的独立测试App，先查已有应用，不能指向Suno/聊天/其他服务origin。[配对说明](../README.md#set-up-a-private-testing-app)。

![Make官方模块选择器参考](../suno/_assets/tutorial/make-official-module-picker.png)

原图是Geocodify，2026-10-17下载，原拍摄日期/版本未知；不证明Nano Banana已安装。[来源](../suno/ASSET_SOURCES.md)。

## 2. 登录Ace并复制或创建专用Token

1. 打开 [Applications](https://platform.acedata.cloud/console/applications?utm_source=make&utm_medium=integration&utm_campaign=evergreen&utm_content=nano_banana_make_zh_api_key) 注册/登录；没有General application时先初始化。
2. 复制General application或可用服务应用的API Key，或 **Manage Keys → Create** 创建`Make Nano Banana`专用Key；核有效期、用量限制、余额与[当前价格](https://platform.acedata.cloud/models?utm_source=make&utm_medium=integration&utm_campaign=evergreen&utm_content=nano_banana_make_zh_pricing)。允许API需覆盖生成`/nano-banana/images`、查询`/nano-banana/tasks`和连接读取`/v1/models`，不盲目扩权。

![Ace Applications: copy a key or open Manage Keys](../suno/_assets/tutorial/get-api-key-en.png)

![Ace key creation with restrictions](../suno/_assets/tutorial/create-api-key-en.png)

平台真图于2026-10-18从固定SunoDify版本取回，Token已遮挡；图中Dify tutorial仅历史Key名称示例，并非本Make App运行。

3. 在已安装模块点 **Create a connection**，把原始Token填进 **Ace Data Cloud API token**，不加Bearer，不用platform管理Token或Make开发Key。保存只做免费模型GET；认证不代表生成权限和余额已足够。

## 3. 首版范围与同ID查询

本服务首版范围（精确字段见英文参数表）：

One generated image only: `action=generate`, `count=1`, Nano Banana 2 / 2.1 / Pro, aspect ratio and 1K/2K/4K resolution. The Lite model is excluded from this module because it supports only 1K. Image editing/reference inputs are not exposed. Its result uses image_url, not the GPT Image url field.

获准预算后只运行一次生成，返回task_id/pending，不代表完成。把Task ID用变量选择器映射到 **Get a Nano Banana task**；它只调用`/nano-banana/tasks`的retrieve，不生成。pending时使用仅查询场景读同ID，不重跑生成。只有Status=succeeded、Terminal success=true时使用 **Completed image URL**。模型/尺寸/时长受当前账户与模型约束，不能把其他服务字段照搬。

先免费运行通用模块 **GET /v1/models**，再查询自己已有任务；没有已成功任务就保留待验收，不使用他人ID。检查原任务/trace和唯一生成账单，Make操作额度与Ace Credits分开；[请求记录](https://platform.acedata.cloud/console/usages?utm_source=make&utm_medium=integration&utm_campaign=evergreen&utm_content=nano_banana_make_zh_usages)。

## 4. 常见问题与发布

- 401：检查完整原始Token、有效期、允许API、服务权限、余额/限额。
- 400：核对本服务字段、模型和大小写分辨率；不套其他服务参数。
- pending/无链接：继续查同一ID；预览不是终态，不重新生成。
- failed/字符串或未知结构：保留task/trace检查，不猜成功。
- 429/超时/5xx：先看请求记录，场景重放/传输错误仍可能导致重复付费；本源不设自动应用错误重试或fallback。

发布须真实Make场景、日志脱敏、独立安装、资格/名称/商标确认和[发布材料](PUBLICATION.md)。当前只有源码和离线验证，无市场版本/真实宿主/新生成账单证明。
