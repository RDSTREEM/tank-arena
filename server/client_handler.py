from server.world_state import players, Player
import uuid
import json

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    player_id = str(uuid.uuid4())[:8]
    players[player_id] = Player(player_id, writer)
    print(f"[CONNECT] {player_id} joined from {addr}")
    await send_packet(writer, {"type": "init", "id": player_id})

    try:
        while True:
            data = await reader.readline()
            if not data:
                break

            message = data.decode().strip()
            packet = json.loads(message)
            await handle_packet(packet, player_id)
    except Exception as e:
        print(f"[ERROR] {player_id}: {e}")
    finally:
        del players[player_id]
        writer.close()
        await writer.wait_closed()
        print(f"[DISCONNECT] {player_id} disconnected")

async def send_packet(writer, packet):
    message = json.dumps(packet) + "\n"
    writer.write(message.encode())
    await writer.drain()

async def handle_packet(packet, player_id):
    if packet["type"] == "update":
        player = players[player_id]
        player.x = packet["x"]
        player.y = packet["y"]
        player.angle = packet["angle"]
        await broadcast_world_state()

async def broadcast_world_state():
    state = {
        "type": "world_state",
        "players": [
            {"id": p.id, "x": p.x, "y": p.y, "angle": p.angle}
            for p in players.values()
        ]
    }
    for p in players.values():
        await send_packet(p.writer, state)