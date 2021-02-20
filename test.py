import asyncio
import websockets
import socket
#from threading import Thread
import json
import random
import time


server_host = socket.gethostbyname(socket.gethostname())
server_port = 3001 

async def hello():
    uri = "ws://{}:{}".format(server_host, server_port)
    print ("Variable Wind")
    print ("connecting to", uri)
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                
                while True:
                    parameter_name = "environment.wind.angleApparent"
                    parameter_value = random.randint(225, 235)
                    message = json.dumps({parameter_name: parameter_value})
                    await websocket.send(message)
                    
                    parameter_name = "environment.wind.speedApparent"
                    parameter_value = random.randint(15, 22)
                    message = json.dumps({parameter_name: parameter_value})
                    await websocket.send(message)
                    
                    time.sleep(0.5)
        except:
            pass
        
asyncio.get_event_loop().run_until_complete(hello())
