import math

class Bullet:
    def __init__(self, owner_id, x, y, angle):
        self.owner_id = owner_id
        self.x = x
        self.y = y
        self.angle = angle
        self.alive = True

    def update(self, dt, width, height, speed=400):
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * speed * dt
        self.y -= math.sin(rad) * speed * dt
        if self.x < 0 or self.x > width or self.y < 0 or self.y > height:
            self.alive = False

class Player:
    def __init__(self, player_id, writer=None):
        self.id = player_id
        self.x = 400
        self.y = 300
        self.angle = 0
        self.writer = writer
        self.health = 3

class PowerUp:
    def __init__(self, powerup_id, x, y, type):
        self.id = powerup_id
        self.x = x
        self.y = y
        self.type = type  # e.g., 'health', 'speed', 'shield', etc.
        self.active = True

    def apply(self, player):
        if self.type == 'health':
            player.health += 1
        elif self.type == 'speed':
            player.speed = getattr(player, 'speed', 1.0) * 1.5
        elif self.type == 'shield':
            player.shield = True
        # Add more powerup types as needed
        self.active = False
