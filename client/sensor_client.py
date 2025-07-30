import requests
import json
import random
import time
import base64
import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

API_KEY = "SECRET-PI-KEY-123"
DEVICE_ID = "raspberry-pi-01"

# Load private key for signing
with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

# URL of the server, my raspberry pi's local IP address in this instance
SERVER_URL = 'https://192.168.0.25:5000/api/sensor-data'

# Simulated sensor data function
def generate_sensor_data():
    return {
        'temperature': round(random.uniform(20.0, 30.0), 2),
        'humidity': round(random.uniform(30.0, 70.0), 2),
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'device_id': DEVICE_ID
    }

# Main function to send data securely
def send_sensor_data():
    data = generate_sensor_data()
    print(f"Sending data: {data}")

    # Prepare the signed_data as a JSON string (only temperature and humidity)
    signed_data = json.dumps({
        "temperature": data["temperature"],
        "humidity": data["humidity"]
    })

    # Sign the JSON string
    signature = private_key.sign(
        signed_data.encode("utf-8"),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    encoded_signature = base64.b64encode(signature).decode('utf-8')

    # Payload matches server expectations
    payload = {
        "signed_data": signed_data,
        "signature": encoded_signature
    }

    # TC-4: Tamper with the signed_data after signing 
    # payload["signed_data"] = json.dumps({
    #    "temperature": 999,  # Tampered value
    #    "humidity": data["humidity"]
    #})

    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }

        response = requests.post(
            SERVER_URL,
            json=payload,
            headers=headers,
            timeout=10,
            verify="server.crt"  # Use the server's certificate for verification
        )

        if response.status_code == 200:
            print(f"Data sent successfully. Server response: {response.text}")
        else:
            print(f"Failed to send data. Server responded with status code: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        # Handle exceptions (network errors, timeout, SSL issues, etc.)
        print(f"Error sending data: {e}")


# Continuously send data every 10 seconds
if __name__ == "__main__":
    while True:
        send_sensor_data()
        time.sleep(10)
