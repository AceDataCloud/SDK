#requirements:
#acedatacloud==2026.11.27.2

from typing import Literal, TypedDict

from acedatacloud import AceDataCloud


class ace_data_cloud(TypedDict):
    token: str


def main(
    connection: ace_data_cloud,
    service: Literal[
        "Suno", "Nano Banana", "GPT Image", "Seedance", "Kling", "Veo",
        "Seedream", "Flux", "Hailuo", "Fish Audio", "Wan", "Luma",
    ],
    task_id: str,
) -> dict:
    """Read an existing media task owned by this application."""
    services = {
        "Suno": "suno", "Nano Banana": "nano-banana", "GPT Image": "openai",
        "Seedance": "seedance", "Kling": "kling", "Veo": "veo", "Seedream": "seedream",
        "Flux": "flux", "Hailuo": "hailuo",
        "Fish Audio": "fish", "Wan": "wan", "Luma": "luma",
    }
    task_id = task_id.strip()
    token = connection["token"].strip()
    if not token or not task_id or service not in services:
        raise ValueError("Select a supported service, a resource and an existing task ID.")

    with AceDataCloud(api_token=token, base_url="https://api.acedata.cloud", max_retries=0) as client:
        record = client.tasks.get(task_id, service=services[service])
    if not record or record.get("id") != task_id:
        raise LookupError("No matching task was returned for this service and application.")
    return {
        "service": service,
        "task_id": task_id,
        "finished_at": record.get("finished_at"),
        "response": record.get("response"),
    }
