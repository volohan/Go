from datetime import datetime
from board import Goban
from player_colors import Colors
from opponent import GoOpponentAI
from sys import exit
from notation import GoNotation

__author__ = 'Nikolai V.'
__version__ = '0.4 Beta'


class GoEngine:
    def __init__(self, size, komi):
        self.board = Goban(size, komi)
        self.is_end = True
        self.notation = GoNotation()
        self.next_move = Colors.black

    def start(self, two_players, player_color=Colors.black):
        self.two_players = two_players
        if self.two_players:
            self.player_color = Colors.black
        else:
            self.player_color = player_color
            self.opponent = GoOpponentAI(Colors(-player_color))

        self.salutation()

        self.is_end = False
        self.player_pass = False

        name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.notation.create_new_notation(name, self.board.size,
                                          self.board.komi)
        self.main_loop()

    def main_loop(self):
        while not self.is_end:
            print(self.board.get_map())
            print('----------------------------------------------------------')

            if self.next_move == self.player_color:
                move = self.demand_move()
            else:
                move = self.opponent.move()

            if move:
                is_success = self.board.make_move(move[0], move[1],
                                                  self.next_move)

                if not is_success:
                    self.illegal_move()
                    continue

                self.notation.record_move(move[0], move[1], self.next_move)
                self.player_pass = False
            else:
                if self.player_pass:
                    break
                else:
                    self.player_pass = True

            if self.two_players:
                self.player_color = Colors(-self.next_move)
            self.next_move = Colors(-self.next_move)

        scores = self.board.score(True)
        self.print_score()
        if scores[Colors.black] > scores[Colors.white]:
            self.announce_winner(Colors.black)
        else:
            self.announce_winner(Colors.white)

    def illegal_move(self):
        print('!!!!Невозможный  ход!!!!\n'
              'Ознокомьтесь с правилами\n'
              '------(Use "help")------\n')

    def salutation(self):
        print('(ノ-_-)ノﾞ_□ VS □_ヾ(^-^ヽ)\n'
              f'Go on Python by {__author__}\n'
              f'(version: {__version__})')

    def announce_winner(self, winner):
        print(f'{winner.name} won!\n'
              f'☆*:.｡.o(≧▽≦)o.｡.:*☆'
              f'\n.\n.\n.\n.\n.\n.\n'
              f'{Colors(-winner).name}: (╮°-°)╮┳━━┳ ( ╯°□°)╯ ┻━━┻')

    def print_help(self):
        print('----------------------------------------------------\n'
              f'"* *" (где * число 1-{self.board.size}) - координата поля по '
              'горизонтали (с лева на право) и по вертикали (снизу '
              'вверх)\n\n'
              '"rules" - правила игры\n\n'
              '"zen" - дзен игры\n\n'
              '"map" - показать доску игры\n\n'
              '"help" - этот текст\n\n'
              '"exit" - выход\n'
              '----------------------------------------------------\n')

    def print_default(self):
        print('Не понимаю... Что ты написал?\n'
              '--------(Use "help")--------')

    def print_rules(self):
        with open('rules.txt', 'r', encoding='utf-8') as rules:
            for line in rules.readlines():
                print(line)

    def print_zen(self):
        with open('zen.txt', 'r', encoding='utf-8') as zen:
            for line in zen.readlines():
                print(line)

    def print_map(self):
        print(self.board.get_map())

    def print_score(self):
        score = self.board.score(False)
        print(f'Black: {score[Colors.black]}\n'
              f'White: {score[Colors.white] + self.board.komi}\n')

    def demand_move(self):
        while True:
            try:
                player_response = input()
                print(' ')
                try:
                    coordinate = [int(i) for i in player_response.split(' ')]
                    if len(coordinate) == 2 \
                            and 0 < coordinate[0] <= self.board.size \
                            and 0 < coordinate[1] <= self.board.size:
                        return coordinate
                except ValueError:
                    pass
                if player_response == 'map':
                    self.print_map()
                elif player_response == 'score':
                    self.print_score()
                elif player_response == 'rules':
                    self.print_rules()
                elif player_response == 'zen':
                    self.print_zen()
                elif player_response == 'help':
                    self.print_help()
                elif player_response == 'pass':
                    return None
                elif player_response == 'exit':
                    exit(0)
                else:
                    self.print_default()
            except EOFError:
                self.print_default()


if __name__ == '__main__':
    x = GoEngine(9, 6.5)
    x.start(True)
