# Suno by Ace Data Cloud: first use in CLI

This is an Ace Data Cloud integration for Suno, not an official client published by the model owner. Installing the integration and making a service request are separate steps. Use your own application API key.

## 1. Install from the correct entry

Open the [verified install entry](https://pypi.org/project/suno-cli/) and confirm the maintainer/source belongs to AceDataCloud.

```bash
python -m pip install suno-cli
suno --help
suno models
```

## 2. Register/sign in and create a key

Open [Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=suno_cli_readme_api_key), register/sign in, and choose **Initialize General Application** if needed. Copy its API Key or use **Manage Keys → Create** to name a separate key for this host.

Check model/service access, expiration, usage limits, balance and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=suno_cli_readme_pricing). If Allowed APIs is enabled, allow `/suno/audios`, `/suno/tasks`; task-query permission does not grant generation access. Copy only the raw token, without Bearer, quotation marks or spaces. A platform management token and a Discord proxy credential are different credentials.

![Copy the application key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![Create a dedicated key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

These are historical official screenshots with sensitive values redacted. The original name is Dify tutorial; they show shared key steps, not execution in this host. See assets.json for source and dates.

## 3. Configure credentials in this host

Set the raw token in ACEDATACLOUD_API_TOKEN in the environment launching the terminal command. Do not paste it into a prompt.

No CLI terminal screenshot is supplied by this shared template. Add an actual dated install/command/result capture before claiming this host flow is visually verified.

## 4. First use and retrieve the same task

The commands above only show local help and model references. Check current model/service access, price and balance before using the generation example in the package README. This template does not run a paid request.

```text
suno task <task-id>
suno wait <task-id> --interval 5
```

While pending, query the same task ID; do not submit another generation. Check the terminal result/media URL, then verify the usage record separately. A green node or exit code is not final service success.

## Troubleshooting

401/403: check the raw key and application/service access. 400: check this service's exact model/parameters. 429: wait and reduce concurrency, without automatic paid retries. 5xx/timeout: inspect the original task/trace before resubmitting. Never expose keys in prompts, logs, Git, screenshots or support requests.
