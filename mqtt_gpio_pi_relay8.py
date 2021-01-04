import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

#Initialize MQTT Varaibles
client_id="PI-LAB1"
broker="192.168.0.127"
port=8883
subs_topic_dict={
                    "Relay/r1_write":25,
                    "Relay/r2_write":8,
                    "Relay/r3_write":7,
                    "Relay/r4_write":1,
                    "Relay/r5_write":12,
                    "Relay/r6_write":16,
                    "Relay/r7_write":20,
                    "Relay/r8_write":21,
                    }
pub_topic_dict={
                    "Relay/r1_read":25,
                    "Relay/r2_read":8,
                    "Relay/r3_read":7,
                    "Relay/r4_read":1,
                    "Relay/r5_read":12,
                    "Relay/r6_read":16,
                    "Relay/r7_read":20,
                    "Relay/r8_read":21,
                    }

#Initialize GPIO 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Pin List
pinlist = [21,20,16,12,1,7,8,25]
#25 - Relay 1
#8 - Relay 2
#7 - Relay 3
#1 - Relay 4
#12 - Relay 5
#16 - Relay 6
#20 - Relay 7
#21 - Relay 8
GPIO.setup(pinlist, GPIO.OUT)

#Connect to Broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[+]Connected to MQTT Broker [+]")
    else:
        print("[!] Failed to connect, return code %d\n", rc)

#Publish Data
def mqtt_publish(client):
    while client.loop()==0:
        for publish_topic,gpio_pin in pub_topic_dict.items():
            current_status=GPIO.input(gpio_pin)
            if current_status==0:  
                client.publish(publish_topic, "ON")
                #print("[#] Relay "+str(gpio_pin)+" Status: ON")
            else:
                client.publish(publish_topic, "OFF")
                #print("[x] Relay "+str(gpio_pin)+" Status: OFF")

#On receving the message
def on_message(client_subs, userdata, message):
    print("Message Received: " +message.topic+" - "+str(message.payload.decode("utf-8")))
    topic=message.topic
    msg=message.payload.decode("utf-8")
    gpio_pin=subs_topic_dict[topic]
    if msg=="ON":
        GPIO.output(gpio_pin,GPIO.LOW)
    elif msg=="OFF":
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
client.subscribe([("Relay/r1_write",0),("Relay/r2_write",0),("Relay/r3_write",0),("Relay/r4_write",0),("Relay/r5_write",0),("Relay/r6_write",0),("Relay/r7_write",0),("Relay/r8_write",0)])
client.on_message=on_message
#Publish Topic
mqtt_publish(client)
#MQTT Loop
client.loop_forever()
#GPIO Clean up
GPIO.cleanup()