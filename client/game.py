import pygame
import math

TANK_SPEED = 200 
TANK_ROT_SPEED = 200

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tank_pos = pygame.Vector2(width // 2, height // 2)
        self.tank_angle = 0 
        self.tank_image = pygame.Surface((50, 30), pygame.SRCALPHA)
        pygame.draw.rect(self.tank_image, (0, 200, 0), (0, 0, 50, 30))
        pygame.draw.circle(self.tank_image, (0, 100, 0), (10, 15), 6)

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

    def update(self, dt):
        self.dt = dt
    def draw(self, surface):
        surface.fill((30, 30, 30))
        rotated_image = pygame.transform.rotate(self.tank_image, self.tank_angle)
        rect = rotated_image.get_rect(center=self.tank_pos)

        surface.blit(rotated_image, rect.topleft)
