# Use an ACE Music track in Canva or Adobe Express

These panels can submit a paid ACE Music task on an explicit click or import tracks from an existing, owned task. They display the group state and preserve the surviving track of a partial result. The application token is held only in the current panel and goes only to the Ace Data Cloud service endpoints. Audio is uploaded to the editor only after the user selects **Add track to design**. Source audio must be yours or licensed for use in your design.

Run `npm ci && npm test && npm run build` with Node 22 or later. For Canva, configure asset and design content write permissions, upload `dist/canva/app.js` and its matching English (US) translator file `dist/canva/messages_en.json` in the Developer Portal, and test in a design that supports audio. The code identifies generated audio as app-generated. For Adobe Express, test `dist/adobe` in the add-on developer sandbox, then zip its contents with `manifest.json` at the archive root and upload the ZIP to the public listing in Express. Adobe uses the manifest's `testId` during development and ignores it for marketplace submissions.

Sign in to [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and open **General Application**. If it is missing, select **Initialize General Application**. Click the copy button to the right of **API KEY**.

![API key in the General Application card](https://cdn.acedata.cloud/dvc3cg.jpg)

Paste the raw key into the design panel. It needs access to ACE Music. Enter the original task ID, preview an available track, then insert it. To create music, expand Create a soundtrack and select Generate with credits. Save the returned task ID and use Find tracks to query it. If the result is uncertain, check task history before retrying. ACE Music can return vocals; a publisher must not describe it as an instrumental-only generator. Test both a completed track and a pending task in a real editor before public submission.

In either panel, anyone can preview **Studio chimes** and add the six-second sample to a design without an Ace account or credits. Adobe Express loads the audio from the add-on package. This original synthesized cue is included under the repository license. Its upload uses Canva’s stock-asset AI disclosure. User-generated ACE Music tracks keep the app-generated disclosure.

## Import other media into Adobe Express

In **Import a media task**, choose the service that created the task, enter the matching application token and task ID, then select **Find media**. Suno imports audio, Nano Banana, GPT Image, Seedream and Flux import images, and Seedance, Kling, Veo and Hailuo import videos. Preview a result and select **Add to design** for that item. Use an existing task with HTTPS URL output accessible to the browser. The service selector clears the previous credentials. **ACE Music tracks and generation** retains the original music workflow.

For the Adobe Express public listing, upload the 144 × 144 px add-on icon from `adobe/icons/ace-media.png`. Express resizes it for the panel header and minimized module.
