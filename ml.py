# ML processing
from tensorflow.keras.models import load_model
import pickle
import pandas as pd
import numpy as np

def process(temp,hum,lux):
    model = load_model('model.keras')
    f = open('scaler.pkl', 'rb')
    scaler = pickle.load(f)

    sensor_data = pd.DataFrame({
    "temperature": [temp],
    "humidity": [hum],
    })
    sensor_data = scaler.transform(sensor_data[["temperature", "humidity"]].to_numpy())

    # Use the model to make predictions
    pred = model.predict(sensor_data)
    pred = np.round(pred).astype(int).flatten()
    if pred[0] == 0:
        plant = "unhealthy"
        color = "red"
    else:
        plant = "healthy"
        color = "green"
    if lux > 100:
        day = "day"
    else:
        day = "night"
        
    return (plant, color, day)
