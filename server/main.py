import asyncio
from server.client_handler import handle_client  # You'll implement this module

HOST = '0.0.0.0'
PORT = 9000

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f"[SERVER] Listening on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
