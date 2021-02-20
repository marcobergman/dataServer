#!/usr/bin/env python

import asyncio
import json
import socket
import websockets
import datetime
import threading

/*
 * Data Server
 * Listen to a web socket for {"name": "value"} pairs
 * Distribute this data in signalk format to all attached clients
 *
 */

server_host=socket.gethostbyname(socket.gethostname())
#server_host="192.168.178.30"
server_port=3001

class dataServer (object):
    
    def __init__(self):
        self.USERS = set()

    async def distribute(self, path, value):
        if self.USERS:  # asyncio.wait doesn't accept an empty list
            message = json.dumps({
                        "context": "my-boat",
                        "updates": [{
                            "$source": "sailing-pd",
                            "timestamp": datetime.datetime.now().isoformat(),
                            "values": [{
                                "path": path,
                                "value": value
                            }]
                        }]})  
            await asyncio.wait([user.send(message) for user in self.USERS])

    async def register(self, websocket):
        self.USERS.add(websocket)

    async def unregister(self, websocket):
        self.USERS.remove(websocket)

    async def counter(self, websocket, path):
        # register(websocket) sends user_event() to websocket
        await self.register(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                for i in data:
                    print (i, data[i])
                    await self.distribute(i, data[i])
        except Exception as e:
            print ("***", str(e))
        finally:
            await self.unregister(websocket)

    def runServer(self, loop):
        loop.run_until_complete(start_server)
        loop.run_forever()

if __name__ == '__main__':
    print ("DataServer - running a web socket at {}:{}".format(server_host, server_port))
    myDataServer = dataServer()
    new_loop = asyncio.get_event_loop()
    start_server = websockets.serve(myDataServer.counter, server_host, server_port, loop=new_loop)
    t = threading.Thread(target=myDataServer.runServer, args=(new_loop, ))
    t.start()

    


