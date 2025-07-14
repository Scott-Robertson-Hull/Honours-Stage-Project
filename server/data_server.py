from flask import Flask, request, jsonify

app = Flask(__name__)

# Endpoint to receive sensor data securely via HTTPS POST
@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    try:
        # Parse JSON data sent from the client
        data = request.get_json()

        # Basic validation to ensure both fields exist and are correct types
        if ('temperature' in data and isinstance(data['temperature'], (float, int)) and
            'humidity' in data and isinstance(data['humidity'], (float, int))):

            print(f"Received data: {data}")

            # Respond positively if data is valid
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
