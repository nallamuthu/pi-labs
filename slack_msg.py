import slack_sdk as slack_web
from slack_sdk.errors import SlackApiError
#Slack API BOT Token
slack_bot_token='xoxb-XXXX'
channel = "#test"
msg="Hello"
try:
        slack_client=slack_web.WebClient(token=slack_bot_token)
        response = slack_client.chat_postMessage(channel=channel,text=msg)
except SlackApiError as e:
        print(e)