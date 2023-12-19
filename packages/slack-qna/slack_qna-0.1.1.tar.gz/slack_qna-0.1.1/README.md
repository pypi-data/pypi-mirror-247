# Slack Q&A

An easy plug-and-use library for developing Slack BOT that serves a Q&A-like use case.

For NodeJS version, please see https://github.com/lokwkin/slack-qna-node

## Description

High level flow:
1. User messages this BOT via either:
    1. Direct Message
    2. Mention in Channel
    3. Slack Command
2. The BOT shows a loading reaction to the message.
3. The BOT relays user's message to your custom handler, and expect for a result either in `Text`, `File` or `Image` type.
4. The BOT reply the user's message in Slack Thread.
5. The BOT also shows a success reaction to the message.

Note:
- This BOT uses Slack's Socket Mode instead of Webhook mode for slack connection, so it does not require an exposed public endpoint. But your services need to be long running.

## Sample use cases

#### Use with ChatGPT (Text Response)
##### Loading
<img src="./docs/chatgpt-a.png" width="50%">

##### Reply
<img src="./docs/chatgpt-b.png" width="50%">

#### Use with Dall-E (Image Response)
##### Loading
<img src="./docs/dalle-a.png" width="50%">

##### Reply
<img src="./docs/dalle-b.png" width="50%">

## Usage

### Install
```
pypi install slack-qna
```

```python
from slack_qna.slack_qna import SlackQna
from slack_qna.schema import IncomingMessage, CommandHook, Reactions

slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
slack_app_token = os.getenv("SLACK_APP_TOKEN")
bot_user_id = os.getenv("SLACK_BOT_USER_ID")

slackQnaBot = SlackQna(slack_bot_token, slack_app_token, bot_user_id, Reactions(
            loading="loading",
            success="white_check_mark",
            failed="x"
        ))

def my_handler(message: IncomingMessage):
    return "Hi there"

slackQnaBot.register_handler(CommandHook(is_sync=True, data_type='text', handler=my_handler))
slackQnaBot.listen(direct_message=True, mention=True)
```

### Slack Setup
1. Register an Slack App in portal https://api.slack.com/
2. "Socket Mode" -> Enable Socket Mode
3. "OAuth & Permissions" -> "Bot Token Scopes" -> Grant these permissions: `app_mentions:read`, `channels:history`, `chat:write`, `im:history`, `im:write`, `reactions:write`, `groups:history`, `files:write`
4. "Event Subscription" -> "Enable Event" -> "Subscribe to bot events" -> Add `message.im` and `app_mention` --> "save"
5. "App Home" -> "Message Tab" -> Enable "Allow users to send Slash commands and messages from the messages tab"
6. Install bot to your workspace
7. Obtain your Bot Token from "OAuth & Permissions" > "Bot User OAuth Token"
8. Obtain your App Token from "Basic Information" > "App Level Token"
9. "Install App" -> Reinstall to workspace if neccessary