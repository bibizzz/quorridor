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

import random

from quoridor import *
import minimax


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
        moves = board.get_actions(player)
        for move in moves :
            newBoard = board.clone()
            newBoard = newBoard.play_action(move, player)
            yield (move, (newBoard, (player + 1) % 2))
        raise StopIteration

    def cutoff(self, state, depth):
        """The cutoff function returns true if the alpha-beta/minimax
        search has to stop; false otherwise.
        """
        board, player = state
        return depth >= 2 or board.is_finished()

    def evaluate(self, state):
        """The evaluate function must return an integer value
        representing the utility function of the board.
        """
        board, player = state

        minStepsMe = board.min_steps_before_victory(self.player)
        minStepsHim = board.min_steps_before_victory((self.player + 1) % 2)

        diffMinSteps = minStepsHim - minStepsMe

        maxPath = 30

        score = 1*diffMinSteps/maxPath

        score += 0.1 * ((board.nb_walls[self.player]/10) - (board.nb_walls[(self.player+1)%2]/10))

        if board.nb_walls[self.player] == 0 and minStepsMe < minStepsHim:
            score -= 1
        if board.nb_walls[(self.player+1)%2] == 0 and minStepsMe > minStepsHim:
            score += 1

        if board.is_finished() :
            if player == self.player : score -= 9000
            else : score += 9000

        return (int) (score * 10000)

    def play(self, percepts, player, step, time_left):
        """This function is used to play a move according
        to the percepts, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        """
        self.player = player
        board = dict_to_board(percepts)
        state = (board, player)
        if step < 7 and board.nb_walls[0]+board.nb_walls[1] == 20 :
            (x, y) = board.get_shortest_path(self.player)[0]
            return ('P', x, y)
        else :
            return minimax.search(state, self)


if __name__ == "__main__":
    agent_main(MyAgent())
