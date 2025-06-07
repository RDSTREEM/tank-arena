import pygame
import math
import asyncio
from client.network import NetworkClient

TANK_SPEED = 200 
TANK_ROT_SPEED = 200
BULLET_SPEED = 400
BULLET_RADIUS = 5
BULLET_COLOR = (255, 220, 0)

class Bullet:
    def __init__(self, pos, angle):
        self.pos = pygame.Vector2(pos)
        self.angle = angle
        direction = pygame.Vector2(1, 0).rotate(-angle)
        self.velocity = direction * BULLET_SPEED
        self.alive = True

    def update(self, dt, width, height):
        self.pos += self.velocity * dt
        # Remove bullet if it goes off screen
        if (
            self.pos.x < 0 or self.pos.x > width or
            self.pos.y < 0 or self.pos.y > height
        ):
            self.alive = False

    def draw(self, surface):
        pygame.draw.circle(surface, BULLET_COLOR, (int(self.pos.x), int(self.pos.y)), BULLET_RADIUS)

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tank_pos = pygame.Vector2(width // 2, height // 2)
        self.tank_angle = 0 
        self.tank_image = pygame.Surface((50, 30), pygame.SRCALPHA)
        pygame.draw.rect(self.tank_image, (0, 200, 0), (0, 0, 50, 30))
        pygame.draw.circle(self.tank_image, (0, 100, 0), (10, 15), 6)
        self.bullets = []
        self.shoot_cooldown = 0
        self.network = NetworkClient()
        self.player_id = None
        self.other_players = {}  # id: {'x':..., 'y':..., 'angle':...}
        self.network_task = asyncio.create_task(self.network_main())

    async def network_main(self):
        await self.network.connect()
        # Wait for init packet
        while True:
            msg = await self.network.get_message()
            if msg.get('type') == 'init':
                self.player_id = msg['id']
                break
        # Start listening for world state
        asyncio.create_task(self.listen_world_state())

    async def listen_world_state(self):
        while True:
            msg = await self.network.get_message()
            if msg.get('type') == 'world_state':
                self.other_players = {p['id']: p for p in msg['players'] if p['id'] != self.player_id}

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.tank_angle += TANK_ROT_SPEED * self.dt
        if keys[pygame.K_d]:
            self.tank_angle -= TANK_ROT_SPEED * self.dt

        direction = pygame.Vector2(1, 0).rotate(-self.tank_angle)
        if keys[pygame.K_w]:
            self.tank_pos += direction * TANK_SPEED * self.dt
        if keys[pygame.K_s]:
            self.tank_pos -= direction * TANK_SPEED * self.dt

        # Shooting with space bar
        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
            bullet = Bullet(self.tank_pos, self.tank_angle)
            self.bullets.append(bullet)
            self.shoot_cooldown = 0.25  # 250ms cooldown

        # After movement, send update to server
        if self.player_id:
            asyncio.create_task(self.network.send({
                'type': 'update',
                'x': self.tank_pos.x,
                'y': self.tank_pos.y,
                'angle': self.tank_angle
            }))

    def update(self, dt):
        self.dt = dt
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
        # Update bullets
        for bullet in self.bullets:
            bullet.update(dt, self.width, self.height)
        # Remove dead bullets
        self.bullets = [b for b in self.bullets if b.alive]

    def draw(self, surface):
        surface.fill((30, 30, 30))
        rotated_image = pygame.transform.rotate(self.tank_image, self.tank_angle)
        rect = rotated_image.get_rect(center=self.tank_pos)
        surface.blit(rotated_image, rect.topleft)
        # Draw other players
        for p in self.other_players.values():
            tank_img = pygame.transform.rotate(self.tank_image, p['angle'])
            rect = tank_img.get_rect(center=(p['x'], p['y']))
            surface.blit(tank_img, rect.topleft)
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(surface)
