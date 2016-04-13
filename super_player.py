#!/usr/bin/env python3

"""

Group 05

Authors : Aref Shabana - Christophe Limbree

Date : 

"""

import random

from quoridor import *

import minimax

import math

class MyAgent(Agent, minimax.Game):

    DEPTH_LIMIT = 2

    RED_PLACES = []

    RED_VALUES = []

    """My Quoridor agent."""

    def __init__(self):

        self.firstTime = 0


		
    def successors(self, state, depth):

        """The successors function must return (or yield) a list of

        pairs (a, s) in which a is the action played to reach the

        state s; s is the new state, i.e. a pair (b, p) where

        b is the new board after the action a has been played and

        p is the player to play the next move.

        """

        board, player = state

        legal_p_moves =  board.get_legal_pawn_moves(player) # A list of action

        other_player = (player + 1) % 2

        legal_p_moves =  board.get_legal_wall_moves_colsely_filtered(player) + legal_p_moves

        if depth == 0:

                self.DEPTH_LIMIT = 1 + 5/len(legal_p_moves)

                self.detect_red_places(board , player, False, 164)

                self.detect_suspected_red_places(board, player, True)        

        for action in legal_p_moves:

            modified_board = board.clone()

            modified_board.play_action(action, player)

            new_state = (modified_board, other_player)

            yield (action, new_state)



    def cutoff(self, state, depth):

        """The cutoff function returns true if the alpha-beta/minimax

        search has to stop; false otherwise.

        """

        board, player = state

        if board.is_finished():

            return True

        if depth > self.DEPTH_LIMIT:

            return True

        return False





    def evaluate(self, state):

        """The evaluate function must return an integer value

        representing the utility function of the board.

        """

        board, player = state

        root_player = self.player # I am not sure

        otherPlayer = (root_player+1)%2

        (y0, x0) = board.pawns[root_player]

        (y1, x1) = board.pawns[otherPlayer]

        d0 = abs(board.goals[root_player] - x0)

        d1 = abs(board.goals[otherPlayer] - x1)

        nbOfHWallsInFront = 0

        nbOfVWallsInFront = 0

        WEIGHT_H_WALLS = 5

        WEIGHT_V_WALLS = 1

        WEIGHT_PROXIMITY = 10

        WEIGHT_STRAIGHT_LINE = 100        

        WEIGHT_RED_PLACE = 100
        
        CONTINUOUS_WALL_WEIGHT = 5

        straight_line_to_goal = 1

        opponent_straight_line_to_goal = 1

        nearest_hor_wall_distance = 10

        opponent_nearest_hor_wall_distance = 10
        
        distToContinuousWall = 10

        distToContinuousWallOp = 10

        for wall in board.horiz_walls:

            (y, x) = wall

            if ((board.goals[root_player] == 8 and y0 <= y) or (board.goals[root_player] == 0 and y0 > y)) and (x == x0 or (x+1) == x0): # In front of me in the same column

                nbOfHWallsInFront -= 1

                straight_line_to_goal = 0

                if math.fabs(y - y0) < nearest_hor_wall_distance:

                    nearest_hor_wall_distance = math.fabs(y-y0)

                (wCL, wCR) =  self.continuousWallInFront(state, x0, y)

                if wCL or wCR:

                    distToContinuousWall = min(distToContinuousWall, math.fabs(y-y0))

            if ((board.goals[otherPlayer] == 8 and y1 <= y) or (board.goals[otherPlayer] == 0 and y1 > y)) and (x == x1 or (x+1) == x1):

                nbOfHWallsInFront += 1 # Must be positive in case it's in front of my opponent

                opponent_straight_line_to_goal = 0

                if math.fabs(y - y0) < opponent_nearest_hor_wall_distance:

                    opponent_nearest_hor_wall_distance = math.fabs(y-y1)
                    
                (wCL, wCR) =  self.continuousWallInFront(state, x1, y)

                if wCL or wCR:
                
                    distToContinuousWallOp = min(distToContinuousWallOp, math.fabs(y-y1))

        for wall in board.verti_walls:

            (y, x) = wall

            if ((board.goals[root_player] == 8 and y0 <= y) or (board.goals[root_player] == 0 and y0 > y)) and (x == x0 or (x0-1) == x) : # In front of me in the same column

                nbOfVWallsInFront -= 1

            if ((board.goals[otherPlayer] == 8 and y1 <= y) or (board.goals[otherPlayer] == 0 and y1 > y)) and (x == x1 or (x1-1) == x):

                nbOfVWallsInFront += 1

        nbOfHWallsInFront *= WEIGHT_H_WALLS

        nbOfVWallsInFront *= WEIGHT_V_WALLS
    
        #calculate difference in proximity to goal (straigh line)

        proximity_to_goal = WEIGHT_PROXIMITY * (math.fabs(board.goals[otherPlayer] - board.pawns[otherPlayer][0]) - math.fabs(board.goals[root_player] - board.pawns[root_player][0]))

        #calculate open straight line to goal

        straight = WEIGHT_STRAIGHT_LINE * (opponent_straight_line_to_goal - straight_line_to_goal)

        nearest_hor_wall_distance = WEIGHT_H_WALLS * (10 - nearest_hor_wall_distance)

        opponent_nearest_hor_wall_distance = WEIGHT_H_WALLS * (10 - opponent_nearest_hor_wall_distance)

        opponent_nearest_hor_wall_distance -= nearest_hor_wall_distance

        red_value = WEIGHT_RED_PLACE * ( self.is_red(board.pawns[otherPlayer]) - self.is_red(board.pawns[root_player]))
        
        continuous_wall_effect = CONTINUOUS_WALL_WEIGHT * (20 + distToContinuousWallOp - distToContinuousWall)
        
        return ( nbOfVWallsInFront + proximity_to_goal + straight + opponent_nearest_hor_wall_distance + red_value + continuous_wall_effect)


  
    def continuousWallInFront(self, state, xPosi, yPosi):

        board, player = state

        nbWallsLeftOnTheRow = 0

        wallsAreClosedToTheRight = False

        wallsAreClosedToTheLeft = False

        nbWalls = 0

        for w in range(0, max(0, xPosi-2), 2):

            nbWalls += 1
            
            if (yPosi, w) in board.horiz_walls:

                nbWallsLeftOnTheRow += 1

        if nbWallsLeftOnTheRow == nbWalls:

            wallsAreClosedToTheLeft = True

        nbWallsRightOnTheRow = 0

        nbWalls = 0

        for w in range(min(xPosi+2, 7),7, 2):

            nbWalls += 1

            if (yPosi, w) in board.horiz_walls:

                nbWallsRightOnTheRow += 1

        if nbWallsRightOnTheRow == nbWalls:

            wallsAreCloseToTheRigth = True

        return (wallsAreClosedToTheLeft, wallsAreClosedToTheRight)
  
  
  
    
    RED_CHECKED_POSITIONS = []
    

    def detect_red_places(self, board, player, in_way, value):

        if not in_way:
            self.RED_CHECKED_POSITIONS = []
        if [board.pawns[player][0], board.pawns[player][1]] in self.RED_CHECKED_POSITIONS:
            return
        self.RED_CHECKED_POSITIONS.append([board.pawns[player][0], board.pawns[player][1]])

        p_moves = board.get_legal_pawn_moves(player)

        if(len(p_moves) == 1):
            value = 164
        
        if(len(p_moves) == 2):
            value = value -1

        if(len(p_moves) == 1 or (len(p_moves) == 2 and in_way)):

            if(board.pawns[player] != board.pawns[(player+1)%2]):

                if(board.pawns[player] not in self.RED_PLACES):

                    self.RED_PLACES.append(board.pawns[player])

                    self.RED_VALUES.append(value)

                else:

                    self.RED_VALUES[self.RED_PLACES.index([board.pawns[player][0], board.pawns[player][1]])] = value

                for i in p_moves:

                    cloned = board.clone()                        

                    cloned.pawns[player] = [i[1], i[2]]
                    self.detect_red_places(cloned, player, True, value - 1)

					
					
    SUSPECTED_CHECKED_POSITIONS = []
    

	
    def detect_suspected_red_places(self, board, player, isRoot):

        if(isRoot):
                self.SUSPECTED_CHECKED_POSITIONS = []
        
        if [board.pawns[player][0], board.pawns[player][1]] in self.SUSPECTED_CHECKED_POSITIONS:
                return
        self.SUSPECTED_CHECKED_POSITIONS.append([board.pawns[player][0], board.pawns[player][1]])

        p_moves = board.get_legal_pawn_moves(player)

        if(len(p_moves) == 1):

            self.detect_red_places( board, player, False, 164)

        if(len(p_moves) == 2):
                for i in p_moves:
                       cloned = board.clone()
                       cloned.pawns[player] = [i[1], i[2]] 

                       self.detect_suspected_red_places(cloned, player, False)

    

    def is_red(self, place):

        place = [place[0], place[1]]

        if place in self.RED_PLACES:

            return self.RED_VALUES[self.RED_PLACES.index(place)]

        return 0

        

        

    def play(self, percepts, player, step, time_left):

        """This function is used to play a move according

        to the percepts, player and time left provided as input.

        It must return an action representing the move the player

        will perform.

        """

        self.player = player

        state = (dict_to_board(percepts), player)

        return minimax.search(state, self)

		
		
if __name__ == "__main__":

    agent_main(MyAgent())
