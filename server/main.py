import asyncio
from server.client_handler import handle_client

HOST = '192.168.8.112'
PORT = 9000

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f"[SERVER] Listening on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
