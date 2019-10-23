class PlayerInfo:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.gamemode = 0
        self.level = 0
        self.exp = 0

    def set_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
