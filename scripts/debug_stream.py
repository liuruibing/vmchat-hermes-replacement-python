import asyncio
import httpx

async def debug_stream():
    url = "http://127.0.0.1:7311/v1/runs"
    payload = {
      "model": "gpt-4",
      "input": [{"role": "user", "content": "Hello"}],
      "instructions": "",
      "session_id": "test",
      "skills": ["vm-report-dsl"],
      "tools": []
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload)
        print("POST status:", resp.status_code)
        run_id = resp.json()["id"] if "id" in resp.json() else resp.json()["run_id"]
        print("Run ID:", run_id)
        
        # Connect to stream
        stream_url = f"http://127.0.0.1:7311/v1/runs/{run_id}/events"
        async with client.stream("GET", stream_url) as sresp:
            print("GET status:", sresp.status_code)
            async for chunk in sresp.aiter_text():
                print("CHUNK:", repr(chunk))

if __name__ == "__main__":
    asyncio.run(debug_stream())
