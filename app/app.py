from flask import Flask, Response, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "flask_app_request_count",
    "Total number of requests received",
    ["method", "endpoint", "http_status"]
)

REQUEST_LATENCY = Histogram(
    "flask_app_request_latency_seconds",
    "Request latency in seconds",
    ["endpoint"]
)


@app.route("/")
def home():
    start = time.time()
    response = "Flask app is running! Visit /metrics to see Prometheus metrics."
    latency = time.time() - start
    REQUEST_LATENCY.labels(endpoint="/").observe(latency)
    REQUEST_COUNT.labels(method="GET", endpoint="/", http_status=200).inc()
    return response


@app.route("/health")
def health():
    start = time.time()
    response = {"status": "healthy"}
    latency = time.time() - start
    REQUEST_LATENCY.labels(endpoint="/health").observe(latency)
    REQUEST_COUNT.labels(method="GET", endpoint="/health", http_status=200).inc()
    return response


@app.route("/work")
def work():
    start = time.time()
    time.sleep(random.uniform(0.05, 0.6))
    latency = time.time() - start
    REQUEST_LATENCY.labels(endpoint="/work").observe(latency)
    REQUEST_COUNT.labels(method="GET", endpoint="/work", http_status=200).inc()
    return {"message": "work done", "duration_seconds": round(latency, 3)}


@app.route("/error")
def error():
    start = time.time()
    latency = time.time() - start
    REQUEST_LATENCY.labels(endpoint="/error").observe(latency)
    REQUEST_COUNT.labels(method="GET", endpoint="/error", http_status=500).inc()
    return {"error": "simulated failure"}, 500


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)