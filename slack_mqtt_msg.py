import paho.mqtt.client as mqtt
import slack_sdk as slack_web
from slack_sdk.errors import SlackApiError

#Slack variable
slack_bot_token='xoxp-XXXX'
slack_client= slack_web.WebClient(token=slack_bot_token)
slack_channel = "#test"
#MQTT Variables
mqtt_topic_sub = "test-write"

#MQTT OnConnection
def on_connect(self,client, userdata, rc):
        try:
                print("Connected with result code " + str(rc) + " to topic " + mqtt_topic_sub)
                self.subscribe(mqtt_topic_sub)
        except Exception as err:
                print(err)

#MQTT On Message Received
def on_message(client1, userdata, msg):
        try:
                print("Topic: "+msg.topic + "\tMessage: " + str(msg.payload))
                response = slack_client.chat_postMessage(channel=slack_channel,text=str(msg.payload))
        except SlackApiError as e:
                print(e)
#MQTT Connection
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("127.0.0.1", 1883,8000)
mqtt_client.loop_forever()
