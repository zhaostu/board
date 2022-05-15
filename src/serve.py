#!/usr/bin/env python3

import asyncio
from threading import Thread
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

import websockets

CONNECTIONS = set()
state = []

def handler(*args, **kwargs):
    return SimpleHTTPRequestHandler(*args, **kwargs, directory='web')

def serve_http():
    print('Serving http')
    server = ThreadingHTTPServer(('localhost', 8080), handler)
    server.serve_forever()

async def conn(websocket):
    CONNECTIONS.add(websocket)
    try:
        known_state = await websocket.recv()
        print(f'Connection with {known_state}')
        if int(known_state) < len(state):
            for message in state[int(known_state):]:
                await websocket.send(message)

        async for message in websocket:
            websockets.broadcast(CONNECTIONS, message)
            state.append(message)
    finally:
        CONNECTIONS.remove(websocket)

def serve_websocket():
    async def serve():
        async with websockets.serve(conn, 'localhost', 8765):
            await asyncio.Future()
    asyncio.run(serve())

def main():
    Thread(target=serve_websocket).start()
    serve_http()

if __name__ == '__main__':
    main()
