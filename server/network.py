import asyncio
import json

class NetworkClient:
    def __init__(self, host='localhost', port=9000):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.incoming_messages = asyncio.Queue()

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        print(f"[CLIENT] Connected to server at {self.host}:{self.port}")
        asyncio.create_task(self.listen())

    async def listen(self):
        while True:
            try:
                data = await self.reader.readline()
                if not data:
                    print("[CLIENT] Server closed connection")
                    break
                message = json.loads(data.decode().strip())
                await self.incoming_messages.put(message)
            except (json.JSONDecodeError, ConnectionResetError):
                break

    async def send(self, packet: dict):
        if self.writer:
            message = json.dumps(packet) + "\n"
            self.writer.write(message.encode())
            await self.writer.drain()

    async def get_message(self):
        return await self.incoming_messages.get()
