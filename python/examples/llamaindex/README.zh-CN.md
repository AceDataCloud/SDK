# LlamaIndex：搜索 → 网页提取 → 带来源检索

[English](README.md)

使用已发布的 Ace Data Cloud Python SDK，以及 LlamaIndex 的 `FunctionTool`、
`Document` 和 `SimpleKeywordTableIndex`，得到带来源 URL 的检索片段。
示例不生成回答，不需要 LLM 或 embedding 密钥。这是 Ace 维护的示例；
尚无 LlamaIndex 官方收录、默认内置或精选证明。

这是辅助性的 SDK 搜索/提取兼容示例，与已通过 GitHub 发布 **v0.1.0** 的六个原生 LlamaIndex 包分开：

| 原生集成 | 版本化发行入口 |
|---|---|
| Ace Data Cloud LLM | [v0.1.0](https://github.com/AceDataCloud/AceDataCloudModelProviderLlamaIndex/releases/tag/v0.1.0) |
| Suno | [v0.1.0](https://github.com/AceDataCloud/SunoLlamaIndex/releases/tag/v0.1.0) |
| Seedance | [v0.1.0](https://github.com/AceDataCloud/SeedanceLlamaIndex/releases/tag/v0.1.0) |
| HappyHorse | [v0.1.0](https://github.com/AceDataCloud/HappyHorseLlamaIndex/releases/tag/v0.1.0) |
| GPT Image | [v0.1.0](https://github.com/AceDataCloud/GPTImageLlamaIndex/releases/tag/v0.1.0) |
| Nano Banana | [v0.1.0](https://github.com/AceDataCloud/NanoBananaLlamaIndex/releases/tag/v0.1.0) |

六包各自有独立 wheel 和原生类/工具，本示例不代替它们，也不等于官方收录。
六个新包的 PyPI 发布仍待共享创建项目配额，按 GitHub 正式发行说明安装，不猜造 PyPI 版本。

## 无 Token 安装与体验

需要 Python 3.10+，CI 使用 3.12。在本目录运行：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python workflow.py
```

默认模式使用**人工编写的模拟响应**，但 SDK、LlamaIndex 工具调用与索引都是真实组件。
API 请求被拦截，未匹配请求会失败。输出标为 `synthetic-offline`，
正文和 task/trace ID 是模拟数据；来源 URL 仅用于演示引用。无需 Token，不发收费请求。

## 连接自己的账户

1. [注册或登录](https://platform.acedata.cloud?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=llamaindex_search_extraction_example_register_zh)，打开[应用控制台 Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=llamaindex_search_extraction_example_api_key_zh)。
2. 找到 **General application**；没有时点 **Initialize General Application**。
   通用应用 Key 仍受当前账户服务权限约束，专用应用仅限其服务；本流程同时需要 Google Search 与 WebExtrator。
3. 复制应用的 **API Key**；或 **Manage Keys → Create** 新建 `LlamaIndex search/extraction` 专用 Key。

![真实 Ace 控制台：复制已遮挡 Key 或打开 Manage Keys](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

4. 按需设置 **Expiration Time**、**Set Usage Limitation** 和 **Allowed APIs**。
   若限制接口，需允许 `/serp/google`、`/webextrator/extract` 以及同 ID 恢复用的 `/webextrator/tasks`。
   创建后回 Key 列表复制 Token 本体，不加 `Bearer `、引号、空格或截图遮挡字符。
   `platform-...` 管理令牌不能代替本流程的服务 Key；不要把真实 Key 放入 prompt、输出、截图或 Git。

![真实 Ace 控制台：创建独立 Key 和可选权限限制](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

图片复用固定 SunoDify 提交的真实脱敏控制台截图，**2026-10-19 复用并目视核验**；
原拍摄日期与控制台版本未知。旧示例名 `Dify tutorial` 应改填 `LlamaIndex search/extraction`。
这些图只展示账户步骤，不是本示例真实运行证据。

5. 开启真实调用前核当前权限、用量、余额与价格：
   [Google Search API](https://platform.acedata.cloud/documents/serp-google?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=llamaindex_serp_example_docs_zh) ·
   [WebExtrator 提取 API](https://platform.acedata.cloud/documents/webextrator-extract?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=llamaindex_webextrator_example_docs_zh) ·
   [当前模型/服务价格](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=llamaindex_search_extraction_example_pricing_zh)。
   本教程不假定固定单价或免费额度。

在 shell 中设置 `ACEDATACLOUD_API_TOKEN`，然后显式开启：

```bash
python workflow.py --live --query "LlamaIndex search tools" --max-pages 1
```

该命令发一次搜索及最多一次提取。`--max-pages` 允许 1–3，默认 2；提取前按 URL 去重。
真实调用使用 `https://api.acedata.cloud` 的 Bearer 鉴权，禁用自动重试；
提取明确设置 `async=false`、`enable_llm=false`。不开 LLM 增强仍可能消耗搜索和提取 Credits。
示例不安装付款 handler，不发链上付款。

鉴权、限流、提取失败、空正文或意外 pending 均会报错。
只有完成的 `data` 会进入索引；若已得到 task ID 却没有正文，
按[任务查询指南](https://platform.acedata.cloud/documents/webextrator-tasks?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=llamaindex_webextrator_example_task_guide_zh)
查询同一 ID，避免重新提交提取。结果保留 `text`、`url`、`title`、`task_id` 和 `trace_id`。

## 放入自己的 Agent

`make_tools(client)` 返回 `ace_web_search` 与 `ace_web_extract` 两个 LlamaIndex 工具，
可加入 Agent 的 `tools`。参见英文 README 的完整代码。
自主 Agent 可能追加调用，需单独设置审批和调用限制；示例 CLI 是有页数上限的固定流程。
本地检索按字面关键词匹配，验证查询为英文，不提供语义排序或回答合成。
在下游 Agent 中把网页正文作为来源数据处理。

## 只读 MCP 工具发现

使用 LlamaIndex 官方通用 MCP 客户端连接 Ace 现有托管 Serp MCP：

```bash
python -m pip install -r requirements-mcp.txt
python mcp_discovery.py
```

上面的工作流与测试使用模拟 API，与这里的联网工具发现分开。2026-10-12 曾通过真实
LlamaIndex MCP 客户端读回 11 个工具并调用免费静态信息工具；这是历史只读证据，
不等于收费搜索/提取或六个原生包发布验收。

先设置 `ACEDATACLOUD_API_TOKEN`：托管端点在工具发现阶段也需要 Bearer 鉴权。
只初始化并执行 `tools/list`，打印工具名与输入 schema。
不执行搜索工具。工具发现通过不能替代真实付费首调；执行搜索仍需自己的权限与额度。

## 离线验证

```bash
python -m pip install pytest
python -m pytest -q
```

测试自动发现 `tests/`，模拟所有 API 请求，验证引用、请求上限、空搜索、URL 去重、
pending/失败提取以及 401/429 错误含义。专属 CI 使用公开发布的依赖版本。

官方依据（2026-10-12 复核）：

- [LlamaIndex 工具](https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/tools/)
- [官方 MCP 客户端](https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/tools/llama-index-tools-mcp)
- [贡献政策](https://github.com/run-llama/llama_index/blob/main/CONTRIBUTING.md)：新增 integration package 在独立仓维护并发布 PyPI，不进入 monorepo。
