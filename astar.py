from search import *
import re
import os
from datetime import datetime
import time
from quoridor import Board


class AstarBoard(Board):
    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self.pawns != other.pawns:
            return False
        return True

    def __hash__(self):
        return hash(self.pawns.__str__())

    def clone(self):
        """Return a clone of this object"""
        clone_board = AstarBoard()
        clone_board.pawns[0] = self.pawns[0]
        clone_board.pawns[1] = self.pawns[1]
        clone_board.goals[0] = self.goals[0]
        clone_board.goals[1] = self.goals[1]
        clone_board.nb_walls[0] = self.nb_walls[0]
        clone_board.nb_walls[1] = self.nb_walls[1]
        for (x, y) in self.horiz_walls:
            clone_board.horiz_walls.append((x, y))
        for (x, y) in self.verti_walls:
            clone_board.verti_walls.append((x, y))
        return clone_board

class Astar(Problem):

    def __init__(self, state):
        board, player = state
        board = board.clone()
        board.__class__ = AstarBoard
        self.initial = (board,player)

    def goal_test(self, state):
        board, player = state

        x, y = board.pawns[player]
        rows = board.goals[player]
        distance = rows - x

        return distance == 0

    def successor(self, state):
        board, player = state

        rows  = board.rows
        size  = board.size
        pawns = board.pawns

        for move in board.get_legal_pawn_moves(player):
            new_board = board.clone()
            new_board.play_action(move, player)
            yield move, (new_board, player)

    def heuristic(self, n):
        state = n.state
        board, player = state

        # Our heuristic computes the shortest straight path:
        x, y = board.pawns[player]
        rows = board.goals[player]
        distance = math.fabs(rows - x)

        # This is in case of a jump over the opponent:
        if distance > 1:
            distance -= 1

        return distance
