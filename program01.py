#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Othello, or Reversi (https://en.wikipedia.org/wiki/Reversi), is a board game
played by two players, playing "disks" of different colors an 8x8 board.
Despite having relatively simple rules, Othello is a game of high strategic depth.
In this homework you will need to simulate a simplified version of othello,
called Dumbothello, in which each player can capture the opponent's disks
by playing a new disk on an adjacent empty cell.
The rules of Dumbothello are:
- each player has an associated color: white, black;
- the player with black is always the first to play;
- in turn, each player must place a disk of their color in such a way
  to capture one or more opponent's disks;
- capturing one or more opponent's disks means that the disk played by the
  player changes into the player's color all the directly adjacent opponent's disks,
  in any horizontal, vertical or diagonal direction;
- after playing one's own disk, the captured opponent's disks change
  their color, and become the same color as the player who just played;
- if the player who has the turn cannot add any disk on the board,
  the game ends. The player who has the higher number of disks on the board wins
  or a tie occurs if the number of disks of the two players is equal;
- the player who has the turn cannot add any disk if there is
  no way to capture any opponent's disks with any move, or if there are no
  more free cells on the board.
Write a function dumbothello(filename) that reads the configuration of the
board from the text file indicated by the string "filename" and,
following the rules of Dumbothello, recursively generates the complete game tree
of the possible evolutions of the game, such that each leaf of the tree
is a configuration from which no more moves can be made.

The initial configuration of the chessboard in the file is stored line by
line in the file: letter "B" identifies a black disk, a "W" a white disk,
and the character "." an empty cell. The letters are separated by one or
more spacing characters.

The dumbothello function will return a triple (a, b, c), where:
- a is the total number of evolutions ending in a black victory;
- b is the total number of evolutions ending in a white victory;
- c is the total number of evolutions ending in a tie.

For example, given as input a text file containing the board:
. . W W
. . B B
W W B B
W B B W

The function will return the triple:
(2, 16, 0)

NOTICE: the dumbotello function or some other function used by it must be recursive.

'''

def dumbothello(filename: str) -> tuple[int, int, int]:
    # read the board into a list of list
    with open(filename) as file:
        board = [board_row.strip().split(" ") for board_row in file.readlines()]
        b = Othello(board)
        return b.evaluate_game('W')


class Othello:

    # constructer for getting the board
    def __init__(self, board):
        self.board = board
        self.index = [(r, c) for r in range(len(self.board)) for c in range(len(self.board[r]))]

    # fun that returns a list of empty cells
    def empty_cells(self, player):
        cells = [(r, c) for r in range(len(self.board))
                 for c in range(len(self.board[r]))
                 if self.board[r][c] == '.'
                 ]
        possible_moves = []
        for x, y in cells:
            neighbors = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1),
                         (x + 1, y - 1),
                         (x + 1, y), (x + 1, y + 1)]
            for neighbor in neighbors:
                if neighbor in self.index:
                    if self.board[neighbor[0]][neighbor[1]] != player and self.board[neighbor[0]][neighbor[1]] != ".":
                        possible_moves.append((x,y))
                        break

        return possible_moves

    # the next player
    def next_player(self, player):
        if player == 'W':
            return 'B'
        return 'W'
    
    #determine the conditions that a winner exist
    def winner(self, player):
        
        
        cells = self.empty_cells(player)
        if not cells:
            return self.has_won()

        for n, m in self.empty_cells(player):
            neighbors_nm = [(n - 1, m - 1), (n - 1, m), (n - 1, m + 1), (n, m - 1), (n, m + 1),
                        (n + 1, m - 1), (n + 1, m), (n + 1, m + 1)]
            new_neighbors_nm = [(n, m) for n, m in neighbors_nm if n >= 0 and m >= 0]

            if new_neighbors_nm.count(player) == len(neighbors_nm):
                return self.has_won()
        return None

    #determine who is the winner
    def has_won(self):
        countb = 0
        countw = 0
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 'B':
                    countb += 1
                elif self.board[row][col] == 'W':
                    countw += 1
        if countw > countb:
            return 'W'
        elif countb > countw:
            return 'B'
        else:
            return 'E'


    def evaluate_game(self, player):
        '''returns a tuple (a, b, c), a is all the ways that black can win, b is all the ways that white
        can win and c is all the ways that no one wins.'''

        player = self.next_player(player)
        win = {"B": (1, 0, 0), "W": (0, 1, 0), "E" : (0,0,1)}
        w = self.winner(player)
        if w:
            return win[w]

        moves = self.empty_cells(player)
        A = B = C = 0

        for r, c in moves:

            new_board = [row.copy() for row in self.board]
            new_board[r][c] = player
            neighbors = [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1), (r, c - 1), (r, c + 1),
                         (r + 1, c - 1),
                         (r + 1, c), (r + 1, c + 1)]

            for expand in neighbors:
                if expand in self.index and self.board[expand[0]][expand[1]] != player and self.board[expand[0]][
                    expand[1]] != '.':
                    new_board[expand[0]][expand[1]] = player

            child = Othello(new_board)
            a, b, t = child.evaluate_game(player)
            A += a
            B += b
            C += t

        return A, B, C
