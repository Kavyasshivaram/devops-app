from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Metric for Prometheus
REQUEST_COUNTER = Counter("devops_app_requests_total", "Total HTTP requests")

@app.route("/")
def home():
    REQUEST_COUNTER.inc()
    return "Hello, DevOps Pipeline!"

@app.route("/health")
def health():
    return jsonify({"status": "UP"}), 200

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
