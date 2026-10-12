# Connect AceDataCloud to Zapier

This guide is a draft for the private **Create Chat Response** action. The integration is not yet listed in the Zapier App Directory. Follow these steps after an AceDataCloud administrator has given your account access to a private version.

## Get an API token

1. Open [AceDataCloud Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=zapier_help_api_key). Sign in or register first.
2. Find **General application**. If it does not exist, choose **Initialize General Application**. A general application's key can use services available to your account. A dedicated application's key is limited to that service; make sure your application can access the model you plan to use.
3. Open **Keys / Manage Keys → Create**, name the key `Zapier`, and review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Allow the chat operation you will use. Copy only the API Key / API Token value, without quotes or a `Bearer ` prefix. A platform account-management token does not replace this API token.
4. Check [current model pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=zapier_help_pricing) and your application's balance. Any trial allowance is whatever your account currently displays.

![Copy an API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key and review its restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the token in Zapier's account connection. Keep it out of prompts, Zap names, screenshots, shared workflows, and support messages. A separately named key lets you rotate or revoke Zapier access independently.

## Connect and create a response

1. In the Zap editor, select the private AceDataCloud integration and **Create Chat Response**.
2. Add a connection. Paste the raw token into **API token** and enter a short label such as `Work` in **Connection name**. The label identifies your connection and is not sent to AceDataCloud. Connecting checks the token without charging for a chat response.
3. Choose **Model** from the current chat catalog. A model's presence in the picker does not guarantee access for your particular token.
4. Enter or map **Prompt** from an earlier step. For example, map a short note and ask: `Summarize this note in one sentence: {{note}}`. Optional **System instructions** can request a tone or format. **Max completion tokens** limits output for models that support that parameter; it does not cap input length or total cost.
5. **Test** sends a real chat request and uses your AceDataCloud balance. Check the response text before proceeding. When the Zap is turned on, each triggered run also uses balance. A continuously scheduled trigger can incur repeated charges; turn it off after a one-run acceptance test.
6. Map **Response text** to a later step, such as a field in a document or worksheet. **Response ID**, **Model**, **Finish reason**, token counts, and **Created at** are also available when returned by the model.

The action handles text only. It does not support images, tools, streaming, or conversation history. A model refusal is shown as response text. An empty response fails visibly.

## Pricing and retries

AceDataCloud usage and Zapier tasks are billed by their respective products. Connecting and loading the model picker do not generate a paid chat response. Both the Zap editor's Test button and an enabled Zap action consume AceDataCloud balance. Cost depends on the model, input and output tokens, and your current package rate.

A rate limit asks Zapier to retry after a delay. A timeout or failed run can leave the completion outcome uncertain. Before replaying, check the run's timestamp, response or reference ID, and your [AceDataCloud usage records](https://platform.acedata.cloud/console?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=zapier_help_usage). Replaying a chat request may create another response and another charge. Do not assume that a failed Zap means no AceDataCloud usage.

## Fix a connection or failed step

| What you see | What to check |
| --- | --- |
| Token cannot be verified / reconnect | Copy the complete raw token; check expiration, key usage limit, and application access. Update the connection after rotating a key. |
| Token cannot use Chat Completions | Use a general application or a dedicated application/key that permits the selected chat service and operation. |
| Insufficient balance | Check the application's balance and current package. |
| Rejected request / unavailable model | Check the selected model and prompt; refresh the picker. If set, confirm that the model supports Max completion tokens. |
| Rate limit | Let Zapier's delayed retry finish; review Zap History before manually replaying. |
| No chat text / uncertain failure | Check Zap History and AceDataCloud usage for the same time window before replaying. |

For unresolved issues, contact [support@acedata.cloud](mailto:support@acedata.cloud) with the response ID or reference ID, model, and approximate run time. Never include your API token or private prompt. See our [privacy policy](https://docs.acedata.cloud/en/resources/privacy), [terms](https://docs.acedata.cloud/en/resources/terms), and [support information](https://docs.acedata.cloud/en/resources/support).
