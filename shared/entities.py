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

    def to_dict(self):
        return {
            'owner_id': self.owner_id,
            'x': self.x,
            'y': self.y,
            'angle': self.angle,
            'alive': self.alive
        }

    @classmethod
    def from_dict(cls, data):
        b = cls(data['owner_id'], data['x'], data['y'], data['angle'])
        b.alive = data.get('alive', True)
        return b

class Player:
    def __init__(self, player_id, writer=None):
        self.id = player_id
        self.x = 400
        self.y = 300
        self.angle = 0
        self.writer = writer
        self.health = 3

    def to_dict(self):
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'angle': self.angle,
            'health': self.health
        }

    @classmethod
    def from_dict(cls, data):
        p = cls(data['id'])
        p.x = data['x']
        p.y = data['y']
        p.angle = data['angle']
        p.health = data.get('health', 3)
        return p

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

    def to_dict(self):
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'type': self.type,
            'active': self.active
        }

    @classmethod
    def from_dict(cls, data):
        pu = cls(data['id'], data['x'], data['y'], data['type'])
        pu.active = data.get('active', True)
        return pu
