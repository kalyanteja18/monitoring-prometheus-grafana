import random
import time
import requests

BASE_URL = "http://localhost:5000"
ENDPOINTS = ["/", "/health", "/work", "/error"]

print(f"Sending traffic to {BASE_URL} — press Ctrl+C to stop.")

while True:
    endpoint = random.choice(ENDPOINTS)
    try:
        r = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        print(f"GET {endpoint} -> {r.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    time.sleep(random.uniform(0.2, 1.5))