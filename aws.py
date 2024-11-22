# import json
# import time
# from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
# import boto3
# import grovepi

# # AWS IoT Core Configuration
# THING_NAME = "RPi"
# CERTIFICATE_PATH = "RPi.cert.pem"
# PRIVATE_KEY_PATH = "RPi.private.key"
# CA_PATH = "root-CA.crt"
# ENDPOINT = "alqez4fmof1su-ats.iot.us-east-1.amazonaws.com"

# # AWS IoT SiteWise Client
# sitewise_client = boto3.client("iotsitewise", region_name="us-east-1")

# # GrovePi Sensor Configuration
# temperature_sensor = 4  # Connect sensor to port D4
# grovepi.pinMode(temperature_sensor, "INPUT")

# # MQTT Client Setup
# mqtt_client = AWSIoTMQTTClient(THING_NAME)
# mqtt_client.configureEndpoint(ENDPOINT, 8883)
# mqtt_client.configureCredentials(CA_PATH, PRIVATE_KEY_PATH, CERTIFICATE_PATH)
# mqtt_client.connect()

# # Function to send data to AWS IoT SiteWise
# def send_to_sitewise(asset_id, property_id, value):
#     timestamp = int(time.time() * 1000)  # Epoch in milliseconds
#     sitewise_client.batch_put_asset_property_value(
#         entries=[
#             {
#                 "entryId": "1",
#                 "assetId": asset_id,
#                 "propertyId": property_id,
#                 "propertyValues": [
#                     {
#                         "value": {"doubleValue": value},
#                         "timestamp": {"timeInSeconds": timestamp // 1000, "offsetInNanos": (timestamp % 1000) * 1_000_000},
#                         "quality": "GOOD",
#                     }
#                 ],
#             }
#         ]
#     )

# # Main Loop
# ASSET_ID = "f61fd66e-ccd5-4eb3-9bd8-9cf88ce84c92"
# PROPERTY_ID_TEMP = "ee288f99-f1dc-4124-a346-c85e12f6c305"

# try:
#     while True:
#         # Read sensor data
#         temperature = grovepi.analogRead(temperature_sensor)
        
#         # Send to AWS IoT SiteWise
#         send_to_sitewise(ASSET_ID, PROPERTY_ID_TEMP, temperature)
        
#         print(f"Temperature sent: {temperature}")
#         time.sleep(5)

# except KeyboardInterrupt:
#     print("Exiting...")
#     mqtt_client.disconnect()

import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import grovepi
import boto3

# Create a boto3 client for IoT SiteWise
client = boto3.client('iotsitewise')

# Define the entries you want to send in the batch

# GrovePi sensor setup
temp_sensor = 4  # digital port 4

# AWS IoT configuration
client = AWSIoTMQTTClient("RPi")
client.configureEndpoint("alqez4fmof1su-ats.iot.us-east-1.amazonaws.com", 8883)
client.configureCredentials("root-CA.crt", "RPi.private.key", "RPi.cert.pem")

client.configureOfflinePublishQueueing(-1)
client.configureDrainingFrequency(2)
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)

# Connect to AWS IoT Core
client.connect()

while True:
    try:
        [temp,humidity] = grovepi.dht(temp_sensor,0)  # blue sensor
        payload = {"temperature": temp, "timestamp": time.time()}
        # client.publish("grovepi/sensors", json.dumps(payload), 1)
        entries = [
            {
                'assetId': 'f61fd66e-ccd5-4eb3-9bd8-9cf88ce84c92',
                'propertyId': 'dd024614-b04b-4820-91e9-48442c8982bf',     # The property ID
                'value': {
                    'value': {
                        'doubleValue': temp         # The value to put (e.g., double, integer, string, etc.)
                    },
                    'timestamp': {
                        'timeInSeconds': int(time.time()),  # The timestamp in seconds (e.g., Unix timestamp)
                        'offsetInNanos': 0           # The timestamp offset in nanoseconds
                    }
                }
            },
        ]

        # Call the BatchPutAssetPropertyValue API
        response = client.batch_put_asset_property_value(
            entries=entries
        )

        print("Data published:", payload)
        time.sleep(5)  # Adjust as needed
    except KeyboardInterrupt:
        break
    except Exception as e:
        print("Error:", e)


# aws iotsitewise batch-put-asset-property-value --entries '[ 
#   {
    
#     "assetId": "f61fd66e-ccd5-4eb3-9bd8-9cf88ce84c92",
#     "entryId": "1236",
#     "propertyId": "dd024614-b04b-4820-91e9-48442c8982bf",
#     "propertyValues": [
#       {
#         "value": { "doubleValue": 25 },
#         "timestamp": { "timeInSeconds": 1732278759}
#       }
#     ]
#   }
# ]'

# aws sts assume-role \
#     --role-arn arn:arn:aws:iam::863518420748:role/service-role/new_role \
#     --role-session-name Session1
