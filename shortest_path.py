#Julien De Coster - Sebastien Villar

import search
import copy
import time
import os
import signal
import sys


cache = {}
######################  Implement the search #######################
class ShortestPath(search.Problem):

	def __init__(self, board, player, goal):
		self.initial = State(board, player)
		self.goal = goal

	def goal_test(self, state):
		board = state.board
		player = state.player
		return board.pawns[player][0] == self.goal

	def successor(self, state):
		board = state.board
		player = state.player
		for move in board.get_simplified_legal_pawn_moves(player):
			new_board = board.clone()
			new_board.simplified_play_action(move, player)
			yield move, State(new_board, player)

	def run(self):
		global cache

		board = self.initial.board
		player = self.initial.player
		board_rep = str(board.pawns[player]) + str(board.horiz_walls) + str(board.verti_walls) + str(player)
		if board_rep in cache:
			return cache[board_rep]

		if len(cache) >= 10000:
			cache = {}
		node = search.astar_graph_search(self, h)
		if node == None:
			return -1

		length = 0
		while node.parent:
			node = node.parent
			length += 1
			cache[board_rep] = length
		return length

def h(node):
	board = node.state.board
	player = node.state.player
	return abs(board.pawns[player][0] - board.goals[player])

class State():
	def __init__(self, board, player):
		self.board = board
		self.player = player

	def __repr__(self):
		return repr(self.board) + str(self.player)

	def __eq__(self, state2):
		return repr(self) == repr(state2)

	def __hash__(self):
		return hash(repr(self))


