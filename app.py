from flask import Flask, jsonify, render_template
import random
import time
import threading

app = Flask(__name__)

# Bus data with seat availability
buses = [
    {"id": 1, "route": "Route A", "lat": 11.0168, "lng": 76.9558, "status": "On Time", "seats_available": 12},
    {"id": 2, "route": "Route B", "lat": 11.0183, "lng": 76.9400, "status": "Delayed", "seats_available": 5},
    {"id": 3, "route": "Route C", "lat": 11.0100, "lng": 76.9700, "status": "On Time", "seats_available": 20},
]

# API route to return bus data
@app.route("/buses")
def get_buses():
    return jsonify(buses)

# Homepage
@app.route("/")
def index():
    return render_template("index.html")

# Function to simulate movement + seat updates
def update_buses():
    while True:
        for bus in buses:
            # Random GPS shift (simulate movement)
            bus["lat"] += random.uniform(-0.0005, 0.0005)
            bus["lng"] += random.uniform(-0.0005, 0.0005)

            # Random seat updates
            if bus["seats_available"] > 0 and random.random() > 0.7:
                bus["seats_available"] -= 1  # Someone boarded
            elif bus["seats_available"] < 30 and random.random() > 0.8:
                bus["seats_available"] += 1  # Someone left / got down

        time.sleep(5)  # update every 5 sec

# Background thread for simulation
threading.Thread(target=update_buses, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
