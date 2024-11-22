from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import boto3
import time
import grovepi

# Create a boto3 client for IoT SiteWise
sitewise_client = boto3.client('iotsitewise')

# AWS IoT configuration
mqtt_client = AWSIoTMQTTClient("RPi")
mqtt_client.configureEndpoint("alqez4fmof1su-ats.iot.us-east-1.amazonaws.com", 8883)
mqtt_client.configureCredentials("root-CA.crt", "RPi.private.key", "RPi.cert.pem")
# Connect to AWS IoT Core
mqtt_client.connect()

# GrovePi sensor setup
temp_sensor = 4  # digital port 4
light_sensor = 0 # analog port 0
led = 3 # digital port 3

threshold = 10 # brightness threshold
grovepi.pinMode(light_sensor,"INPUT")
grovepi.pinMode(led,"OUTPUT")

entry_id = 1
asset_id = 'f61fd66e-ccd5-4eb3-9bd8-9cf88ce84c92'

while True:
    try:
        [temp,humidity] = grovepi.dht(temp_sensor,0)  # blue sensor
        sensor_value = grovepi.analogRead(light_sensor)
        resistance = (float)(1023 - sensor_value) * 10 / sensor_value
        if resistance > threshold:
            grovepi.digitalWrite(led,0) # LED off
        else:
            grovepi.digitalWrite(led,1) # LED on

        properties = [
            {
                'propertyId': 'ee288f99-f1dc-4124-a346-c85e12f6c305', # temperature
                'value': { 'doubleValue': temp },  
            },
            {
                'propertyId': 'dd024614-b04b-4820-91e9-48442c8982bf',  # humidity
                'value': { 'doubleValue': humidity },  # Value for Property 2
            },
            {
                'propertyId': '85b95849-2117-4eff-844a-c70f0473308b',  # light
                'value': { 'doubleValue': resistance },  # Value for Property 3
            }
        ]

        # Create the entries list for the batch request
        entries = []
        for prop in properties:
            entries.append({
                'assetId': asset_id,
                'entryId': str(entry_id),
                'propertyId': prop['propertyId'],
                'propertyValues': [
                    {
                        'value': prop['value'],
                        'timestamp': {
                            'timeInSeconds': int(time.time())
                        }
                    }
                ]
            })
            entry_id += 1  # Increment entry ID for each property

        # Call the BatchPutAssetPropertyValue API
        response = sitewise_client.batch_put_asset_property_value(
            entries=entries
        )

        print("Data published:", entry_id)
        time.sleep(5)  # Adjust as needed
        entry_id += 1
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
