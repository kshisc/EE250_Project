# EE250_Project
Team members: Kyra Shi

Introduction: My project is a plant health monitor. It uses GrovePi sensors to collect data on temperature, humidity, and light, simulating a plant environment. When light reaches a certain threshold, the LED turns on to signal that it is “day.” The RPi continuously sends sensor data to the AWS IOT Sitewise database through an API call, where it is displayed on a dashboard visualizer. A simple ML classification model uses temperature and humidity to predict whether the plant is healthy or not. A flask web page dynamically updates to display different images and text based on the outcome of the prediction.

Components:
The hardware components include a RaspberryPi board, GrovePi shield, 2 sensor nodes (temperature/humidity sensor and light sensor), and an LED.
The software I used was python (for data processing and communication with the database), and html/css (for the web page). I used AWS to host my database and visualizer.
The protocols I used were HTTPS to send data to the AWS SiteWise database and MQTT to send data to the AWS cloud server, where it was routed to the CloudWatch Log.
The data processing is done through a Machine Learning classification model, which I trained using a 2 node input layer, ReLu activation (for nonlinear relationships), and a single output neuron that we could use to predict if a plant was healthy or unhealthy.
 
Limitations: 
One limitation I ran into was not being able to find sufficient data about healthy plant temperatures and humidities, which I needed to train my ML model. Because of this, I had to create the csv file myself by generating random numbers for temperature and humidity and manually classifying them based on what Google said a healthy indoor plant environment was (temperature between 21-27℃ and humidity between 40-60%). This might have caused the model to not be as accurate since it didn’t have a lot of data to train on.

Diagrams:

<img width="582" alt="Screenshot 2024-11-28 at 12 05 40 AM" src="https://github.com/user-attachments/assets/7aedd52a-cfd1-45b3-979f-d356de149130">
(AWS Dashboard) 

<img width="507" alt="Screenshot 2024-11-28 at 12 06 01 AM" src="https://github.com/user-attachments/assets/ab82c14f-082c-4e5f-bbdd-8d5f2eef563e">
(Machine Learning)

<img width="589" alt="Screenshot 2024-11-28 at 12 06 28 AM" src="https://github.com/user-attachments/assets/037487f5-d621-4221-9dd2-8c8f20e188e6">
(Dynamic Flask Page)
