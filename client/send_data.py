import requests
import random
import time

def simulate_temperature():
    """Simulate a temperature reading in Celsius."""
    return round(random.uniform(18.0, 30.0), 2)

def send_temperature():
    temperature = simulate_temperature()
    payload = {"device_id": "iot-pi-001", "temperature": temperature}
    try:
        response = requests.post("http://192.168.0.25:5000/data", json=payload)
        print(f"Sent: {payload}")
        print(f"Response: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print("Error:", e)

if __name__ == "__main__":
    while True:
        send_temperature()
        time.sleep(10)  # wait 10 seconds before sending next reading

