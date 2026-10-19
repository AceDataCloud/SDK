# Suno by Ace Data Cloud：CLI 首次使用

这是 Ace Data Cloud 提供的 Suno 集成，不是模型方官方客户端。安装与服务调用是不同步骤，使用你自己的应用 API Key。

## 1. 从正确入口安装

打开[已核对的安装入口](https://pypi.org/project/suno-cli/)，确认维护者/源码归属 AceDataCloud。

```bash
python -m pip install suno-cli
suno --help
suno models
```

## 2. 注册/登录并创建 Key

打开 [Applications / 我的应用](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=suno_cli_readme_api_key)，注册或登录。没有通用应用时选 **Initialize General Application / 初始化通用应用**。复制已有 API Key，或 **Manage Keys → Create** 创建本宿主专用 Key。

核对模型/服务权限、有效期、用量限制、余额和[当前价格](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=suno_cli_readme_pricing)。如果启用 Allowed APIs，应允许本例的 `/suno/audios`, `/suno/tasks`；查询权限不等于生成权限。只复制 Token 字符串，不加 Bearer、引号或空格。平台管理 Token 和 Discord 代理凭据均不能代替此 Key。

![Copy the application key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![Create a dedicated key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

以上为官方历史截图，敏感值已遮挡；原字段名 Dify tutorial，仅示意共用 Key 步骤，不是本宿主运行结果。来源/日期见 assets.json。

## 3. 在宿主配置密钥

在启动终端命令的环境变量 ACEDATACLOUD_API_TOKEN 中设置原始 Token，不粘贴到提示词。

共享模板不提供CLI终端截图。需补实际带日期的安装/命令/结果截图，才能声称宿主流程有图验证。

## 4. 首用与同一个任务查询

前面的help/models是本地免费命令。确认并接受当前价格、账号权限和余额后，以下是明确的首次请求例子（模板不会执行）：

```bash
suno generate "A short gentle instrumental piano melody for a sunrise, no vocals." --model chirp-v5-5 --instrumental --async --json
```

它会提交一次可能收费的音乐任务。保存返回的task_id，再用下方命令查询同一个ID；pending时不要重复运行generate。

```text
suno task <task-id>
suno wait <task-id> --interval 5
```

pending 时只查询同一个 task ID，不重复生成。检查最终状态与媒体 URL 后，再独立核对账单；绿色节点或退出码不能代替最终成功。

## 常见问题

401/403：核对原始Key、应用与服务权限。400：核对本服务模型/参数。429：等待并降并发，不自动增加付费重试。5xx/超时：先查原task/trace再决定是否重发。不要在提示词、日志、Git、截图或支持工单中放密钥。
