# 单服务集成的图文首用素材

[English](README.md)

用户搜索的是 Suno、Seedance、HappyHorse、GPT Image、Nano Banana；保持“服务名 + by Ace Data Cloud”的清晰身份。SDK 是这些独立服务插件的公共底座，不是外部市场收录或默认 Provider 本身。

## 复用真实流程

参考 [Suno Dify 英文](https://github.com/AceDataCloud/SunoDify/blob/main/README.md)和[中文](https://github.com/AceDataCloud/SunoDify/blob/main/readme/README_zh_Hans.md)：准确官方安装入口 → 注册/登录 → Applications/General application → 复制/创建本宿主专用 API Key → 宿主实际凭据位置 → 首用 → 同 task ID 查询 → 最终输出/常见问题。

复用结构，不能把 Dify 菜单或运行结果移植成另一个宿主的截图。Ace 集成不是模型方官方客户端；不能臆造默认 Provider、新按钮、搜索排名或尚不存在的独立包。

## 可执行的英中模板

用 [`profiles/suno-cli.json`](profiles/suno-cli.json) 配置真实包入口、终端凭据位置和本地免费命令。渲染结果见 [English](suno-cli.en.md) / [中文](suno-cli.zh-CN.md)。

```bash
python3 scripts/render_onboarding.py --profile docs/integration-onboarding/profiles/suno-cli.json --language en --output /tmp/suno-first-use.en.md
python3 scripts/render_onboarding.py --profile docs/integration-onboarding/profiles/suno-cli.json --language zh-CN --output /tmp/suno-first-use.zh-CN.md
```

新 profile 必须写准安装入口、真实 Token 粘贴位置、生成/查询 API、首用步骤、同 ID 查询。脚本只生成说明，不装软件、不建账号、不保存Key、不启动服务、不调用API。

保留已有四项 UTM：source、medium=referral、campaign=evergreen、服务/宿主 content。共享 GitHub/包 README 使用 opensource；单独渲染包页面才可用 pypi/npm。不要把营销参数加到协议地址、OAuth或Key；不借此改全局归因规范。

## 真图与限制

[复制应用Key](assets/get-api-key-en.png) · [创建专用Key](assets/create-api-key-en.png) · [完整出处、日期、SHA](assets.json)

两张原图来自 Suno Dify 固定提交 8d3d0357，10-08 已存档；敏感值已遮挡，原拍摄时间/前端版本未核实。Dify tutorial 是原字段示例名，请实际用自己的宿主名。原图只证明共用取密钥步骤，不证明新宿主安装或运行。

宿主图必须有真实来源和日期，缺少时渲染器会拒绝。没有真实图就保留缺证说明，不画假终端/假GUI。官方图编辑预览也必须标“官方原图改编，非实际运行”。

## 源码归属与发布

- SDK 底座归 SDK；生成客户端不在模板中重复维护。
- 服务名目录归 Clis/service-packages.json，只有已核实包可以称已发布。
- MCPs/Skills 各由现有唯一源码负责人维护，只消费实际生命周期、合同和宿主配方，不改镜像或重复错误语义PR。
- 凭据、价格、UTM 归 Backend；不新增fallback、费用或全局渠道规则。
- 各平台原生 Provider/独立插件由对应平台负责人实现，本模板不把手动导入当原生收录。

官方 [PyPA](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) 与 [npm](https://docs.npmjs.com/cli/v11/configuring-npm/package-json) 支持正确的服务关键词、summary、author/source 元数据。源码合并后仍需构建检查、现有流程发包、读回真实版本、全新安装，再独立验宿主/生成/最终媒体/唯一账单/注册付费。包数与下载量不是获客或营收。
