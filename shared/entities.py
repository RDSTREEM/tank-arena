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
