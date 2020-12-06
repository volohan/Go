from board import Goban
from player_colors import Colors
from opponent import GoOpponentAI
from sys import exit

__author__ = 'Nikolai V.'
__version__ = '0.2.1 Pre-Alpha'


class GoEngine:
    def __init__(self):
        self.board = Goban(9, 0.5)
        self.is_end = True
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
        self.main_loop()

    def main_loop(self):
        while not self.is_end:
            print(' ')
            print(self.board.get_map())
            print('----------------------------------------------------------')

            if self.next_move == self.player_color:
                move = self.demand_move()
            else:
                move = self.opponent.move()

            if move:
                is_success = self.board.make_move(move[0], move[1], self.next_move)

                if not is_success:
                    self.illegal_move()
                    continue

                self.player_pass = False
            else:
                if self.player_pass:
                    break
                else:
                    self.player_pass = True

            if self.two_players:
                self.player_color = Colors(-self.next_move)
            self.next_move = Colors(-self.next_move)

        scores = self.board.score()
        if scores[Colors.white] > scores[Colors.black]:
            self.announce_winner(Colors.white)
        else:
            self.announce_winner(Colors.black)

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
              '"* *" (где * число 1-19) - координата поля по '
              'горизонтали (с лева на право) и по вертикали (снизу '
              'вверх)\n\n'
              '"rules" - правила игры\n\n'
              '"map" - показать доску игры\n\n'
              '"help" - этот текст\n\n'
              '"exit" - выход\n'
              '----------------------------------------------------\n')

    def print_default(self):
        print('Странный ты человек, конечно.\nЯ хочу от тебя ход, '
              'а ты пишешь мне такое...\n--------(Use "help")--------')

    def print_rules(self):
        print("Sorry, it's not working yet")

    def print_map(self):
        print(self.board.get_map())

    def demand_move(self):
        while True:
            try:
                player_response = input()
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
                elif player_response == 'rules':
                    self.print_rules()
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
    x = GoEngine()
    x.start(True)
