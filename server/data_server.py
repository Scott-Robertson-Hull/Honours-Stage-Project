from flask import Flask, request, jsonify
import csv
from datetime import datetime  # For timestamping log entries

app = Flask(__name__)

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

        # Step 3: Validate the data format
        if ('temperature' in data and isinstance(data['temperature'], (float, int)) and
            'humidity' in data and isinstance(data['humidity'], (float, int))):

            print(f"Received data from {device_id}: {data}")

            # Step 4: Log to CSV file
            with open("logs.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    datetime.now().isoformat(),  # Timestamp
                    device_id,                  # Which device sent it
                    data['temperature'],
                    data['humidity']
                ])

            # Step 5: Respond positively
            return jsonify({"message": "Data received successfully!"}), 200
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
