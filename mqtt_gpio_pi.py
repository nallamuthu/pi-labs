import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

#Initialize MQTT Varaibles
client_id="PI-LAB1"
broker="192.168.x.x"
port=8883
subs_topic="Relay/r1_write"
publish_topic="Relay/r1_read"

#Initialize GPIO 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
gpio_pin=25
GPIO.setup(gpio_pin, GPIO.OUT)

#Connect to Broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[+]Connected to MQTT Broker [+]")
    else:
        print("[!] Failed to connect, return code %d\n", rc)

#Publish Data
def mqtt_publish(client):
    while client.loop()==0:
        current_status=GPIO.input(25)
        if current_status==0:
            client.publish(publish_topic, "ON")
            print("[#] Relay Status: ON")
        else:
            client.publish(publish_topic, "OFF")
            print("[x] Relay Status: OFF")
        time.sleep(5)

#On receving the message
def on_message(client_subs, userdata, message):
    print("Message Received: " +message.topic+" - "+str(message.payload.decode("utf-8")))
    topic=message.topic
    msg=message.payload.decode("utf-8")
    if topic==subs_topic and msg=="ON":
        GPIO.output(gpio_pin,GPIO.LOW)
    else:
        GPIO.output(gpio_pin,GPIO.HIGH)

#Initialize MQTT
def Initialize_mqtt():
    try:
        client = mqtt.Client(client_id)
        client.connect(broker, port)
        client.on_connect = on_connect
        return client
    except Exception as e:
        print(e)

#Initialize MQTT
client=Initialize_mqtt()
#Subscribe to Topic
client.subscribe(subs_topic)
client.on_message=on_message
#Publish Topic
mqtt_publish(client)
#MQTT Loop
client.loop_forever()
#GPIO Clean up
GPIO.cleanup()