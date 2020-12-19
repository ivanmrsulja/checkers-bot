#NAPOMENA : Pokrenuti iz terminala na Linux operativnom sistemu

from copy import deepcopy
from time import time
import os

clear = lambda: os.system("clear")


class Move(object):   #samo za obavezne poteze covjeka

    def __init__(self, piece, destination, to_eat):
        self._piece = piece
        self._position = piece.get_position()
        self._destination = destination
        self._to_eat = to_eat

    def execute(self, board):
        board._board[self._position], board._board[self._destination] = board._board[self._destination], board._board[self._position]
        del board._white_pieces[self._position]
        self._piece.set_position(self._destination)
        board._board[self._to_eat] = 0
        del board._black_pieces[self._to_eat]
        board._white_pieces[self._piece.get_position()] = self._piece

    def __str__(self):
        return "Move {0:2} to {1:2} and eat {2:2} (Mandatory move)".format(self._piece.name, self._destination, self._to_eat)

class Piece(object):

    def __init__(self, position, color, name):
        self._position = position
        self._color = color
        self.name = name
        self.is_queen = False

    def get_position(self):
        return self._position

    def set_position(self, new):
        self._position = new
        if self._color == "white" and self._position > 55 and self.is_queen is False:
            self.is_queen = True
            self.name = "Q" + self.name
        elif self._color == "black" and self._position < 8 and self.is_queen is False:
            self.is_queen = True
            self.name = "Q" + self.name

    def get_color(self):
        return self._color

    def is_on_a_wall(self):
        wall_positions = [8, 16, 15, 23, 24, 31, 32, 39, 40, 47, 48, 55]
        if self._position in wall_positions:
            return True
        else:
            return False

    def is_on_a_right_wall(self):
        wall_positions = [15, 23, 31, 39, 47, 55]
        if self._position in wall_positions:
            return True
        else:
            return False

    def is_in_a_corner(self):
        corner_positions = [0, 7, 56, 63]
        if self._position in corner_positions:
            return True
        else:
            return False


