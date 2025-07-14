import requests
import json
import random
import time

API_KEY = "SECRET-PI-KEY-123"

# URL of the server, my raspberry pi's local IP address in this instance
SERVER_URL = 'https://192.168.0.25:5000/api/sensor-data'


# Simulated sensor data function
def generate_sensor_data():
    # Simulate temperature and humidity readings
    data = {
        'temperature': round(random.uniform(20.0, 30.0), 2),  # e.g., 25.47°C
        'humidity': round(random.uniform(30.0, 70.0), 2)      # e.g., 55.12%
    }
    return data

# Main function to send data securely
def send_sensor_data():
    data = generate_sensor_data()
    print(f"Sending data: {data}")

    try:
        headers = {
        "Authorization": f"Bearer {API_KEY}"
        }
        
        # Convert data dictionary to JSON format and send it over HTTPS
        response = requests.post(
            SERVER_URL, 
            json=data,
            headers=headers,
            timeout=10,  # 10-second timeout
            verify=False  # This bypasses SSL verification (because of ad-hoc cert)
        )

        # Check response status code (200 means success)
        if response.status_code == 200:
            print(f"Data sent successfully. Server response: {response.text}")
        else:
            print(f"Failed to send data. Server responded with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        # Handle exceptions (network errors, timeout, SSL issues, etc.)
        print(f"Error sending data: {e}")

# Continuously send data every 10 seconds
if __name__ == "__main__":
    while True:
        send_sensor_data()
        time.sleep(10)
