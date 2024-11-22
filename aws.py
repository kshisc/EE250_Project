import json
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import boto3
import grovepi

# AWS IoT Core Configuration
THING_NAME = "RPi"
CERTIFICATE_PATH = "RPi.cert.pem"
PRIVATE_KEY_PATH = "RPi.private.key"
CA_PATH = "root-CA.crt"
ENDPOINT = "alqez4fmof1su-ats.iot.us-east-1.amazonaws.com"

# AWS IoT SiteWise Client
sitewise_client = boto3.client("iotsitewise", region_name="us-east-1")

# GrovePi Sensor Configuration
temperature_sensor = 4  # Connect sensor to port D4
grovepi.pinMode(temperature_sensor, "INPUT")

# MQTT Client Setup
mqtt_client = AWSIoTMQTTClient(THING_NAME)
mqtt_client.configureEndpoint(ENDPOINT, 8883)
mqtt_client.configureCredentials(CA_PATH, PRIVATE_KEY_PATH, CERTIFICATE_PATH)
mqtt_client.connect()

# Function to send data to AWS IoT SiteWise
def send_to_sitewise(asset_id, property_id, value):
    timestamp = int(time.time() * 1000)  # Epoch in milliseconds
    sitewise_client.batch_put_asset_property_value(
        entries=[
            {
                "entryId": "1",
                "assetId": asset_id,
                "propertyId": property_id,
                "propertyValues": [
                    {
                        "value": {"doubleValue": value},
                        "timestamp": {"timeInSeconds": timestamp // 1000, "offsetInNanos": (timestamp % 1000) * 1_000_000},
                        "quality": "GOOD",
                    }
                ],
            }
        ]
    )

# Main Loop
ASSET_ID = "30195743-fec1-4685-83b6-258326029aa8"
PROPERTY_ID_TEMP = "Yee288f99-f1dc-4124-a346-c85e12f6c305"

try:
    while True:
        # Read sensor data
        temperature = grovepi.analogRead(temperature_sensor)
        
        # Send to AWS IoT SiteWise
        send_to_sitewise(ASSET_ID, PROPERTY_ID_TEMP, temperature)
        
        print(f"Temperature sent: {temperature}")
        time.sleep(5)

except KeyboardInterrupt:
    print("Exiting...")
    mqtt_client.disconnect()