# LangChain chat POC

Use the existing `langchain-openai` package to call AceDataCloud's OpenAI-compatible Chat Completions API. This example fixes the request mode to Chat Completions because LangChain can otherwise infer the Responses API from a model name. It disables automatic retries so a failed request is not silently repeated and billed again.

```bash
python3 -m pip install langchain-openai
export ACEDATACLOUD_API_TOKEN='your-token'
python3 chat.py 'Summarize this text in one sentence.'
```

The default endpoint is `https://api.acedata.cloud/v1` and the default model is `gpt-5.5`. Set `ACEDATACLOUD_MODEL` to a currently supported chat model if needed. Keep the token in an environment variable, never in the script or a repository. Each run makes one billable API request. The endpoint can be changed with `ACEDATACLOUD_BASE_URL` for a local mock or a staging environment.

This POC uses LangChain's existing adapter. A separate AceDataCloud LangChain package is only useful if it adds typed provider operations or task lifecycle handling that the OpenAI-compatible adapter cannot provide.
