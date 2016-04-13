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
        for m in moves:
            if(board.is_action_valid(m, player)):
                newB = board.clone()
                newB.play_action(m, player)
                newS = (newB , 1-player)
                yield(m,newS)

    def cutoff(self, state, depth):
        """The cutoff function returns true if the alpha-beta/minimax
        search has to stop; false otherwise.
        """
        board, player = state
        if(board.is_finished()):
            return True
        else:
            if(depth >= 1):
                return True
            else:
                return False

    def evaluate(self, state):
        """The evaluate function must return an integer value
        representing the utility function of the board.
        """
        board, player = state
#Score regarding the minimum number of steps to win
        score = board.min_steps_before_victory(player)
#Score regarding the number of walls behind player
        scoreWallsBack = 0
        for wall in board.horiz_walls:
#Add 1 for each wall behind player
            if(board.goals[player] == 0):
                if(wall[0] > board.pawns[player][0]):
                    scoreWallsBack = scoreWallsBack + 1
            else:
                if(wall[0] < board.pawns[player][0]):
                    scoreWallsBack = scoreWallsBack + 1
        totplayer1 = 3*score + 2*scoreWallsBack
#changing player
        player = 1-player
#Score regarding the minimum number of steps to win
        score = board.min_steps_before_victory(player)
#Score regarding the number of walls behind player
        scoreWallsBack = 0
        for wall in board.horiz_walls:
#Add 1 for each wall behind player
            if(board.goals[player] == 0):
                if(wall[0] > board.pawns[player][0]):
                    scoreWallsBack = scoreWallsBack + 1
            else:
                if(wall[0] < board.pawns[player][0]):
                    scoreWallsBack = scoreWallsBack + 1
        totplayer2 = 3*score + scoreWallsBack

        player = 1-player
#Final score
        return totplayer1 - totplayer2
        '''
#Score regarding the minimum number of steps to win
        score = board.min_steps_before_victory(player) - board.min_steps_before_victory(1-player)

#Score regarding the number of wall still available
        scoreWalls =  board.nb_walls[player] - board.nb_walls[1-player]

#Score regarding the number of walls behind player
        scoreWallsBack = 0
        for wall in board.horiz_walls:
#Add 1 for each wall behind player
            if(board.goals[player] == 0):
                if(wall[0] > board.pawns[player][0]):
                    scoreWallsBack = scoreWallsBack + 1
            else:
                if(wall[0] < board.pawns[player][0]):
                    scoreWallsBack = scoreWallsBack + 1
#Withdraw 1 for each wall behind player (1-p)
            if(board.goals[1-player] == 0):
                if(wall[0] > board.pawns[1-player][0]):
                    scoreWallsBack = scoreWallsBack - 1
            else:
                if(wall[0] < board.pawns[1-player][0]):
                    scoreWallsBack = scoreWallsBack - 1

#Final score
        return 3*score + scoreWalls + 2*scoreWallsBack
        '''


    def play(self, percepts, player, step, time_left):
        """This function is used to play a move according
        to the percepts, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        """
        self.player = player
        state = (dict_to_board(percepts), player)
        return minimax.search(state, self)

    def makeMove(self, state, move):
        board, player = state
        

if __name__ == "__main__":
    agent_main(MyAgent())
