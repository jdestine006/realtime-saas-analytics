from datetime import datetime
from uuid import uuid4
import json
import os

from fastapi import FastAPI
from pydantic import BaseModel
from confluent_kafka import Producer

app = FastAPI(title="Real-Time SaaS Analytics API")

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:19092")
TOPIC_NAME = os.getenv("TOPIC_NAME", "product-events")

producer = Producer({"bootstrap.servers": KAFKA_BROKER})


class ProductEvent(BaseModel):
    event_type: str
    user_id: str
    session_id: str
    product_id: str
    amount: float = 0.0
    timestamp: datetime | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/events")
def create_event(event: ProductEvent):
    payload = {
        "event_id": str(uuid4()),
        "event_type": event.event_type,
        "user_id": event.user_id,
        "session_id": event.session_id,
        "product_id": event.product_id,
        "amount": event.amount,
        "timestamp": (event.timestamp or datetime.utcnow()).isoformat(),
    }

    def delivery_report(err, msg):
        if err is not None:
            print("Delivery failed:", err)
        else:
            print(f"Delivered to {msg.topic()} [{msg.partition()}]")

    producer.produce(
        TOPIC_NAME,
        json.dumps(payload).encode("utf-8"),
        callback=delivery_report,
    )
    producer.flush()

    return {"message": "event published", "event": payload}