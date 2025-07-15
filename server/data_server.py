from flask import Flask, request, jsonify
import csv
from datetime import datetime  # For timestamping log entries
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
import base64

app = Flask(__name__)

# Load the RSA public key once at startup
with open("public_key.pem", "rb") as key_file:
    PUBLIC_KEY = serialization.load_pem_public_key(key_file.read())

# Define valid API keys and map them to device IDs
VALID_API_KEYS = {
    "SECRET-PI-KEY-123": "raspberry-pi-01"
}

# Endpoint to receive sensor data securely via HTTPS POST
@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    try:
        # Step 1: Extract and validate API key
        api_key = request.headers.get("Authorization", "").replace("Bearer ", "")
        if api_key not in VALID_API_KEYS:
            return jsonify({"error": "Unauthorized - invalid API key"}), 401
        
        device_id = VALID_API_KEYS[api_key]

        # Step 2: Parse JSON data
        data = request.get_json()

        # Step 3: Validate data format (temperature, humidity, signature)
        if ('temperature' in data and isinstance(data['temperature'], (float, int)) and
            'humidity' in data and isinstance(data['humidity'], (float, int)) and
            'signature' in data):

            # Step 4: Reconstruct the message and verify the signature
            message = f"{data['temperature']},{data['humidity']}".encode()
            signature = base64.b64decode(data['signature'])

            try:
                PUBLIC_KEY.verify(
                    signature,
                    message,
                    padding.PKCS1v15(),
                    hashes.SHA256()
                )
            except InvalidSignature:
                return jsonify({"error": "Invalid digital signature"}), 403

            print(f"Verified data from {device_id}: {data}")

            # Step 5: Log to CSV
            with open("logs.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    datetime.now().isoformat(),  # Timestamp
                    device_id,                  # Which device sent it
                    data['temperature'],
                    data['humidity']
                ])

            # Step 6: Respond positively
            return jsonify({"message": "Data received and verified successfully!"}), 200
        else:
            # Respond negatively if validation fails
            return jsonify({"error": "Invalid data format"}), 400

    except Exception as e:
        # Catch-all for unexpected errors
        print(f"Error: {e}")
        return jsonify({"error": "Server encountered an error"}), 500

# Run the Flask server with SSL (HTTPS)
if __name__ == "__main__":
    # Note: For real projects a proper certificate would be used here.
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
