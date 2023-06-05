#!/usr/bin/env python

import asyncio
import websockets

async def handler(websocket):
    while True:
        message = await websocket.recv()
        print(message)

async def start_server():
    # Start the WebSocket server
    server = await websockets.serve(handle_websocket, "localhost", 8765)
    print("WebSocket server started")

    # Run the server indefinitely
    await server.wait_closed()

if __name__ == "__main__":
    # Run the server in an asyncio event loop
    asyncio.get_event_loop().run_until_complete(start_server())