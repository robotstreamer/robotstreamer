import asyncio
import json
import _thread
from aiohttp import web
import websockets
import queue

# Queue for safe communication between HTTP and WebSocket threads
messageQueue = queue.Queue()

#message = await messageQueue.get()  # Get message from the queue
#await websocket.send(message)  # Send message to WebSocket client

async def handlePost(request):
    """Handles HTTP POST requests and forwards data to WebSocket via the queue."""
    try:
        data = await request.json()  # Parse JSON request body
        message = json.dumps(data)  # Convert JSON to string
        messageQueue.put(message)  # Put message in the queue
        return web.json_response({"status": "Message added to queue", "data": data})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=400)

async def startHttpServer():
    """Starts the HTTP server."""
    app = web.Application()
    app.add_routes([web.post("/send_chat_message", handlePost)])  # Define the POST route
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 8080)
    print("HTTP server started on http://localhost:8080")
    await site.start()
    await asyncio.Event().wait()  # Keep running indefinitely

def runHttpServer():
    """Runs the HTTP server in a new event loop."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(startHttpServer())




# Keep the thread alive
#threading.Event().wait()
