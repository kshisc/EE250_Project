Team members: Kyra Shi

Intructions: 
1. Attach the GrovePi shield to the Raspberry Pi and connect the LED (D3), temperature/humidity sensor (D4), and light sensor (A0)
2. Turn on the RPi, connect to the network, and ssh into the RPi (pi@kyrashi.local)
3. Run aws.py code and view the sensor data on the aws dashboard: https://p-6992lnbr.app.iotsitewise.aws/projects/3f93d03c-2575-4993-b851-9bc89f2835e3
4. Run train.ipynb to see the ML prediction 

Libraries:
AWSIoTPythonSDK.MQTTLib (using MQTT to connect to AWS IOT Core)
boto3 (runs the API to put data in AWS SiteWise)
