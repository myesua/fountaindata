### FountainData API: The Hyper-Fast Gateway for Resilient Data Ingestion

FountainData is an open-source, high-performance API service designed to act as a resilient ingestion gateway, ensuring that only clean, validated, and schematized data ever enters your core data pipelines.

Built on an asynchronous Python stack (FastAPI, Pydantic, Asyncio), FountainData provides C-speed schema validation combined with concurrent data routing, making it the ideal solution for protecting your data lake, message queues, and real-time streams from data quality errors and schema drift.

#### ⚡ Key Features & Performance Edge

FountainData is engineered to be the fastest possible data quality gate.

- Feature

- Description

- Performance Benefit

- Pydantic-Native Validation

- Converts JSON Schemas (contracts) into compiled Pydantic models at runtime for C-speed data validation.

- Microsecond Validation Latency

- Asynchronous Routing

- Uses asyncio.gather to concurrently push valid data to the 'CLEAN' queue and invalid data to the 'QUARANTINE' queue.

- Non-Blocking I/O and maximum throughput.

- Batch Rate Limiting

- Middleware enforces flow control based on records per second, protecting downstream data sinks from ingestion spikes.

- Guarantees Quality of Service (QoS) for the entire pipeline.

- Adaptive Schema Control

- Automatically approves low-risk changes (adding optional fields) but blocks high-risk changes (removing required fields) with a 403 Forbidden.

- Prevents schema drift and catastrophic pipeline failure.

- RESTful API

- Clean, intuitive REST endpoints for dynamic contract registration and high-volume data validation.

- Easy integration with any modern application or service.

#### 🏗️ Architecture: Why FountainData is so Fast

FountainData is built on a modern, asynchronous technology stack that prioritizes I/O concurrency over threading:

Ingestion & Routing: FastAPI handles high concurrency, allowing thousands of requests to be processed by a small number of asynchronous workers.

Validation: The Pydantic Core compiles schemas directly, shifting validation overhead from CPU-intensive Python interpretation to fast, optimized code.

Concurrent Dispatch: The DataRouter uses async operations to push validated data and quarantined data simultaneously, ensuring that the total processing time is governed by the slower of the two downstream I/O operations, not the sum of both.

#### Data Flow Diagram

![Data Flow Diagram](data_flow_diagram.png)

#### 🚀 Getting Started (Run Locally)

FountainData is easy to run and test using Uvicorn.

Prerequisites

Python 3.10+

pip

1. Installation

Clone the repository and install dependencies:

git clone [https://github.com/fountaindata/fountaindata.git](https://github.com/fountaindata/fountaindata.git)
cd fountaindata
pip install -r requirements.txt

2. Run the Server

Launch the Uvicorn server in development mode:

uvicorn main:app --reload --host 0.0.0.0 --port 8000

3. Test the Validation Endpoint

Send a batch of records to the primary validation endpoint. This test includes one valid record, one missing a required field, and one with a type error.

POST http://127.0.0.1:8000/v1/data/cust_events_stream/validate

```json
{
  "data_batch": [
    {
      "user_id": 101,
      "event_name": "product_view",
      "timestamp": "2025-11-03T10:00:00Z",
      "price": 19.99
    },
    { "user_id": 102, "timestamp": "2025-11-03T10:05:00Z", "price": 50.0 },
    {
      "user_id": 103,
      "event_name": "checkout_start",
      "timestamp": "2025-11-03T10:10:00Z",
      "price": "49.99 dollars"
    }
  ]
}
```

> **Expected Console Output:** You will see logs confirming the asynchronous routing:
>
> `[DATA ROUTER] Pushing 1 valid records to CLEAN DATA queue...`  
> `[DATA ROUTER] Pushing 2 invalid records to QUARANTINE queue...`

#### 🗺️ Roadmap & Ecosystem (FountainCore vs. Enterprise)

The current repository represents FountainCore: a complete, high-performance data quality gateway. Our future roadmap focuses on building a full-fledged ecosystem suitable for the most demanding enterprise environments.

- FountainCore (Open Source) Priorities

- Integration Drivers: Develop and document core service interfaces (e.g., how to integrate custom data sinks).

- Expanded Data Types: Support for advanced validation types (e.g., regex constraints, complex array structures).

- Detailed Metrics: Expose a /metrics endpoint for Prometheus/Grafana to track throughput and error rates.

#### FountainEnterprise (Premium Offerings)

These features are essential for production-grade security and governance and will form the basis of our premium offering:

- 🔒 Persistence Layer: Replace the in-memory registry with a robust, asynchronous database (PostgreSQL, Mongo) for permanent contract storage.

- 🔑 Authentication & Authorization: JWT/API key security middleware to protect high-volume validation endpoints.

- 📊 Observability Dashboard: A dedicated web UI to view schema history, analyze quarantine data, and monitor pipeline performance.

- We invite all contributions to the FountainCore project!

#### 🤝 Contributing

> We welcome bug reports, feature requests, and code contributions. Please read our CONTRIBUTING.md (coming soon) for guidelines.
> Email us at info@fountaindata.com for collaboration

#### 📄 License

FountainData is licensed under the MIT License.
