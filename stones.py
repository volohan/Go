from player_colors import Colors


class Goishi:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        if color == Colors.white:
            self.image = 'w'
        else:
            self.image = 'b'
        self.is_surrounded = False
