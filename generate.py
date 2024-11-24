import csv
import random

filename = "data.csv"

# Generate 100 entries with random values for temperature and humidity
data = [
    {"temperature": round(random.uniform(10, 35), 2), # 18-24 healthy
     "humidity": round(random.uniform(30, 90), 2)} # 40-60 healthy
    for _ in range(100)
]

# Write to CSV file
with open(filename, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["temperature", "humidity"])
    writer.writeheader()
    writer.writerows(data)