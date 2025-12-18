import requests
import uuid
import random
import time

BASE_URL = "http://aggregator:8080"
HEALTH_URL = f"{BASE_URL}/health"
PUBLISH_URL = f"{BASE_URL}/publish"


def wait_for_aggregator():
    for i in range(30):
        try:
            r = requests.get(HEALTH_URL, timeout=2)
            if r.status_code == 200:
                print("✅ Aggregator ready")
                return
        except Exception:
            print(f"⏳ Waiting for aggregator ({i+1}/30)")
        time.sleep(2)

    raise RuntimeError("❌ Aggregator not ready")



wait_for_aggregator()


topics = ["demo", "test"]
events = []

for i in range(50):
    event_id = str(uuid.uuid4()) if random.random() > 0.3 else "DUPLICATE-ID"
    events.append({
        "topic": random.choice(topics),
        "event_id": event_id,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "source": "publisher",
        "payload": {
            "value": random.randint(1, 100)
        }
    })


for e in events:
    resp = requests.post(
        PUBLISH_URL,
        json=e,
        timeout=5
    )
    resp.raise_for_status()

print(f"🚀 Published {len(events)} events successfully")
