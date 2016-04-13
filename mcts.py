# This is a very simple implementation of the UCT Monte Carlo Tree Search algorithm in Python 2.7.
# The function UCT(rootstate, itermax, verbose = False) is towards the bottom of the code.
# It aims to have the clearest and simplest possible code, and for the sake of clarity, the code
# is orders of magnitude less efficient than it could be made, particularly by using a
# state.GetRandomMove() or state.DoRandomRollout() function.
#
# Example GameState classes for Nim, OXO and Othello are included to give some idea of how you
# can write your own GameState use UCT in your 2-player game. Change the game to be played in
# the UCTPlayGame() function at the bottom of the code.
#
# Written by Peter Cowling, Ed Powley, Daniel Whitehouse (University of York, UK) September 2012.
#
# Licence is granted to freely use and distribute for any sensible/legal purpose so long as this comment
# remains in any distributed code.
#
# For more information about Monte Carlo Tree Search check out our web site at www.mcts.ai

from math import *
import random
from quoridor import *

class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self, move = None, parent = None, state = None):
        self.board, self.player = state
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = self.board.get_actions(self.player) # future child nodes
        self.playerJustMoved = self.player # the only part of the state that the Node needs later


    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s

    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s


def UCT(rootstate, itermax, verbose = False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""


    def get_moves(state):
        moves = []
        board, player = state
        # TODO
        for move in board.get_legal_pawn_moves(player):
            moves.append ( (move, (board.clone().play_action(move, player), (player + 1) % 2)) )

        opponent_position = board.pawns[(player + 1) % 2]
        wall_adjacent_consider_level = 2

        if wall_adjacent_consider_level == 1:
            for move in board.get_legal_wall_moves(player):
                import math
                if math.fabs(opponent_position[0] - move[1]) < 2 and math.fabs(opponent_position[1] - move[2]) < 2:
                    if move[1] - opponent_position[0] < 1 and move[2] - opponent_position[1] < 1:

                        moves.append ( move )
        else:
            for move in board.get_legal_wall_moves(player):
                import math
                if math.fabs(opponent_position[0] - move[1]) < 3 and math.fabs(opponent_position[1] - move[2]) < 3:
                    if move[1] - opponent_position[0] < 2 and move[2] - opponent_position[1] < 2:

                        moves.append ( move )
        return moves

    rootnode = Node(state = rootstate)

    for i in range(itermax):
        import copy
        node = rootnode
        state = copy.deepcopy(rootstate)
        board, player = state

        print("Iteration: ", i)

        # Select
        while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
            print("1. Select")
            node = node.UCTSelectChild()
            board.play_action(node.move, player)

        # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
            print("2. Expand")
            m = random.choice(node.untriedMoves)
            node = node.AddChild(m, (board.clone().play_action(m, player), (player + 1 ) % 2)) # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        counter = 0
        while node.untriedMoves != []: # while state is non-terminal
            print("3. Rollout - Iteration: ", counter)
            board.play_action(random.choice(board.get_actions(player)), player)
            counter += 1

        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            print("4. Backpropagate")
            if (board.is_playerwin(player)):
                node.Update(1)
            else:
                node.Update(0)
            node = node.parentNode

    # Output some information about the tree - can be omitted
    #if (verbose): print rootnode.TreeToString(0)
    #else: print rootnode.ChildrenToString()

    return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited

def search(state):
    board, player = state
    print("START UCT!")
    move = UCT(state, 1, verbose=False)
    print("NEXT MOVE IS:")
    print(move)
    return move