import pygame
import math

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
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(surface)
