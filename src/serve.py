import asyncio
from threading import Thread
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

import websockets

def handler(*args, **kwargs):
    return SimpleHTTPRequestHandler(*args, **kwargs, directory='web')

def serve_http():
    print('Serving http')
    server = ThreadingHTTPServer(('localhost', 8080), handler)
    server.serve_forever()

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

def serve_websocket():
    async def serve():
        async with websockets.serve(echo, 'localhost', 8765):
            await asyncio.Future()
    asyncio.run(serve())

def main():
    Thread(target=serve_websocket).start()
    serve_http()

if __name__ == '__main__':
    main()
