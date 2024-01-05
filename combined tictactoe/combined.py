import math
import random
import time
from tkinter import *

class Player:
    def __init__(self, letter):
        self.letter = letter

    def make_move(self, game):
        self.game = game

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def make_move(self, game):
        tiles = random.choice(game.assessible_moves())
        return tiles

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def make_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            tiles = input(self.letter + '\'s turn, input move (0-8):')

            try:
                val = int(tiles)
                if val not in game.assessible_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid input, try again.')

        return val

class UnbeatableAiPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def make_move(self, game):
        if len(game.assessible_moves()) == 9:
            tiles = random.choice(game.assessible_moves())
        else:
            tiles = self.minimax(game, self.letter)['position']
        return tiles

    def minimax(self, game, player):
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if game.current_winner == other_player:
            return {'position': None,
                    'score': 1 * (game.num_empty_squares() + 1) if other_player == max_player else -1 *
                        (game.num_empty_squares() + 1)
                    }

        elif not game.num_empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            optimal = {'position': None, 'score': -math.inf}
        else:
            optimal = {'position': None, 'score': math.inf}

        for possible_move in game.assessible_moves():
            game.make_move(possible_move, player)

            sim_score = self.minimax(game, other_player)

            game.board[possible_move] = ' '
            game.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > optimal['score']:
                    optimal = sim_score
            else:
                if sim_score['score'] < optimal['score']:
                    optimal = sim_score

        return optimal


class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i * 3:(i + 1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_num():
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def assessible_moves(self):
        return [i for i, mix in enumerate(self.board) if mix == ' ']

    def empty_tiles(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, tiles, letter):
        if self.board[tiles] == ' ':
            self.board[tiles] = letter
            if self.winner(tiles, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, tiles, letter):
        row_ind = tiles // 3
        row = self.board[row_ind * 3: (row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True

        col_ind = tiles % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        if tiles % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        return False


def next_turn(row, column):
    global player

    if buttons[row][column]['text'] == "" and check_winner() is False:

        if player == players[0]:
            buttons[row][column]['text'] = player

            if check_winner() is False:
                player = players[1]
                Label.config(text=(players[1]+" turn"))

            elif check_winner() is True:
                Label.config(text=(players[0]+" wins"))

            elif check_winner() == "Tie":
                Label.config(text=("Tie:"))

        else:

            buttons[row][column]['text'] = player

            if check_winner() is False:
                player = players[0]
                Label.config(text=(players[0]+" turn"))

            elif check_winner() is True:
                Label.config(text=(players[1]+" wins"))

            elif check_winner() == "Tie":
                Label.config(text=("Tie:"))


def check_winner():
    for row in range(3):
        if buttons[row][0]["text"] == buttons[row][1]['text'] == buttons[row][2]['text'] != "":
            buttons[row][0].config(bg="green")
            buttons[row][1].config(bg="green")
            buttons[row][2].config(bg="green")
            return True
        
    for column in range(3):
        if buttons[0][column]["text"] == buttons[1][column]['text'] == buttons[2][column]['text'] != "":
            buttons[0][column].config(bg="green")
            buttons[1][column].config(bg="green")
            buttons[2][column].config(bg="green")         
            return True   

    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        buttons[0][0].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][2].config(bg="green")   
        return True
    
    elif buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        buttons[0][2].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][0].config(bg="green")   
        return True
    
    elif empty_space() is False:
        for row in range(3):
            for column in range(3):
                buttons[row][column].config(bg="yellow") 
        return "Tie"
    
    else:
        return False


def empty_space():
    spaces = 9
    for row in range(3):
        for column in range(3):
            if buttons[row][column]['text'] != "":
                spaces -= 1
    if spaces == 0:
        return False
    else:
        return True


def new_game():
    global player
    player = random.choice(players)
    Label.config(text=player+" turn")
    for row in range(3):
        for column in range(3):
            buttons[row][column].config(text="", bg="#F0F0F0")


window = Tk()
window.title("Tic-Tac-Toe")
players = ["x", "o"]
player = random.choice(players)
buttons = [[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]]

Label = Label(text=player + " turn", font=('montseratt', 40))
Label.pack(side="top")

reset_button = Button(text="restart", font=('montseratt', 20), command=new_game)
reset_button.pack(side="top")

frame = Frame(window)
frame.pack()

for row in range(3):
    for column in range(3):
        buttons[row][column] = Button(frame, text="", font=('montseratt', 20),
                                      width=5, height=2, command=lambda row=row, column=column: next_turn(row, column))
        buttons[row][column].grid(row=row, column=column)

window.mainloop()
