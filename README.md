# FastAPI with Prometheus and Redis Async Example

This project demonstrates how to create a simple FastAPI application that incorporates Prometheus for metrics gathering and uses an asynchronous Redis client for managing application state. It simulates processing requests and gathers metrics on processing times and request counts.

## Features

- **FastAPI**: For quick and easy setup of REST API endpoints.
- **Prometheus metrics**: Tracks the number of active requests, timeout requests, and the time spent processing requests.
- **Redis (asyncio)**: Manages active and timeout request counts using an asynchronous approach.

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.8 or higher

### Setup and Running

1. **Clone the Repo**

```bash
git clone https://github.com/MantasLukauskas/fastapi-queue-test
cd yourrepository
```

2. **Run Redis and Prometheus using Docker**

Assuming you have a `docker-compose.yml` that includes Redis and Prometheus services, run:

```bash
docker-compose up -d
```

3. **Install Dependencies**

Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn prometheus_client aioredis
```

4. **Run the Application**

```bash
uvicorn main:app --reload
```

Replace `main` with the name of your Python file if it's different.

### Using the Application

- Visit `http://localhost:8000/status/` to simulate processing a request.
- Post JSON data to `http://localhost:8000/process_request/` to simulate processing a different type of request.
- Access metrics at `http://localhost:8000/metrics/` to view Prometheus-formatted data about your running application.

## Understanding the Code

- The FastAPI instance is set up with `/status/` and `/process_request/` endpoints for GET and POST requests, respectively.
- The Redis asyncio client is used to manage counters for active requests within the application.
- Prometheus metrics are updated based on request processing, maintaining counts and processing times.
- Logging provides insight into the application's operation, facilitating debugging and monitoring.

## Contributing

We welcome contributions! Please open an issue or submit a pull request for any improvements you'd like to suggest.

## License

This project is open source and available under the [MIT License](LICENSE).
