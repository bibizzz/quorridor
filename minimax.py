"""
MiniMax and AlphaBeta algorithms.
Author: Cyrille Dejemeppe <cyrille.dejemeppe@uclouvain.be>
Copyright (C) 2013, Université catholique de Louvain

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
import time

class Game:

    """Abstract base class for a game."""

    def successors(self, state):
        """Return the successors of state as (action, state) pairs."""
        abstract

    def cutoff(self, state, depth):
        """Return whether state should be expanded further.

        This function should at least check whether state is a finishing
        state and return True in that case.

        """
        abstract

    def evaluate(self, state):
        """Return the evaluation of state."""
        abstract


inf = float("inf")

#import ETE2  lib for viewing trees


class Search_node:
    def __init__(self, father, action, value, duration=0):
        self.action = action
        self.value = value
        self.duration = duration
        self.father = father
        self.child = []

    def add_child(self, child):
        self.childs.append(child)

    def print_node(self):
        print("a" + str(self.action) + ":" + str(self.value))

    def print_tree(self):
        self.print_node()
        for node in self.child:
            self.print_tree(node)



def nodes(state, game):
    for a, s in game.successors(state):
        yield (a, game.evaluate(s))


def search(state, cut_value, game, prune=True):
    """Perform a MiniMax/AlphaBeta search and return the best action.

    Arguments:
    state -- initial state
    game -- a concrete instance of class Game
    prune -- whether to use AlphaBeta pruning

    """
    print (game.step)
    f = open("search_tree_" + str(game.step) + ".txt", 'w')

    def max_value(state, alpha, beta, depth, node):
        start = time.time()
#        if game.cutoff(state, depth):
#            return game.evaluate(state), None
        val = -inf
        action = None
        pre_val = game.evaluate(state)
        print ("pre " + str(pre_val))
        for a, s in game.successors(state):
            #print (str(a))
            cur_val = game.evaluate(s)
          #print (str(a) + ':' + str(cur_val))
            node_child = Search_node(node, a, cur_val)
            node.addd_child(node_child)
            if cur_val > pre_val + cut_value:
                v, _ = min_value(s, alpha, beta, depth + 1, node_child)
                f.write("a: " + str(a) + "; v: " + str(v) +  "; depth:" + \
                str(depth) + "; alpha:" + str(alpha) +  "; beta:" + str(beta) \
                + " \n")
            else:
                v = cur_val
            if v > val:
                val = v
                action = a
                if prune:
                    if v >= beta:
                        return v, a
                    alpha = max(alpha, v)
        end = time.time()
        print("max t:" + str(end - start))
        return val, action

    def min_value(state, alpha, beta, depth, node):
 #       if game.cutoff(state, depth):
 #           return game.evaluate(state), None
        val = inf
        action = None
        pre_val = game.evaluate(state)
        print ("min pre " + str(pre_val))
        for a, s in game.successors(state):
            cur_val = game.evaluate(s)
            node_child = Search_node(node, a, cur_val)
            node.addd_child(node_child)
            if cur_val < pre_val - cut_value:
                v, _ = max_value(s, alpha, beta, depth + 1, node_child)
             #   f.write("a: " + str(a) + "; v: " + str(v) +  "; depth:" + \
    #  str(depth) + "; alpha:" + str(alpha) +  "; beta:" + str(beta) + " \n")
            else:
                v = cur_val
            if v < val:
                val = v
                action = a
                if prune:
                    if v <= alpha:
                        return v, a
                    beta = min(beta, v)
        return val, action

    root_node = Search_node(None, None, 0)

    _, action = max_value(state, -inf, inf, 0, root_node)
    root_node.print_tree()
    f.close()
    return action
