#!/usr/bin/env python3
"""
Quoridor agent.
Copyright (C) 2013, <<<<<<<<<<< YOUR NAMES HERE >>>>>>>>>>>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""



import minimax
from quoridor import *


class MyAgent(Agent, minimax.Game):

    """My Quoridor agent."""

    def successors(self, state):
        """The successors function must return (or yield) a list of
        pairs (a, s) in which a is the action played to reach the
        state s; s is the new state, i.e. a pair (b, p) where
        b is the new board after the action a has been played and
        p is the player to play the next move.
        """
        board, player = state
        legal_moves = board.get_legal_pawn_moves(player=player)
        successors = []
        for move in legal_moves:
            (id_move, row, col) = move
            if id_move == 'P':
                new_board = board.clone()
                new_board.pawns[player] = (row, col)
                new_player = (player + 1) % 2
                successors.append((move, (new_board, new_player)))

        return successors

    def cutoff(self, state, depth):
        """The cutoff function returns true if the alpha-beta/minimax
        search has to stop; false otherwise.
        """
        board, player = state
        if board.is_finished() or depth == 2:
            return True
        return False

    def evaluate(self, state):
        """The evaluate function must return an integer value
        representing the utility function of the board.
        """
        board, player = state
        score = board.get_score(self.player)
        return score

    def play(self, percepts, player, step, time_left):
        """This function is used to play a move according
        to the percepts, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        """
        self.player = player
        state = (dict_to_board(percepts), player)
        result = minimax.search(state, self)
        return result


if __name__ == "__main__":
    agent_main(MyAgent())