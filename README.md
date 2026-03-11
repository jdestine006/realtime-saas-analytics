# Real-Time SaaS Analytics Platform

A real-time analytics pipeline that ingests product events, streams them through a distributed message broker, processes them into an analytics database, and visualizes them in a dashboard.

This project demonstrates modern data platform architecture used by SaaS companies tto power product analytics and revenue insights

# Architecture

Event Simulator/Client --> FastAPI Event Ingestion API --> Redpanda (Kafka-compatible streaming broker) -->Python Consumer --> ClickHouse (analytics database) --> Metabase (analytics dashboard)

## Features

 - Real-time event ingestion API
 - Kafka-compatible streaming using Redpanda
 - Event-driven consumer pipeline
 - High-performance analytics database with ClickHouse
 - Product analytics dashboards in Metabase
 - Event simulator for generating realistic SaaS activity

## Example Analytics
 - Total events
 - Total revenue
 - Events by type 
 - Revenue by product 
 - Revenue over time
 - Conversion funnel

 These metrics simulate common SaaS product analytics.

 ## Tech Stack

 Backend API
  - FastAPI 
  - Python

Streaming
  - Redpanda

Data Processing
  - Consumer (Python)

Analytics Database
  - ClickHouse

Visualization
  - Metabase

Infrastructure
  - Docker/ Docker Compose

## Example Event

``` json
{
     "event_type": "purchase",
    "user_id": "user_345",
    "session_id": "sess_678",
    "product_id": "prod_789",
    "amount": 69.99,
    "timestamp": "2026-03-11T16:24:23"
}