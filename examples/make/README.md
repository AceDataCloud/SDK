# Make custom app POC

These JSON files define the minimum pieces of a Make custom app: Base, API-key Connection, and one action module. They are **editor snippets**, not an installable app package or a public Make listing.

1. In a Make developer account, create a private custom app named AceDataCloud.
2. Paste `connection-parameters.json` into the Connection's **Parameters** tab and `connection-communication.json` into **Communication**. The connection test calls the non-billable `/v1/models` route.
3. Paste `base.json` into **Base**. It sends the Bearer token in an Authorization header and sanitizes it from logs.
4. Add an **Action** module called **Send Chat Prompt** using that Connection. Paste `chat-parameters.json` into **Mappable Parameters** and `chat-communication.json` into **Communication**.
5. Create a private scenario, run one prompt with a valid AceDataCloud token, and verify `content` plus `total_tokens` in the output. Each run calls the billable Chat Completions API.

The POC was checked as JSON and against Make's published component structure. A live Make editor test, test scenario, and app review are still required before sharing it publicly. Keep the token in the Make Connection; do not put it in scenario inputs or exported snippets.
