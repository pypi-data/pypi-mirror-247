import asyncio
import websockets
import json
url = "ws://localhost:3774"

class watchlogConnect:
    def __init__(self):
        self.websocket = None
        
    async def connect(self):
        try:
            self.websocket = await websockets.connect(url)
            print(f"Connected to WebSocket server at {url}")
        except Exception as e:
            print(f"Failed to connect to watchlog agent: {e}")

    async def send_message(self, message):
        if self.websocket:
            try:
                await self.websocket.send(message)
                print(f"Sent message: {message}")
            except Exception as e:
                print(f"Failed to send message to watchlog: {e}")
        else:
            await self.connect()

    async def increment(self, metric , count = 1):
        if metric and isinstance(metric, str) and (isinstance(count , float) or isinstance(count , int)) and count > 0:
            message = json.dumps({"method" : "increment", "metric" : metric, "count" : count})
            if self.websocket:
                try:
                    await self.websocket.send(message)
                except Exception as e:
                    print(f"Failed to send message to watchlog agent: {e}")
            else:
                await self.connect()


    async def decrement(self, metric , count = 1):
        if metric and isinstance(metric, str) and (isinstance(count , float) or isinstance(count , int)) and count > 0:
            message = json.dumps({"method" : "decrement", "metric" : metric, "count" : count})
            if self.websocket:
                try:
                    await self.websocket.send(message)
                except Exception as e:
                    print(f"Failed to send message to watchlog agent: {e}")
            else:
                await self.connect()

        

    async def distribution(self, metric , count):
        if metric and isinstance(metric, str) and (isinstance(count , float) or isinstance(count , int)) :
            message = json.dumps({"method" : "distribution", "metric" : metric, "count" : count})
            if self.websocket:
                try:
                    await self.websocket.send(message)
                    print(f"Sent message: {message}")
                except Exception as e:
                    print(f"Failed to send message to watchlog agent: {e}")
            else:
                await self.connect()


    async def gauge(self, metric , count):
        if metric and isinstance(metric, str) and (isinstance(count , float) or isinstance(count , int)) :
            message = json.dumps({"method" : "gauge", "metric" : metric, "count" : count})
            if self.websocket:
                try:
                    await self.websocket.send(message)
                    print(f"Sent message: {message}")
                except Exception as e:
                    print(f"Failed to send message to watchlog agent: {e}")
            else:
                await self.connect()


    async def percentage(self, metric , count):
        if metric and isinstance(metric, str) and (isinstance(count , float) or isinstance(count , int)) :
            message = json.dumps({"method" : "percentage", "metric" : metric, "count" : count})
            if self.websocket:
                try:
                    await self.websocket.send(message)
                    print(f"Sent message: {message}")
                except Exception as e:
                    print(f"Failed to send message to watchlog agent: {e}")
            else:
                await self.connect()


    async def systembyte(self, metric , count):
        if metric and isinstance(metric, str) and (isinstance(count , float) or isinstance(count , int)) :
            message = json.dumps({"method" : "systembyte", "metric" : metric, "count" : count})
            if self.websocket:
                try:
                    await self.websocket.send(message)
                    print(f"Sent message: {message}")
                except Exception as e:
                    print(f"Failed to send message to watchlog agent: {e}")
            else:
                await self.connect()

    async def log(self, service , logMessage):
        if service and isinstance(service, str) and (isinstance(logMessage , str) ) :
            message = json.dumps({"method" : "log", "service" : service, "message" : logMessage, "status" : 0})
            if self.websocket:
                try:
                    await self.websocket.send(message)
                    print(f"Sent message: {message}")
                except Exception as e:
                    print(f"Failed to send message to watchlog agent: {e}")
            else:
                await self.connect()
                
    async def successLog(self, service , logMessage):
        if service and isinstance(service, str) and (isinstance(logMessage , str) ) :
            message = json.dumps({"method" : "log", "service" : service, "message" : logMessage, "status" : 1})
            if self.websocket:
                try:
                    await self.websocket.send(message)
                    print(f"Sent message: {message}")
                except Exception as e:
                    print(f"Failed to send message to watchlog agent: {e}")
            else:
                await self.connect()
    async def warningLog(self, service , logMessage):
        if service and isinstance(service, str) and (isinstance(logMessage , str) ) :
            message = json.dumps({"method" : "log", "service" : service, "message" : logMessage, "status" : 2})
            if self.websocket:
                try:
                    await self.websocket.send(message)
                    print(f"Sent message: {message}")
                except Exception as e:
                    print(f"Failed to send message to watchlog agent: {e}")
            else:
                await self.connect()
    async def errorLog(self, service , logMessage):
        if service and isinstance(service, str) and (isinstance(logMessage , str) ) :
            message = json.dumps({"method" : "log", "service" : service, "message" : logMessage, "status" : -1})
            if self.websocket:
                try:
                    await self.websocket.send(message)
                    print(f"Sent message: {message}")
                except Exception as e:
                    print(f"Failed to send message to watchlog agent: {e}")
            else:
                await self.connect()


    async def receive_messages(self):
        if self.websocket:
            try:
                async for message in self.websocket:
                    print(f"Received message: {message}")
            except Exception as e:
                print(f"Watchlog connection closed unexpectedly: {e}")
        else:
            await self.connect()


    async def close(self):
        if self.websocket:
            await self.websocket.close()
            print("Watchlog connection closed.")
        else:
            print("Watchlog connection is not established.")
