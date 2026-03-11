import random
import time
import uuid
from datetime import datetime
import requests

API_URL = "http://localhost:8000/events"

EVENT_TYPES = [
    "page_view",
    "page_view",
    "page_view",
    "signup",
    "signup",
    "trial_started",
    "purchase",
]

PRODUCT_IDS = [
    "prod_basic",
    "prod_pro",
    "prod_enterprise",
    "prod_addon",
]


def generate_event():
    event_type = random.choice(EVENT_TYPES)

    amount = 0.0
    if event_type == "purchase":
        amount = round(random.uniform(10, 500), 2)

    return {
        "event_type": event_type,
        "user_id": f"user_{random.randint(1, 500)}",
        "session_id": f"sess_{uuid.uuid4().hex[:8]}",
        "product_id": random.choice(PRODUCT_IDS),
        "amount": amount,
        "timestamp": datetime.utcnow().isoformat()
    }


def main():
    total_events = 1000

    for i in range(total_events):
        event = generate_event()

        try:
            response = requests.post(API_URL, json=event, timeout=5)
            print(f"[{i+1}/{total_events}] {response.status_code} - {event['event_type']}")
        except Exception as e:
            print(f"Failed to send event: {e}")

        time.sleep(0.1)


if __name__ == "__main__":
    main()