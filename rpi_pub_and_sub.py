"""EE 250L Lab 05 Starter Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

# Team Members: I worked alone
# Github Repository: https://github.com/usc-ee250-fall2024/mqtt-new

import paho.mqtt.client as mqtt
import time

import sys
sys.path.append('../../Software/Python/')
sys.path.append('../../Software/Python/grove_rgb_lcd')
from grovepi import *
from grove_rgb_lcd import *

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("kyrashi/led")
    client.message_callback_add("kyrashi/led", custom_callback_led)
    client.subscribe("kyrashi/lcd")
    client.message_callback_add("kyrashi/lcd", custom_callback_lcd)


#default message callback
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

#custom callbacks
def custom_callback_led(client, userdata, message):
    str_message = str(message.payload, "utf-8")

    if str_message == "LED_ON":
        digitalWrite(led_port,1)	
        time.sleep(1)

    if str_message == "LED_OFF":
        digitalWrite(led_port,0)	
        time.sleep(1)

def custom_callback_lcd(client, userdata, message):
    str_message = str(message.payload, "utf-8")
    setText_norefresh(str_message)


if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="broker.hivemq.com", port=1883, keepalive=60)
    client.loop_start()

    #configure sensors
    ranger_port = 2 #port D2
    led_port = 3 #port D3
    button_port = 4 #port D4
    pinMode(led_port,"OUTPUT")
    pinMode(button_port,"INPUT")
    

    while True:
        time.sleep(1)

        try:
            distance = ultrasonicRead(ranger_port) #read ultrasonic sensor
            client.publish("kyrashi/ultrasonicRanger", distance)

            but = digitalRead(button_port) #read button
            if but: 
                client.publish("kyrashi/button", "Button pressed!")
        

        except Exception as e:
            print ("Error:{}".format(e))
            

