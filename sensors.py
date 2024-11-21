import grovepi
import math
import time

temp_sensor = 4  # digital port 4
light_sensor = 0 # analog port 0
led = 3 # digital port 3

threshold = 10 # brightness threshold
grovepi.pinMode(light_sensor,"INPUT")
grovepi.pinMode(led,"OUTPUT")

while True:
    try:
        [temp,humidity] = grovepi.dht(temp_sensor,0)  # blue sensor
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            print("temp = %d C humidity = %d%%"%(temp, humidity))

        sensor_value = grovepi.analogRead(light_sensor)
        resistance = (float)(1023 - sensor_value) * 10 / sensor_value
        if resistance > threshold:
            grovepi.digitalWrite(led,0) # LED off
        else:
            grovepi.digitalWrite(led,1) # LED on
        print("sensor_value = %d resistance = %.2f" %(sensor_value,  resistance))
        
        time.sleep(.5)
    except IOError:
        print ("Error")
