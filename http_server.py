import asyncio
import json
import _thread
import websockets
import traceback
import time
from aiohttp import web
from shared_controller_entities import currentWebsocket


async def handlePost(request):
    """handles HTTP POST requests and forwards data to chat
    websocket. Data should be json.

    """
    try:
        data = await request.json()  # Parse JSON request body
        message = json.dumps(data)  # Convert JSON to string
        await currentWebsocket['chat'].send(message)
        return web.json_response({"status": "message sent", "data": data})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=400)

    
async def startHTTPServer():
    """Starts the HTTP server."""
    app = web.Application()
    app.add_routes([web.post("/send_chat_message", handlePost)])  # Define the POST route
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 8080)
    print("HTTP: server started on http://localhost:8080")
    await site.start()
    await asyncio.Event().wait()  # Keep running indefinitely
    

def startHTTP():
    while True:
        print("HTTP: starting HTTP loop")
        try:
            asyncio.new_event_loop().run_until_complete(startHTTPServer())
        except:
            print("HTTP: error")
            traceback.print_exc()
        print("HTTP: event handler died")

        time.sleep(2)


