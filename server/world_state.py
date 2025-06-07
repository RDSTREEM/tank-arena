class Player:
    def __init__(self, player_id, writer):
        self.id = player_id
        self.x = 400
        self.y = 300
        self.angle = 0
        self.writer = writer
        # Add more state as needed (e.g., bullets)

players = {}