class Board(object):

    def __init__(self):

        while True:
            choice = input("Is eating a mandatory move[Y/n]:")
            if choice == "Y":
                self._must_eat = True
                break
            elif choice == "n":
                self._must_eat = False
                break
            else:
                print("Error, enter Y or n !")

        self._black_pieces = {}
        self._white_pieces = {}

        w1 = Piece(0, "white", "W1")
        w2 = Piece(2, "white", "W2")
        w3 = Piece(4, "white", "W3")
        w4 = Piece(6, "white", "W4")
        w5 = Piece(9, "white", "W5")
        w6 = Piece(11, "white", "W6")
        w7 = Piece(13, "white", "W7")
        w8 = Piece(15, "white", "W8")
        w9 = Piece(16, "white", "W9")
        w10 = Piece(18, "white", "Wx")
        w11 = Piece(20, "white", "Wy")
        w12 = Piece(22, "white", "Wz")

        b1 = Piece(57, "black", "B1")
        b2 = Piece(59, "black", "B2")
        b3 = Piece(61, "black", "B3")
        b4 = Piece(63, "black", "B4")
        b5 = Piece(48, "black", "B5")
        b6 = Piece(50, "black", "B6")
        b7 = Piece(52, "black", "B7")
        b8 = Piece(54, "black", "B8")
        b9 = Piece(41, "black", "B9")
        b10 = Piece(43, "black", "Bx")
        b11 = Piece(45, "black", "By")
        b12 = Piece(47, "black", "Bz")

        self._board = [w1, 0, w2, 0, w3, 0, w4, 0,
                       0, w5, 0, w6, 0, w7, 0, w8,
                       w9, 0, w10, 0, w11, 0, w12, 0,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       0, b9, 0, b10, 0, b11, 0, b12,
                       b5, 0, b6, 0, b7, 0, b8, 0,
                       0, b1, 0, b2, 0, b3, 0, b4
                       ]

        for element in self._board:
            if element:
                if element.get_color() == "white":
                    self._white_pieces[element.get_position()] = element
                else:
                    self._black_pieces[element.get_position()] = element

        self.print_board()

    def try_right_down(self, piece, moves, board):
        if board[piece.get_position() + 9]:
            try:
                if board[piece.get_position() + 18] == 0 and board[
                    piece.get_position() + 9].get_color() != piece.get_color() and board[
                    piece.get_position() + 9].is_on_a_wall() is False and board[
                    piece.get_position() + 9].is_in_a_corner() is False:
                    moves[piece.get_position() + 18] = piece.get_position() + 9
            except:
                return
        else:
            moves[piece.get_position() + 9] = "move"

    def try_left_down(self, piece, moves, board):
        if board[piece.get_position() + 7]:
            try:
                if board[piece.get_position() + 14] == 0 and board[
                    piece.get_position() + 7].get_color() != piece.get_color() and board[
                    piece.get_position() + 7].is_on_a_wall() is False and board[
                    piece.get_position() + 7].is_in_a_corner() is False:
                    moves[piece.get_position() + 14] = piece.get_position() + 7
            except:
                return
        else:
            moves[piece.get_position() + 7] = "move"

    def try_right_up(self, piece, moves, board):
        if board[piece.get_position() - 7]:
            try:
                if board[piece.get_position() - 14] == 0 and board[
                    piece.get_position() - 7].get_color() != piece.get_color() and board[
                    piece.get_position() - 7].is_on_a_wall() is False and board[
                    piece.get_position() - 7].is_in_a_corner() is False and piece.get_position() - 14 >= 0:
                    moves[piece.get_position() - 14] = piece.get_position() - 7
            except:
                return
        else:
            moves[piece.get_position() - 7] = "move"

    def try_left_up(self, piece, moves, board):
        if board[piece.get_position() - 9]:
            try:
                if board[piece.get_position() - 18] == 0 and board[
                    piece.get_position() - 9].get_color() != piece.get_color() and board[
                    piece.get_position() - 9].is_on_a_wall() is False and board[
                    piece.get_position() - 9].is_in_a_corner() is False and piece.get_position() - 18 >= 0:
                    moves[piece.get_position() - 18] = piece.get_position() - 9
            except:
                return
        else:
            moves[piece.get_position() - 9] = "move"

    def print_board(self):
        clear()
        print()
        counter = 0
        for i in range(63,-1,-1):
            if self._board[i]:
                if self._board[i].is_queen:
                    print(self._board[i].name + "  |   ", end="")
                else:
                    print(self._board[i].name + "   |   ", end="")
            else:
                print("-    |   ", end="")
            counter += 1
            if counter > 7:
                print()
                counter = 0

    def all_possible_moves(self, piece):  # prima figuru i vraca sve poteze za nju
        moves = {}
        if piece.is_in_a_corner():
            if piece.get_position() == 0:
                self.try_right_down(piece, moves, self._board)
            elif piece.get_position() == 7:
                self.try_left_down(piece, moves, self._board)
            elif piece.get_position() == 56:
                self.try_right_up(piece, moves, self._board)
            elif piece.get_position() == 63:
                self.try_left_up(piece, moves, self._board)
        elif piece.is_queen:
            if piece.get_position() < 8:
                self.try_left_down(piece, moves, self._board)
                self.try_right_down(piece, moves, self._board)
            elif piece.get_position() > 55:
                self.try_left_up(piece, moves, self._board)
                self.try_right_up(piece, moves, self._board)
            elif piece.is_on_a_wall():
                if piece.is_on_a_right_wall():
                    self.try_left_up(piece, moves, self._board)
                    self.try_left_down(piece, moves, self._board)
                else:
                    self.try_right_up(piece, moves, self._board)
                    self.try_right_down(piece, moves, self._board)
            else:
                self.try_left_up(piece, moves, self._board)
                self.try_left_down(piece, moves, self._board)
                self.try_right_up(piece, moves, self._board)
                self.try_right_down(piece, moves, self._board)
        elif piece.is_on_a_wall():
            if piece.is_on_a_right_wall():
                self.try_left_down(piece, moves, self._board)
            else:
                self.try_right_down(piece, moves, self._board)
        else:
            self.try_left_down(piece, moves, self._board)
            self.try_right_down(piece, moves, self._board)
        return moves

    def all_possible_moves_AI(self, piece):  # vraca sve trenutne poteze za datu crnu figuru
        moves = {}
        if piece.is_in_a_corner():
            if piece.get_position() == 0:
                self.try_right_down(piece, moves, self._board)
            elif piece.get_position() == 7:
                self.try_left_down(piece, moves, self._board)
            elif piece.get_position() == 56:
                self.try_right_up(piece, moves, self._board)
            elif piece.get_position() == 63:
                self.try_left_up(piece, moves, self._board)
        elif piece.is_queen:
            if piece.get_position() < 8:
                self.try_left_down(piece, moves, self._board)
                self.try_right_down(piece, moves, self._board)
            elif piece.get_position() > 55:
                self.try_left_up(piece, moves, self._board)
                self.try_right_up(piece, moves, self._board)
            elif piece.is_on_a_wall():
                if piece.is_on_a_right_wall():
                    self.try_left_down(piece, moves, self._board)
                    self.try_left_up(piece, moves, self._board)
                else:
                    self.try_right_up(piece, moves, self._board)
                    self.try_right_down(piece, moves, self._board)
            else:
                self.try_left_up(piece, moves, self._board)
                self.try_left_down(piece, moves, self._board)
                self.try_right_up(piece, moves, self._board)
                self.try_right_down(piece, moves, self._board)
        elif piece.is_on_a_wall():
            if piece.is_on_a_right_wall():
                self.try_left_up(piece, moves, self._board)
            else:
                self.try_right_up(piece, moves, self._board)
        else:
            self.try_left_up(piece, moves, self._board)
            self.try_right_up(piece, moves, self._board)
        return moves

    def all_moves_hooman(self):  # vraca sve trenutne poteze koje coek moze napraviti na tabli
        for_return = []
        for piece in self._white_pieces.values():
            new = self.all_possible_moves(piece)
            pair = (piece.get_position(), new)
            for_return.append(pair)
        return for_return

    def all_moves_compooter(self):
        for_return = []
        for piece in self._black_pieces.values():
            new = self.all_possible_moves_AI(piece)
            pair = (piece.get_position(), new)
            for_return.append(pair)
        return for_return

    def get_eating_moves(self):
        for_return = {}
        piece = -1
        moves = self.all_moves_hooman()
        for pair in moves:
            for move in pair[1]:
                if pair[1][move] != "move":
                    piece = pair[0]
                    new = Move(self._board[piece], move, pair[1][move])
                    for_return[move] = new
        return for_return



    def play_human(self):
        if self._must_eat:
            check = []
            try_moves = self.get_eating_moves()
            if len(try_moves) != 0 :
                for key in try_moves:
                    check.append(key)
                    print(try_moves[key])
                while True:
                    try:
                        choice = input(
                                "Enter only the final position of your figure (mandatory move) >> ")
                        if int(choice) in check:
                            try_moves[int(choice)].execute(self)
                            self.print_board()
                            return
                        else:
                            print("That action is not possible.")
                    except:
                        print("Error, try again. ")
        piece, moves = self.human_menu()
        for key in moves:
            if moves[key] == "move":
                print("Move ", piece.name, " on field ", key)
            elif moves[key] != "move":
                print("Move ", piece.name, " on field ", key, " and eat the piece on field ", moves[key])
        while True:
            try:
                choice = input(
                    "Enter only the final position of your piece or 'x' if you want to choose another one >> ")
                if choice == "x":
                    piece, moves = self.human_menu()
                    for key in moves:
                        if moves[key] == "move":
                            print("Move ", piece.name, " on field ", key)
                        elif moves[key] != "move":
                            print("Move ", piece.name, " on field ", key, " and eat the piece on field ",
                                  moves[key])
                elif int(choice) in moves.keys():
                    break
                else:
                    print("Error, try again. ")
            except:
                print("Error try again. ")
        if moves[int(choice)] == "move":
            self._board[piece.get_position()], self._board[int(choice)] = self._board[int(choice)], self._board[
                piece.get_position()]
            del self._white_pieces[piece.get_position()]
            piece.set_position(int(choice))
        else:
            self._board[piece.get_position()], self._board[int(choice)] = self._board[int(choice)], self._board[
                piece.get_position()]
            del self._white_pieces[piece.get_position()]
            piece.set_position(int(choice))
            self._board[moves[int(choice)]] = 0
            del self._black_pieces[moves[int(choice)]]
        self._white_pieces[piece.get_position()] = piece
        self.print_board()

    def human_menu(self):
        while True:
            try:
                choice = int(input("Enter the position of a piece that you want to select (0-63) >> "))
                if choice in self._white_pieces.keys():
                    break
                else:
                    print("There is no white piece on that field.")
            except:
                continue
        moves = self.all_possible_moves(self._white_pieces[choice])
        return self._white_pieces[choice], moves

    def play_computer(self):
        now = time()
        if self._must_eat:
            max = -1000
            moves = self.all_moves_compooter()
            for pair in moves:
                for move in pair[1]:
                    if pair[1][move] != "move":
                        new_board = deepcopy(self)
                        new_board.move_computer(pair[0], move, pair[1], False)
                        if new_board.evaluate_state() > max:
                            max, to_play = new_board.evaluate_state(), (pair[0], move, pair[1])
            if max != -1000:
                self.move_computer(to_play[0], to_play[1], to_play[2], True)
                print("That move was mandatory.")
                return
        max = -1000
        wanted = self.alphabeta(self, 4, -1000, 1000, True)
        moves = self.all_moves_compooter()
        for pair in moves:
            for move in pair[1]:
                new_board = deepcopy(self)
                new_board.move_computer(pair[0], move, pair[1], False)
                if new_board.evaluate_state() == wanted:
                    self.move_computer(pair[0], move, pair[1], True)
                    print(time()-now)
                    return
                elif new_board.evaluate_state() > max:
                    max, to_play = new_board.evaluate_state(), (pair[0], move, pair[1])   #ovde upadne kad pogresi pri racunanju
        self.move_computer(to_play[0], to_play[1], to_play[2], True)
        print(time() - now)

    def move_computer(self, position, destination, moves, to_print):
        piece = self._black_pieces[position]
        if moves[destination] == "move":
            self._board[position], self._board[destination] = self._board[destination], self._board[position]
            del self._black_pieces[position]
            piece.set_position(destination)
        else:
            self._board[position], self._board[destination] = self._board[destination], self._board[position]
            del self._black_pieces[position]
            piece.set_position(destination)
            self._board[moves[destination]] = 0
            del self._white_pieces[moves[destination]]
        self._black_pieces[piece.get_position()] = piece
        if to_print:
            self.print_board()

    def move_human(self, position, destination, moves):
        piece = self._white_pieces[position]
        if moves[destination] == "move":
            self._board[position], self._board[destination] = self._board[destination], self._board[position]
            del self._white_pieces[position]
            piece.set_position(destination)
        else:
            self._board[position], self._board[destination] = self._board[destination], self._board[position]
            del self._white_pieces[position]
            piece.set_position(destination)
            self._board[moves[destination]] = 0
            del self._black_pieces[moves[destination]]
        self._white_pieces[piece.get_position()] = piece

    def evaluate_state(self):
        value = 0
        for piece in self._board:
            if piece != 0 and piece.get_color() == "white":
                if piece.get_position() > 47:
                    value -= 3
                if piece.is_on_a_wall():
                    value -= 2
                if piece.is_queen:
                    value -= 4
                if piece:
                    value -= 1
            elif piece != 0:
                if piece.get_position() < 8 :
                    value += 3
                if piece.is_on_a_wall():
                    value += 2
                if piece.is_queen:
                    value += 4
                if piece:
                    value += 1
        return value

    def alphabeta(self, board, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or board.isTerminalState():
            if board.isTerminalState() and maximizingPlayer:
                return -1000
            elif board.isTerminalState():
                return 1000
            return board.evaluate_state()
        if maximizingPlayer:
            flag = 0
            value = -1000
            moves = board.all_moves_compooter()
            for pair in moves:
                for move in pair[1]:
                    new_board = deepcopy(board)
                    new_board.move_computer(pair[0], move, pair[1], False)
                    value = max(value, new_board.alphabeta(new_board, depth - 1, alpha, beta, False))
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        flag = 1
                        break
                if flag == 1:
                    break
            return value
        else:
            flag = 0
            value = 1000
            moves = board.all_moves_hooman()
            for pair in moves:
                for move in pair[1]:
                    new_board = deepcopy(board)
                    new_board.move_human(pair[0], move, pair[1])
                    value = min(value, new_board.alphabeta(new_board, depth - 1, alpha, beta, True))
                    beta = min(beta, value)
                    if alpha >= beta:
                        flag = 1
                        break
                if flag == 1:
                    break
            return value

    def isTerminalState(self):
        if len(self._black_pieces) < 4:
            return True
        if len(self._white_pieces) < 4:
            return True
        else:
            return False

    def gameplay(self):
        while True:
            self.play_human()
            if len(self._black_pieces) < 4:
                print("You won.")
                exit()
            self.play_computer()
            if len(self._white_pieces) < 4:
                print("Computer won.")
                exit()


if __name__ == '__main__':
    bd = Board()
    bd.gameplay()
