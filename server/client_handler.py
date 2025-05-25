import asyncio
import json

connected_clients = []

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"[CONNECT] New client connected: {addr}")
    connected_clients.append(writer)

    try:
        while True:
            data = await reader.readline()
            if not data:
                break

            message = data.decode().strip()
            print(f"[RECV] {addr}: {message}")

            try:
                packet = json.loads(message)
                await handle_packet(packet, writer)
            except json.JSONDecodeError:
                print(f"[ERROR] Invalid packet from {addr}")

    except (asyncio.CancelledError, ConnectionResetError):
        print(f"[DISCONNECT] Client {addr} lost connection")
    finally:
        connected_clients.remove(writer)
        writer.close()
        await writer.wait_closed()
        print(f"[CLOSE] Client {addr} connection closed")

async def handle_packet(packet, writer):
    if packet.get("type") == "ping":
        response = {"type": "pong"}
        await send_packet(writer, response)

async def send_packet(writer, data):
    message = json.dumps(data) + "\n"
    writer.write(message.encode())
    await writer.drain()
