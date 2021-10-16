import slack_sdk as slack_web
from slack_sdk.errors import SlackApiError
#Slack API BOT Token
slack_bot_token='xoxb-84873741616-2612338309666-er43O1YOcK9iZvhCpTvh1LiA'
channel = "#test"
msg="Hello"
try:
        slack_client=slack_web.WebClient(token=slack_bot_token)
        response = slack_client.chat_postMessage(channel=channel,text=msg)
except SlackApiError as e:
        print(e)