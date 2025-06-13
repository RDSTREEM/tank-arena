from server.world_state import players, Player, bullets, Bullet
import uuid
import json
import math

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
    elif packet["type"] == "shoot":
        b = Bullet(player_id, packet["x"], packet["y"], packet["angle"])
        bullets.append(b)
        await broadcast_world_state()

async def broadcast_world_state():
    # Move bullets
    dt = 1/60  # Assume 60 FPS tick for now
    width, height = 800, 600
    for b in bullets:
        b.update(dt, width, height)
    # Collision detection: bullets vs players
    bullet_radius = 5
    player_radius = 20
    players_to_remove = []
    for b in bullets:
        if not b.alive:
            continue
        for p in players.values():
            if p.id == b.owner_id:
                continue  # Don't hit owner
            dx = b.x - p.x
            dy = b.y - p.y
            dist = math.hypot(dx, dy)
            if dist < bullet_radius + player_radius:
                b.alive = False
                p.health -= 1
                print(f"[HIT] Player {p.id} was hit by {b.owner_id}, health: {p.health}")
                if p.health <= 0:
                    players_to_remove.append(p.id)
                break
    # Remove dead players
    for pid in players_to_remove:
        del players[pid]
    # Remove dead bullets
    bullets[:] = [b for b in bullets if b.alive]
    state = {
        "type": "world_state",
        "players": [
            {"id": p.id, "x": p.x, "y": p.y, "angle": p.angle, "health": p.health}
            for p in players.values()
        ],
        "bullets": [
            {"owner_id": b.owner_id, "x": b.x, "y": b.y, "angle": b.angle}
            for b in bullets if b.alive
        ]
    }
    for p in players.values():
        await send_packet(p.writer, state)