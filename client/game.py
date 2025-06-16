import pygame
import math
import asyncio
from client.network import NetworkClient
from shared.entities import Bullet as SharedBullet, Player as SharedPlayer

TANK_SPEED = 200 
TANK_ROT_SPEED = 200
BULLET_RADIUS = 5
BULLET_COLOR = (255, 220, 0)

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = SharedPlayer('local')
        self.tank_image = pygame.Surface((50, 30), pygame.SRCALPHA)
        pygame.draw.rect(self.tank_image, (0, 200, 0), (0, 0, 50, 30))
        pygame.draw.circle(self.tank_image, (0, 100, 0), (10, 15), 6)
        self.bullets = []
        self.shoot_cooldown = 0
        self.network = NetworkClient()
        self.player_id = None
        self.other_players = {}  # id: SharedPlayer
        self.network_task = asyncio.create_task(self.network_main())

    async def network_main(self):
        await self.network.connect()
        while True:
            msg = await self.network.get_message()
            if msg.get('type') == 'init':
                self.player_id = msg['id']
                self.player.id = self.player_id
                break
        asyncio.create_task(self.listen_world_state())

    async def listen_world_state(self):
        while True:
            msg = await self.network.get_message()
            if msg.get('type') == 'world_state':
                self.other_players = {p['id']: SharedPlayer.from_dict(p) for p in msg['players'] if p['id'] != self.player_id}
                self.bullets = [SharedBullet.from_dict(b) for b in msg.get('bullets', [])]

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.angle += TANK_ROT_SPEED * self.dt
        if keys[pygame.K_d]:
            self.player.angle -= TANK_ROT_SPEED * self.dt

        direction = pygame.Vector2(1, 0).rotate(-self.player.angle)
        if keys[pygame.K_w]:
            self.player.x += direction.x * TANK_SPEED * self.dt
            self.player.y += direction.y * TANK_SPEED * self.dt
        if keys[pygame.K_s]:
            self.player.x -= direction.x * TANK_SPEED * self.dt
            self.player.y -= direction.y * TANK_SPEED * self.dt

        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0 and self.player_id:
            asyncio.create_task(self.network.send({
                'type': 'shoot',
                'x': self.player.x,
                'y': self.player.y,
                'angle': self.player.angle
            }))
            self.shoot_cooldown = 0.25

        if self.player_id:
            asyncio.create_task(self.network.send({
                'type': 'update',
                'x': self.player.x,
                'y': self.player.y,
                'angle': self.player.angle
            }))

    def update(self, dt):
        self.dt = dt
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

    def draw(self, surface):
        surface.fill((30, 30, 30))
        rotated_image = pygame.transform.rotate(self.tank_image, self.player.angle)
        rect = rotated_image.get_rect(center=(self.player.x, self.player.y))
        surface.blit(rotated_image, rect.topleft)
        for p in self.other_players.values():
            tank_img = pygame.transform.rotate(self.tank_image, p.angle)
            rect = tank_img.get_rect(center=(p.x, p.y))
            surface.blit(tank_img, rect.topleft)
        for bullet in self.bullets:
            pygame.draw.circle(surface, BULLET_COLOR, (int(bullet.x), int(bullet.y)), BULLET_RADIUS)
