#!/usr/bin/env python3
"""
Group 05
Authors : Aref Shabana - Christophe Limbree
"""

import random

from quoridor_LM import *
import minimax
import time


class MyAgent(Agent, minimax.Game):

    """My Quoridor agent."""

    def initialize(self, percepts, players, time_left):

        self.step = 1

    def successors(self, state):
        """The successors function must return (or yield) a list of
        pairs (a, s) in which a is the action played to reach the
        state s; s is the new state, i.e. a pair (b, p) where
        b is the new board after the action a has been played and
        p is the player to play the next move.
        """
        start = time.time()
        board, player = state
        
        legal_p_moves = board.get_actions(player) 
        #legal_p_moves = board.get_legal_pawn_moves(player)  # A list of action
        print( "nb moves: " + str((len(legal_p_moves))))
        other_player = (player + 1) % 2
        for action in legal_p_moves:
            modified_board = board.clone()
            modified_board.play_action(action, player)
            new_state = (modified_board, other_player)
            yield (action, new_state)
        end = time.time()
        print("successor " + str(end - start))

    def cutoff(self, state, depth):
        """The cutoff function returns true if the alpha-beta/minimax
        search has to stop; false otherwise.
        """
        board, player = state
        if board.is_finished():
            return True

        if depth > 0:
            return True
        return False


    def evaluate(self, state):
        """The evaluate function must return an integer value
        representing the utility function of the board.
        """
        board, player = state
        #if board.get_score(self.player) < 0:
            #return -1
        #elif board.get_score(self.player) > 0:
            #return 1
        #else :
            #return 0
        start = time.time()
        if board.is_finished(): # detect the end condition
            return 1000
        ret = board.get_score(self.player)
        end = time.time()
        print("eval" + str(end - start))
        return ret



    def play(self, percepts, player, step, time_left):
        """This function is used to play a move according
        to the percepts, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        """
        self.player = player
        self.step = step
        start = time.time()
        board = dict_to_board(percepts)
        board.get_shortest_path(PLAYER1)
        board.get_shortest_path(PLAYER2)
        state = (board, player)
        end = time.time()
        print("dict: " + str(end - start))
        start = time.time()
        ret = minimax.search(state,  0,  self)
        end = time.time()
        print("minimax: " + str(end - start))
        return ret


if __name__ == "__main__":
    agent_main(MyAgent())
