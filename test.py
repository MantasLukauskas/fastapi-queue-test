import asyncio
import httpx
import time

# Updated to return the response data along with timing information
async def send_request(client, url, request_id):
    start_time = time.time()
    response = await client.get(url)
    elapsed_time = time.time() - start_time
    response_data = response.json()  # Assuming JSON response, adjust as needed
    print(f"Request {request_id} sent and processed in {elapsed_time:.2f} seconds. Response: {response_data}")
    return request_id, elapsed_time, response_data

async def main():
    url = "http://localhost:8000/status/"  # Update to your FastAPI /status/ endpoint URL
    async with httpx.AsyncClient(timeout=120) as client:  # Increased timeout for all operations
        tasks = [send_request(client, url, i + 1) for i in range(100)]
        results = await asyncio.gather(*tasks)

    print("\nRequest timings and responses:")
    for request_id, timing, response_data in results:
        print(f"Request {request_id}: {timing:.2f} seconds, Response: {response_data}")

if __name__ == '__main__':
    asyncio.run(main())