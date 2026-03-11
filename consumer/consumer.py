import json
import time
from datetime import datetime

from confluent_kafka import Consumer
import clickhouse_connect

KAFKA_BROKER = "localhost:19092"
TOPIC_NAME = "product-events"

consumer = Consumer(
    {
        "bootstrap.servers": KAFKA_BROKER,
        "group.id": "analytics-consumer-group",
        "auto.offset.reset": "earliest",
    }
)

clickhouse = clickhouse_connect.get_client(
    host="localhost",
    port=8123,
    username="analytics_user",
    password="analytics_pass",
    database="analytics",
)

consumer.subscribe([TOPIC_NAME])

print("Consumer started. Waiting for events...")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print("Consumer error:", msg.error())
            continue

        event = json.loads(msg.value().decode("utf-8"))
        print("Received event:", event)

        clickhouse.insert(
            "raw_product_events",
            [[
                event["event_id"],
                event["event_type"],
                event["user_id"],
                event["session_id"],
                event["product_id"],
                float(event["amount"]),
                datetime.fromisoformat(event["timestamp"]),
            ]],
            column_names=[
                "event_id",
                "event_type",
                "user_id",
                "session_id",
                "product_id",
                "amount",
                "event_time",
            ],
        )

        print("Inserted into ClickHouse")

except KeyboardInterrupt:
    print("Stopping consumer...")

finally:
    consumer.close()
