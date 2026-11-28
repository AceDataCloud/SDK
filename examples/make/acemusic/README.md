# ACE Music for Make

Open `makecomapp.json` with the Make Apps SDK extension. Bind your own Make test-app origin to this local manifest and synchronize the code files in the app editor. The checked-in source has no production origin, application IDs, or credentials.

Sign in to [Applications](https://platform.acedata.cloud/console/applications) and open **General Application**. Click the copy button to the right of **API KEY**.

![API key in the General Application card](https://cdn.acedata.cloud/dvc3cg.jpg)

Paste the raw key into **AceDataCloud API token** in the Make connection. The key needs ACE Music access. The connection check reads one page of your task history.

The native modules support songs from an idea or custom lyrics, MP3 reference import, covering one owned track, blending two distinct compatible tracks, lyric writing, original-task retrieval, bulk lookup and paginated history. For a song, pick the model, enter a prompt, and submit once. Save `task_id` and map it to **Retrieve task (ACE Music)**. A successful upload delivers one reference track. A full song group can deliver two tracks. Completed tracks in a partially failed group remain available. Lyrics can return text immediately or a pending task ID.

Audio creation, reference imports and writing lyrics are separately priced. An uncertain submission should be reconciled in task history before retry. Task lookup is read-only. [API contract](https://github.com/AceDataCloud/ACEMusicAPI) · [中文使用说明](README.zh-CN.md)
