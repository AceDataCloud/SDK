# Windmill scripts for Ace Data Cloud

Import the Python scripts as **Common Scripts** and use the existing [Ace Data Cloud resource type](https://hub.windmill.dev/resource_types/661/ace_data_cloud).

Sign in to [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and open **General Application**. If it is missing, select **Initialize General Application**. Click the copy button marked **1** beside **API KEY**.

![Button 1 copies the API key from General Application](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

Store the copied key in a Windmill secret and reference that secret from the resource. Choose resources with access to the operations used by each script.

| Script | Inputs | Output |
| --- | --- | --- |
| [Retrieve a media task](https://hub.windmill.dev/scripts/ace_data_cloud/23794/retrieve-a-media-task-ace_data_cloud) · [Source](media/get_task.py) | Service, original task ID and the resource that owns it | Finish time and the native result for Suno, Nano Banana, GPT Image, Seedance, Kling, Veo, Seedream, Flux, Hailuo, Fish Audio, Wan or Luma. Re-run the lookup to check progress. |
| [Create a search brief](https://hub.windmill.dev/scripts/ace_data_cloud/23795/create-a-source-linked-search-brief-ace_data_cloud) · [Source](search/brief.py) | Query, Google Search resource, Chat Completions resource and public model ID | Source snippets and short findings. Each citation URL comes directly from a search result. |
| [Retrieve an ACE Music task](acemusic/) | ACE Music resource and original task ID | Group status and individual audio tracks. |

A media task may contain private asset URLs. Limit access to the Windmill run history accordingly. A finished task may include an error or partial delivery, so inspect its service-specific response before consuming an asset.

The brief calls Google Search once and calls the selected model once if usable organic snippets are available. Each service charges its normal rate. The same saved resource can be selected for both inputs if it has access to both endpoints. Use a public model ID that supports [Chat Completions](../../python/README.md). The brief uses the returned snippets and does not fetch or verify the linked pages.
