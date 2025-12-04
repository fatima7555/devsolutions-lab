# app/status/app.py
from flask import Flask, jsonify
import socket, time

app = Flask(__name__)

@app.route("/status")
def status():
    return jsonify({
        "service": "status",
        "host": socket.gethostname(),
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
