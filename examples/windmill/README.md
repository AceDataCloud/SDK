# Windmill scripts for Ace Data Cloud

Import the Python scripts as **Common Scripts** and use the existing [Ace Data Cloud resource type](https://hub.windmill.dev/resource_types/661/ace_data_cloud). Store the application token in a Windmill secret and reference that secret from the resource. Choose resources with access to the operations used by each script.

| Script | Inputs | Output |
| --- | --- | --- |
| [Retrieve a media task](media/get_task.py) | Service, original task ID and the resource that owns it | Finish time and the native result for Suno, Nano Banana, GPT Image, Seedance, Kling, Veo, Seedream, Flux, Midjourney, Hailuo, Fish Audio, Wan or Luma. Re-run the lookup to check progress. |
| [Create a search brief](search/brief.py) | Query, Google Search resource, Chat Completions resource and public model ID | Source snippets and short findings. Each citation URL comes directly from a search result. |
| [Retrieve an ACE Music task](acemusic/) | ACE Music resource and original task ID | Group status and individual audio tracks. |

A media task may contain private asset URLs. Limit access to the Windmill run history accordingly. A finished task may include an error or partial delivery, so inspect its service-specific response before consuming an asset.

The brief calls Google Search once and calls the selected model once if usable organic snippets are available. Each service charges its normal rate. The same saved resource can be selected for both inputs if it has access to both endpoints. Use a public model ID that supports [Chat Completions](../../python/README.md). The brief uses the returned snippets and does not fetch or verify the linked pages.
