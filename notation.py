import os


class GoNotation:
    def create_new_notation(self, name, board_size, board_komi):
        self.path = os.path.join('parties', f'{name}.GoNotation')
        self.file = open(self.path, 'w', encoding='utf-8')
        self.file.write(f'{board_size}_{board_komi}\n')

    def record_move(self, x, y, color):
        self.file.write(f'{color.name[0]}[{x},{y}]_')
