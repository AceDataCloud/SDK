"""Render a host-specific first-use guide from shared credential/source rules.

This tool formats documentation only. It never installs, authenticates or calls APIs.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlencode, urlsplit

SOURCES = {"opensource", "github", "pypi", "npm"}
ASSETS = "https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial"


def render(profile: dict, language: str = "en") -> str:
    required = {
        "service",
        "host",
        "entry",
        "utm_source",
        "install_url",
        "install_steps",
        "credential_location",
        "credential_location_zh",
        "first_use",
        "first_use_zh",
        "same_task_query",
        "api_operations",
        "host_image_caption",
        "host_image_caption_zh",
    }
    missing = required - profile.keys()
    if missing:
        raise ValueError(f"missing host-specific fields: {sorted(missing)}")
    if profile["utm_source"] not in SOURCES:
        raise ValueError("use an approved source from the existing marketing contract")
    if not re.fullmatch(r"[a-z0-9][a-z0-9_]{0,60}", profile["entry"]):
        raise ValueError("entry must be a stable lowercase attribution identifier")
    if urlsplit(profile["install_url"]).scheme != "https":
        raise ValueError(
            "install_url must be the verified HTTPS package/marketplace entry"
        )
    if language not in {"en", "zh-CN"}:
        raise ValueError("language must be en or zh-CN")

    def cta(path: str, placement: str) -> str:
        query = urlencode(
            {
                "utm_source": profile["utm_source"],
                "utm_medium": "referral",
                "utm_campaign": "evergreen",
                "utm_content": f"{profile['entry']}_readme_{placement}",
            }
        )
        return f"https://platform.acedata.cloud{path}?{query}"

    service, host = profile["service"], profile["host"]
    operations = ", ".join(f"`{value}`" for value in profile["api_operations"])
    zh = language == "zh-CN"
    if zh:
        text = f"""# {service} by Ace Data Cloud：{host} 首次使用

这是 Ace Data Cloud 提供的 {service} 集成，不是模型方官方客户端。安装与服务调用是不同步骤，使用你自己的应用 API Key。

## 1. 从正确入口安装

打开[已核对的安装入口]({profile["install_url"]})，确认维护者/源码归属 AceDataCloud。

{profile["install_steps"]}

## 2. 注册/登录并创建 Key

打开 [Applications / 我的应用]({cta("/console/applications", "api_key")})，注册或登录。没有通用应用时选 **Initialize General Application / 初始化通用应用**。复制已有 API Key，或 **Manage Keys → Create** 创建本宿主专用 Key。

核对模型/服务权限、有效期、用量限制、余额和[当前价格]({cta("/models", "pricing")})。如果启用 Allowed APIs，应允许本例的 {operations}；查询权限不等于生成权限。只复制 Token 字符串，不加 Bearer、引号或空格。平台管理 Token 和 Discord 代理凭据均不能代替此 Key。
"""
    else:
        text = f"""# {service} by Ace Data Cloud: first use in {host}

This is an Ace Data Cloud integration for {service}, not an official client published by the model owner. Installing the integration and making a service request are separate steps. Use your own application API key.

## 1. Install from the correct entry

Open the [verified install entry]({profile["install_url"]}) and confirm the maintainer/source belongs to AceDataCloud.

{profile["install_steps"]}

## 2. Register/sign in and create a key

Open [Applications]({cta("/console/applications", "api_key")}), register/sign in, and choose **Initialize General Application** if needed. Copy its API Key or use **Manage Keys → Create** to name a separate key for this host.

Check model/service access, expiration, usage limits, balance and [current pricing]({cta("/models", "pricing")}). If Allowed APIs is enabled, allow {operations}; task-query permission does not grant generation access. Copy only the raw token, without Bearer, quotation marks or spaces. A platform management token and a Discord proxy credential are different credentials.
"""
    text += f"\n![Copy the application key]({ASSETS}/get-api-key-en.png)\n\n![Create a dedicated key]({ASSETS}/create-api-key-en.png)\n\n"
    text += (
        "以上为官方历史截图，敏感值已遮挡；原字段名 Dify tutorial，仅示意共用 Key 步骤，不是本宿主运行结果。来源/日期见 assets.json。\n"
        if zh
        else "These are historical official screenshots with sensitive values redacted. The original name is Dify tutorial; they show shared key steps, not execution in this host. See assets.json for source and dates.\n"
    )
    text += f"\n## 3. {'在宿主配置密钥' if zh else 'Configure credentials in this host'}\n\n{profile['credential_location_zh' if zh else 'credential_location']}\n\n"
    if profile.get("host_image_url"):
        if urlsplit(profile["host_image_url"]).scheme != "https":
            raise ValueError("host_image_url must be HTTPS")
        if not profile.get("host_image_date") or not profile.get("host_image_source"):
            raise ValueError(
                "host images require date and original source; do not invent host screenshots"
            )
        text += f"![{profile['host_image_caption']}]({profile['host_image_url']})\n\n{profile['host_image_date']} — {profile['host_image_source']}\n\n"
    else:
        text += (
            profile["host_image_caption_zh" if zh else "host_image_caption"] + "\n\n"
        )
    text += f"## 4. {'首用与同一个任务查询' if zh else 'First use and retrieve the same task'}\n\n{profile['first_use_zh' if zh else 'first_use']}\n\n```text\n{profile['same_task_query']}\n```\n\n"
    text += (
        "pending 时只查询同一个 task ID，不重复生成。检查最终状态与媒体 URL 后，再独立核对账单；绿色节点或退出码不能代替最终成功。\n\n## 常见问题\n\n401/403：核对原始Key、应用与服务权限。400：核对本服务模型/参数。429：等待并降并发，不自动增加付费重试。5xx/超时：先查原task/trace再决定是否重发。不要在提示词、日志、Git、截图或支持工单中放密钥。\n"
        if zh
        else "While pending, query the same task ID; do not submit another generation. Check the terminal result/media URL, then verify the usage record separately. A green node or exit code is not final service success.\n\n## Troubleshooting\n\n401/403: check the raw key and application/service access. 400: check this service's exact model/parameters. 429: wait and reduce concurrency, without automatic paid retries. 5xx/timeout: inspect the original task/trace before resubmitting. Never expose keys in prompts, logs, Git, screenshots or support requests.\n"
    )
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--language", choices=("en", "zh-CN"), default="en")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(render(json.loads(args.profile.read_text()), args.language))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
