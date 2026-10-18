# First-use materials for service integration maintainers

[简体中文](README_zh-CN.md)

Keep **Suno by Ace Data Cloud**, **Seedance by Ace Data Cloud**, **HappyHorse by Ace Data Cloud**, **GPT Image by Ace Data Cloud**, and **Nano Banana by Ace Data Cloud** discoverable by the service names users search for. This shared SDK supports their independently distributed integrations; it is not a marketplace listing or an LLM-provider registration by itself.

## Reuse an actual first-use flow

The [Suno Dify English guide](https://github.com/AceDataCloud/SunoDify/blob/main/README.md) and [Chinese guide](https://github.com/AceDataCloud/SunoDify/blob/main/readme/README_zh_Hans.md) show the model: verified install entry → register/sign in → Applications/General application → copy or create a dedicated API Key → exact host credential location → one first use → retrieve the same task ID → terminal output and troubleshooting.

Copy the structure, not the Dify menu names or its generation result into another host. Keep the service's official install URL, package/repository identity and exact commands. An Ace-maintained integration is not an official client from the model owner. Do not invent a default provider, search rank, native button or dedicated package.

## Render English and Chinese starting guides

[`profiles/suno-cli.json`](profiles/suno-cli.json) is a complete, no-cost CLI profile. [`suno-cli.en.md`](suno-cli.en.md) and [`suno-cli.zh-CN.md`](suno-cli.zh-CN.md) are rendered examples, not records of a paid generation.

```bash
python3 scripts/render_onboarding.py \
  --profile docs/integration-onboarding/profiles/suno-cli.json \
  --language en --output /tmp/suno-first-use.en.md
python3 scripts/render_onboarding.py \
  --profile docs/integration-onboarding/profiles/suno-cli.json \
  --language zh-CN --output /tmp/suno-first-use.zh-CN.md
```

A new profile must supply its verified install entry, exact host token field, the service's generation/task-query operations, first-use instructions and same-task commands. The renderer never installs, authenticates, creates accounts, stores a key, starts a server or calls a generation API.

The existing UTM contract is preserved: `utm_source`, `utm_medium=referral`, `utm_campaign=evergreen`, and service/host-specific `utm_content`. Shared GitHub/package README text uses `opensource`; a separately rendered PyPI/npm page may use `pypi`/`npm`. Do not append marketing tags to protocol endpoints or credential values. This utility does not authorize adding a new global source/channel rule.

## Real screenshot assets and their limits

- [Copy an application API key](assets/get-api-key-en.png)
- [Create a dedicated key](assets/create-api-key-en.png)
- [Source URLs, commit date and SHA-256](assets.json)

These two unmodified redacted images come from the Suno Dify tutorial commit `8d3d03570e73324220f111f7fe343da0792a8071`, archived 2026-10-08. Original capture time/frontend version is not established. The original “Dify tutorial” key name is an example; use the actual host's name. They prove only the shared platform credential step, not installation or execution in another host.

A host image must have an original source and date; the renderer refuses an image without them. If there is no real host capture, it prints the missing-evidence note. Do not generate a fake terminal or GUI to fill the gap. An edited official screenshot must be labeled “official screenshot edit, not actual execution”.

## Ownership and release boundaries

| Surface | Source of truth / owner | Consume here | Do not duplicate |
|---|---|---|---|
| Python/TypeScript/Go SDK | `AceDataCloud/SDK` | Typed client resources, current package metadata | Generated providers or routing in guide templates |
| Service CLI directory | `AceDataCloud/Clis/service-packages.json` | Real package identity, local help, published/source-only state | Unverified standalone repos or aliases |
| MCP packages | `AceDataCloud/MCPs`, existing MCP owner | Actual `pyproject.toml`, canonical service lifecycle, tool contract | Mirror source edits or another error-semantics PR |
| Skills | `AceDataCloud/Skills`, existing Skills owner | Current host recipe and service guide | A forked installer engine |
| API, credential, cost, UTM contract | PlatformBackend | Current required permissions and price links | New fallback, price, schema or global attribution rules |
| Each host plugin/node/provider | That host's dedicated repository/owner | This material + verified host steps | Calling local import or manual base URL “native/default” |

Public package metadata must identify Ace Data Cloud as the publisher and link the real repository. The [PyPA guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) and [npm package.json documentation](https://docs.npmjs.com/cli/v11/configuring-npm/package-json) explain keywords/description/source fields used for package discovery. Only relevant supported service names belong in them.

After a reviewed source change: build the package, inspect its metadata/README, publish through the existing release path, then read back the actual registry version and install it in a new environment. Source merge, package publication, official host listing, install, real generation, terminal media, unique bill and attributed signup/payment are separate receipts. Never treat package counts or downloads as acquisition revenue.
