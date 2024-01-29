import logging
import uuid
import asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import redis.asyncio as redis
import time
from prometheus_client import Summary

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect to Redis using the async client
redis_client = redis.Redis(host='redis', port=6379, db=0)

# Instantiate FastAPI application and Prometheus Gauge
app = FastAPI()
ACTIVE_REQUESTS_GAUGE = Gauge('active_requests', 'Number of active requests being processed')
TIMEOUT_REQUESTS_GAUGE = Gauge('timeout_requests', 'Number of timeout requests')
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing requests', ['method', 'endpoint'])
@app.on_event("startup")
async def startup_event():
    await redis_client.delete("active_requests_counter")

@app.get("/metrics/")
async def metrics():
    queue_length = await redis_client.llen("active_requests")
    ACTIVE_REQUESTS_GAUGE.set(queue_length)
    timeout_requests_list = await redis_client.llen("timeout_requests")
    TIMEOUT_REQUESTS_GAUGE.set(timeout_requests_list)
    logger.info(f"Metrics request: Active requests gauge set to {queue_length}")
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/status/")
async def process_request():
    request_id = str(uuid.uuid4())
    start_time = time.time()
    start = time.time()
    await redis_client.lpush("active_requests", request_id)
    queue_length = await redis_client.llen("active_requests")
    logger.info(f"Processing {request_id}. Active requests: {queue_length}")
    await asyncio.sleep(20)  # Simulated processing time
    await redis_client.lrem("active_requests", 0, request_id)
    queue_length = await redis_client.llen("active_requests")
    logger.info(f"Finished processing {request_id}. Active requests now: {queue_length}")
    processing_time = time.time() - start_time
    if processing_time > 60:
        await redis_client.lpush("timeout_requests", request_id)
    REQUEST_TIME.labels(method="GET", endpoint="/status/").observe(processing_time)
    return JSONResponse(content={"request_id": request_id, "active_requests": queue_length, "time": time.time()-start}, status_code=200)

@app.post("/process_request/")
async def process_request(item: dict):
    request_id = str(uuid.uuid4())
    start = time.time()

    # Increment the Redis counter when processing starts
    counter = redis_client.incr("active_requests_counter")
    ACTIVE_REQUESTS_GAUGE.set(counter)  # Also update the Prometheus Gauge
    print(f"Processing {request_id}. Active requests: {counter}")

    # Simulate processing
    await asyncio.sleep(20)  # Simulate async IO operation

    # Decrement the Redis counter when processing is done
    counter = redis_client.decr("active_requests_counter")
    ACTIVE_REQUESTS_GAUGE.set(counter)  # Also update the Prometheus Gauge
    print(f"Finished processing {request_id}. Active requests: {counter}")

    return JSONResponse(content={"request_id": request_id, "active_requests": counter, "time": time.time()-start}, status_code=202)
