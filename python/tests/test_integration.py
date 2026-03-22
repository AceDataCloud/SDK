"""Integration tests for AceDataCloud Python SDK.

These tests run against the live API. Set these in .env (repo root) or environment:
  - ACEDATACLOUD_API_TOKEN      — API token for api.acedata.cloud
  - ACEDATACLOUD_PLATFORM_TOKEN — Platform token for platform.acedata.cloud (optional)

Usage:
    cd python
    pip install -e ".[test]" python-dotenv
    pytest tests/test_integration.py -v -s
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

# Load .env from repo root
_env_path = Path(__file__).resolve().parents[2] / ".env"
if _env_path.exists():
    from dotenv import load_dotenv

    load_dotenv(_env_path)

from acedatacloud import AceDataCloud, AsyncAceDataCloud
from acedatacloud._runtime.errors import APIError

TOKEN = os.environ.get("ACEDATACLOUD_API_TOKEN", "")
PLATFORM_TOKEN = os.environ.get("ACEDATACLOUD_PLATFORM_TOKEN", "")
pytestmark = pytest.mark.skipif(not TOKEN, reason="ACEDATACLOUD_API_TOKEN not set")


# ── Fixtures ──────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def client():
    c = AceDataCloud(api_token=TOKEN)
    yield c
    c.close()


@pytest.fixture(scope="module")
def platform_client():
    """Client with platform token for platform.acedata.cloud APIs."""
    if not PLATFORM_TOKEN:
        pytest.skip("ACEDATACLOUD_PLATFORM_TOKEN not set")
    c = AceDataCloud(api_token=PLATFORM_TOKEN)
    yield c
    c.close()


@pytest.fixture(scope="module")
def async_client():
    return AsyncAceDataCloud(api_token=TOKEN)


# ══════════════════════════════════════════════════════════════════════
# OpenAI-compatible: Chat Completions
# ══════════════════════════════════════════════════════════════════════


class TestOpenAIChatCompletions:
    def test_basic_completion(self, client):
        """Test a simple chat completion request."""
        result = client.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say hello in one word."}],
            max_tokens=10,
        )
        assert "choices" in result
        assert len(result["choices"]) > 0
        assert result["choices"][0]["message"]["content"]
        assert result["choices"][0]["message"]["role"] == "assistant"
        print(f"  Response: {result['choices'][0]['message']['content']}")

    def test_completion_with_system_message(self, client):
        """Test completion with system + user messages."""
        result = client.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful math tutor. Reply concisely."},
                {"role": "user", "content": "What is 2+3?"},
            ],
            max_tokens=20,
        )
        content = result["choices"][0]["message"]["content"]
        assert "5" in content
        print(f"  Response: {content}")

    def test_completion_with_temperature(self, client):
        """Test completion with temperature parameter."""
        result = client.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say yes or no."}],
            max_tokens=5,
            temperature=0,
        )
        assert result["choices"][0]["message"]["content"]

    def test_streaming_completion(self, client):
        """Test streaming chat completion."""
        stream = client.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Count from 1 to 3."}],
            max_tokens=30,
            stream=True,
        )
        chunks = list(stream)
        assert len(chunks) > 0
        # Collect streamed content
        content_parts = []
        for chunk in chunks:
            if "choices" in chunk and chunk["choices"]:
                delta = chunk["choices"][0].get("delta", {})
                if "content" in delta:
                    content_parts.append(delta["content"])
        full_content = "".join(content_parts)
        assert full_content
        print(f"  Streamed: {full_content}")

    def test_multiple_models(self, client):
        """Test with different models."""
        for model in ["gpt-4o-mini", "claude-3-5-haiku-20241022"]:
            result = client.openai.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Reply with just the word 'ok'."}],
                max_tokens=5,
            )
            assert result["choices"][0]["message"]["content"]
            print(f"  {model}: {result['choices'][0]['message']['content']}")

    def test_usage_info(self, client):
        """Test that usage information is returned."""
        result = client.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5,
        )
        assert "usage" in result
        assert result["usage"]["prompt_tokens"] > 0
        assert result["usage"]["total_tokens"] > 0
        print(f"  Usage: {result['usage']}")


# ══════════════════════════════════════════════════════════════════════
# OpenAI-compatible: Responses API
# ══════════════════════════════════════════════════════════════════════


class TestOpenAIResponses:
    def test_basic_response(self, client):
        """Test OpenAI Responses API with string input."""
        result = client.openai.responses.create(
            model="gpt-4o-mini",
            input="What is the capital of France? Reply in one word.",
        )
        assert "output" in result
        print(f"  Response ID: {result.get('id')}")

    def test_response_with_messages(self, client):
        """Test Responses API with structured message input."""
        result = client.openai.responses.create(
            model="gpt-4o-mini",
            input=[
                {"role": "user", "content": "Say hello."},
            ],
        )
        assert "output" in result

    def test_streaming_response(self, client):
        """Test streaming Responses API."""
        stream = client.openai.responses.create(
            model="gpt-4o-mini",
            input="Count from 1 to 3.",
            stream=True,
        )
        chunks = list(stream)
        assert len(chunks) > 0
        print(f"  Received {len(chunks)} stream events")


# ══════════════════════════════════════════════════════════════════════
# Google Search (SERP)
# ══════════════════════════════════════════════════════════════════════


class TestSearch:
    def test_basic_search(self, client):
        """Test basic Google search."""
        result = client.search.google(query="Python programming language")
        assert "organic" in result or "results" in result or "data" in result
        print(f"  Keys: {list(result.keys())}")

    def test_search_with_params(self, client):
        """Test search with country and language parameters."""
        result = client.search.google(
            query="weather today",
            country="us",
            language="en",
        )
        assert result  # Should return some data

    def test_news_search(self, client):
        """Test Google News search."""
        result = client.search.google(
            query="artificial intelligence",
            type="news",
        )
        assert result
        print(f"  Keys: {list(result.keys())}")

    def test_image_search(self, client):
        """Test Google Image search."""
        result = client.search.google(
            query="cute cats",
            type="images",
        )
        assert result
        print(f"  Keys: {list(result.keys())}")


# ══════════════════════════════════════════════════════════════════════
# Image Generation (NanoBanana)
# ══════════════════════════════════════════════════════════════════════


class TestImages:
    def test_generate_async_task(self, client):
        """Test image generation returns a task (no wait)."""
        result = client.images.generate(
            prompt="A cute cartoon cat sitting on a rainbow",
        )
        # Should return task info or direct result
        assert result
        assert "task_id" in result or "data" in result
        print(f"  Keys: {list(result.keys())}")
        if "task_id" in result:
            print(f"  Task ID: {result['task_id']}")

    def test_generate_with_wait(self, client):
        """Test image generation with wait=True (polls until complete)."""
        try:
            result = client.images.generate(
                prompt="A simple red circle on white background",
                wait=True,
                poll_interval=5.0,
                max_wait=300.0,
            )
            assert result
            if "data" in result:
                assert len(result["data"]) > 0
                print(f"  Generated {len(result['data'])} image(s)")
                for item in result["data"]:
                    if "image_url" in item:
                        print(f"  URL: {item['image_url'][:80]}...")
        except Exception as e:
            if "did not complete" in str(e):
                pytest.skip(f"Image generation timed out (upstream slow): {e}")
            raise


# ══════════════════════════════════════════════════════════════════════
# Audio Generation (Suno)
# ══════════════════════════════════════════════════════════════════════


class TestAudio:
    def test_generate_async_task(self, client):
        """Test audio generation returns a task (no wait)."""
        result = client.audio.generate(
            prompt="A cheerful pop song about coding",
        )
        assert result
        assert "task_id" in result or "data" in result
        print(f"  Keys: {list(result.keys())}")
        if "task_id" in result:
            print(f"  Task ID: {result['task_id']}")


# ══════════════════════════════════════════════════════════════════════
# Video Generation (Sora)
# ══════════════════════════════════════════════════════════════════════


class TestVideo:
    def test_generate_async_task(self, client):
        """Test video generation returns a task (no wait)."""
        try:
            result = client.video.generate(
                prompt="A sunset over the ocean, time-lapse style",
            )
            assert result
            assert "task_id" in result or "data" in result
            print(f"  Keys: {list(result.keys())}")
            if "task_id" in result:
                print(f"  Task ID: {result['task_id']}")
        except APIError as e:
            pytest.skip(f"Video API not available: {e}")


# ══════════════════════════════════════════════════════════════════════
# Task Retrieval
# ══════════════════════════════════════════════════════════════════════


class TestTasks:
    def test_get_task_suno(self, client):
        """Test retrieving a Suno task (triggers task creation first)."""
        # First create a task
        gen_result = client.audio.generate(prompt="A short instrumental jingle")
        task_id = gen_result.get("task_id")
        if task_id:
            result = client.tasks.get(task_id, service="suno")
            assert result
            print(f"  Task status: {result.get('response', {}).get('status', 'unknown')}")
        else:
            pytest.skip("No task_id returned from audio generation")

    def test_get_task_nano_banana(self, client):
        """Test retrieving a NanoBanana task."""
        gen_result = client.images.generate(prompt="A blue square")
        task_id = gen_result.get("task_id")
        if task_id:
            result = client.tasks.get(task_id, service="nano-banana")
            assert result
            print(f"  Task status: {result.get('response', {}).get('status', 'unknown')}")
        else:
            pytest.skip("No task_id returned from image generation")


# ══════════════════════════════════════════════════════════════════════
# Platform APIs
# ══════════════════════════════════════════════════════════════════════


class TestPlatform:
    def test_config_get(self, platform_client):
        """Platform configuration retrieval."""
        result = platform_client.platform.config.get()
        assert result
        print(f"  Config keys: {list(result.keys())}")

    def test_models_list(self, platform_client):
        """List available models."""
        result = platform_client.platform.models.list()
        assert result
        print(f"  Keys: {list(result.keys())}")

    def test_applications_list(self, platform_client):
        """List applications."""
        result = platform_client.platform.applications.list()
        assert result
        assert "count" in result or "results" in result
        print(f"  Count: {result.get('count', len(result.get('results', [])))}")

    def test_credentials_list(self, platform_client):
        """List credentials."""
        result = platform_client.platform.credentials.list()
        assert result
        print(f"  Count: {result.get('count', len(result.get('results', [])))}")


# ══════════════════════════════════════════════════════════════════════
# Async Client
# ══════════════════════════════════════════════════════════════════════


class TestAsyncClient:
    @pytest.mark.asyncio
    async def test_async_chat_completion(self, async_client):
        """Test async chat completion."""
        result = await async_client.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say hello in one word."}],
            max_tokens=10,
        )
        assert "choices" in result
        assert result["choices"][0]["message"]["content"]
        print(f"  Async response: {result['choices'][0]['message']['content']}")

    @pytest.mark.asyncio
    async def test_async_search(self):
        """Async Google search."""
        async with AsyncAceDataCloud(api_token=TOKEN) as ac:
            result = await ac.search.google(query="Python SDK")
            assert result
            print(f"  Async search keys: {list(result.keys())}")


# ══════════════════════════════════════════════════════════════════════
# File Upload
# ══════════════════════════════════════════════════════════════════════


class TestFiles:
    def test_upload_bytes(self, platform_client):
        """Upload bytes content."""
        content = b"Hello, this is a test file for SDK integration testing."
        result = platform_client.files.upload(content, filename="test.txt")
        assert result
        print(f"  Upload result keys: {list(result.keys())}")
        if "url" in result:
            print(f"  File URL: {result['url'][:80]}...")

    def test_upload_from_path(self, platform_client, tmp_path):
        """Upload from a file path."""
        test_file = tmp_path / "test_upload.txt"
        test_file.write_text("Integration test file content")
        result = platform_client.files.upload(str(test_file))
        assert result
        print(f"  Upload result keys: {list(result.keys())}")


# ══════════════════════════════════════════════════════════════════════
# Error Handling
# ══════════════════════════════════════════════════════════════════════


class TestErrorHandling:
    def test_invalid_model(self, client):
        """Error response for invalid model."""
        with pytest.raises(APIError):
            client.openai.chat.completions.create(
                model="nonexistent-model-xyz",
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5,
            )

    def test_auth_error(self):
        """Authentication error with bad token."""
        bad_client = AceDataCloud(api_token="invalid-token-12345", max_retries=0)
        with pytest.raises(APIError):
            bad_client.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5,
            )
        bad_client.close()
