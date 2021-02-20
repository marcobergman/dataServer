import asyncio
import websockets
import socket
from threading import Thread
import json


server_host = socket.gethostbyname(socket.gethostname())
server_port = 3001 

async def hello():
    uri = "ws://{}:{}".format(server_host, server_port)
    print ("connecting to", uri)
    async with websockets.connect(uri) as websocket:
        parameter_name = input("Parameter name:  ")
        parameter_value = input("Parameter value: ")
        
        message = json.dumps({parameter_name: parameter_value})
        await websocket.send(message)
        print(f"> {message}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_until_complete(hello())