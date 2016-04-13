from copy import deepcopy
from aima.search import Problem, astar_graph_search
from quoridor import *

class StateAux:
    """
    Instance variables :
    position - coordinates of current position
    dollars - list of coordinates of the dollars
    heuristic_value - We need to keep track of our heuristic_value in order to transform
    our inconsistent heuristic into a consistent one
    """
    width = -1
    height = -1
    destination = -1
    
    def __init__(self, position):
        """Create a state from a string representation if duplicate = False"""
        """Or create a state from variables list_repr, width, height and n_piles"""
        self.position = position
        self.heuristic_value = None;
    
    def apply(self, action):
        """Create a new state by applying the action on this state.
        The action must be a legal action."""
        return StateAux(deepcopy(action))
    
    def __hash__(self):
        return (self.position.__str__()).__hash__()
        
    def __eq__(self, other):
        return self.position == other.position
        
class ShortestPathProblem(Problem):
    """This class defines the mazeCollect Problem in order to be able to use the methods of the framework provided"""
    player = None
    
    def __init__(self,position):
        self.state_init = StateAux(deepcopy(position))
        Problem.__init__(self, self.state_init)
        pass

    
    def goal_test(self, state):
        return state.position[0] == StateAux.destination;
        pass

    def successor(self, state):
            (x, y) = state.position
            positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            for new_pos in positions:
                if AStarAlgorithm.board.is_pawn_move_ok(state.position, new_pos, AStarAlgorithm.board.pawns[1-ShortestPathProblem.player]):
                    yield ("/", StateAux(new_pos))
        
class UtilsAux(object):
    """This class defines the heuristic for the auxiliary problem"""      
    @staticmethod
    def h1(n):
        s = n.state
        return abs(s.position[0]-StateAux.destination)
    
class AStarAlgorithm(object):
    board = None
    @staticmethod
    def shortest_path(player, board):
        AStarAlgorithm.board = board
        ShortestPathProblem.player = player
        StateAux.width = board.rows
        StateAux.height = board.cols
        if player==0:
            StateAux.destination = board.rows-1
        else:
            StateAux.destination = 0
            
        problem=ShortestPathProblem(board.pawns[player])
        node=astar_graph_search(problem, UtilsAux.h1)
        return node.path_cost