from notation import GoNotation
from board import Goban


class Analyzer:
    def __init__(self, path):
        self.notation = GoNotation()
        self.current = self.notation.open_existing(path)
        self.count_moves_displayed = 10
        self.start()

    def start(self):
        self.current_move = 0
        self.board = Goban(self.notation.size, self.notation.komi)
        self.main_loop()

    def display(self, str):
        while len(str) < 8:
            str = ' ' + str
        print(str + '|', end='')

    def main_loop(self):
        while True:
            print(self.board.get_map())
            self.print_branch()

            print('\n--------------------------------------------------------')
            try:
                response = input()
                print()
                if response == 'help':
                    self.print_help()
                elif response == 'exit':
                    exit(0)
                else:
                    self.print_default()
            except EOFError:
                self.print_default()

    def print_branch(self):
        for i in range(self.current_move, self.count_moves_displayed + 1):
            self.display(str(i + 1))
        print()
        for i in range(self.current_move, self.count_moves_displayed + 1):
            move = self.current.moves[i]
            self.display(f'{move[2].name[0]}[{move[0]},{move[1]}]')
        print()
        for i in range(self.current_move, self.count_moves_displayed + 1):
            if i in self.current.branches:
                self.display(str(len(self.current.branches[i])))
            else:
                self.display('0')
        print()

    def print_help(self):
        print(
              f'"* *" (где * число 1-{self.board.size}) - координата поля по '
              'горизонтали (с лева на право) и по вертикали (снизу '
              'вверх) чтобы начать новую ветку\n\n'
              '"*" (где * номер хода) - перейти на этот ход\n\n'
              '"down" - спуститься на ветку ниже'
              '"help" - этот текст\n\n'
              '"exit" - выход\n')

    def print_default(self):
        print('Не понимаю...Что ты написал?\n'
              '--------(Use "help")--------')


if __name__ == '__main__':
    path = r'.\parties\2020-12-15_01-01-54.GoNotation'
    Analyzer(path)
