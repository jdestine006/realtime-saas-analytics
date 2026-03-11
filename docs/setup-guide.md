# Setup Guide — Real-Time SaaS Analytics Platform

This guide explains how to run the Real-Time SaaS Analytics Platform locally.

The system ingests product events, streams them through a distributed event broker, processes them into an analytics database, and visualizes metrics through dashboards.

---

## Prerequisites

Install the following before starting:

- Docker Desktop
- Python 3.10+
- Git

Verify installations:
```
docker --version
python3 --version
git --version
```
---

## Clone the Repository
```
git clone https://github.com/YOUR_USERNAME/realtime-saas-analytics-platform.git
cd realtime-saas-analytics-platform
```
---

## Start Infrastructure

The project uses Docker Compose to run the following services:
```
- Redpanda (event streaming broker)
- ClickHouse (analytics database)
- Metabase (analytics dashboard)
```
Start the containers:
```
docker compose up -d
```
Verify services are running:
```
docker compose ps
```
You should see containers for:
```
redpanda
clickhouse
metabase
```
---

## Create ClickHouse Tables

Initialize the analytics database schema.

Run:
```
docker exec -i clickhouse clickhouse-client < sql/clickhouse_tables.sql
```
Verify the table exists:
```
docker exec -it clickhouse clickhouse-client --query "SHOW TABLES FROM analytics"
```
Expected output:
```
raw_product_events
```
---

## Start the Event Ingestion API

Navigate to the API directory:
```
cd api
```
Create a Python virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```
Install dependencies:
```
pip install -r requirements.txt
```
Start the FastAPI server:
```
uvicorn main:app --reload --port 8000
```
Verify the API is running:
```
http://localhost:8000/health
```
Expected response:
```
{"status": "ok"}
```
---

## Start the Event Consumer

Open a new terminal window.

Navigate to the consumer directory:
```
cd consumer
```
Create and activate a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```
Install dependencies:
```
pip install -r requirements.txt
```
Start the consumer service:
```
python consumer.py
```
The consumer will now listen for events from Redpanda and insert them into ClickHouse.

---

## Generate Test Events

Navigate back to the API directory:
```
cd api
```
Run the event simulator:
```
python simulate_events.py
```
This script generates simulated SaaS activity events including:

- page views
- signups
- trial starts
- purchases

These events will flow through the pipeline into ClickHouse.

---

## Verify Data in ClickHouse

You can confirm events were inserted by running:
```
docker exec -it clickhouse clickhouse-client --query "SELECT count() FROM analytics.raw_product_events"
```
The count should increase after running the simulator.

---

## Open the Analytics Dashboard

Open Metabase in your browser:
```
http://localhost:3001
```
Create an admin account and connect the database using:
```
Host: clickhouse  
Port: 8123  
Database: analytics  
Username: analytics_user  
Password: analytics_pass  
```
After connecting, you can explore the table:
```
raw_product_events
```
---

## Example Analytics Queries

### Events by Type
```
SELECT
  event_type,
  count() AS event_count
FROM analytics.raw_product_events
GROUP BY event_type
ORDER BY event_count DESC;
```
### Revenue by Product
```
SELECT
  product_id,
  sum(amount) AS revenue
FROM analytics.raw_product_events
WHERE event_type = 'purchase'
GROUP BY product_id
ORDER BY revenue DESC;
```
### Revenue Over Time
```
SELECT
  toStartOfHour(event_time) AS hour,
  sum(amount) AS revenue
FROM analytics.raw_product_events
WHERE event_type = 'purchase'
GROUP BY hour
ORDER BY hour;
```
---

## Pipeline Architecture
```
Event Simulator
      ↓
FastAPI Event Ingestion API
      ↓
Redpanda (Kafka-compatible streaming)
      ↓
Python Consumer
      ↓
ClickHouse (Analytics Database)
      ↓
Metabase Dashboard
```
---

## Stopping the System

To stop all infrastructure services:
```
docker compose down
```
---

## Future Improvements

Possible enhancements include:

- dbt transformations
- event replay pipelines
- S3 data lake storage
- streaming anomaly detection
- production cloud deployment
