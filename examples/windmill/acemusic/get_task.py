"""Retrieve an existing ACE Music task using a Windmill Resource."""
import json
from typing import TypedDict
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener


class AceDataCloud(TypedDict):
    token: str


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def main(ace_data_cloud: AceDataCloud, task_id: str) -> dict:
    task_id = task_id.strip()
    token = ace_data_cloud["token"].strip()
    if not task_id or not token:
        raise ValueError("An existing ACE Music task ID and an application token are required.")
    request = Request(
        "https://api.acedata.cloud/acemusic/tasks", method="POST",
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
        data=json.dumps({"action": "retrieve", "id": task_id}).encode(),
    )
    try:
        with build_opener(_NoRedirect()).open(request, timeout=30) as response:
            payload = json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"ACE Music task lookup returned HTTP {exc.code}.") from None
    inner = payload.get("response") or {}
    if payload.get("id") != task_id or inner.get("task_id") not in (None, task_id):
        raise ValueError("The response did not identify the requested task.")
    tracks = inner.get("data") or []
    return {
        "task_id": task_id, "state": payload.get("state") or payload.get("status"),
        "group_status": inner.get("status"),
        "tracks": [{key: item[key] for key in ("id", "title", "audio_url", "duration") if key in item}
                   for item in tracks if isinstance(item, dict)] if isinstance(tracks, list) else [],
    }
