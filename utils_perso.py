from time import time
from Timer import Timer
from aima.utils import PriorityQueue

class NoPath(Exception):
    """Raised when a player puts a wall such that no path exists
    between a player and its goal row"""
    def __repr__(self):
        return "Exception: no path to reach the goal"

class Node:
    def __init__(self, pos, path_cost):
        self.pos=pos
        self.path_cost=path_cost
            
class Utils(object):
    # To record time
    n_successors = 0
    total_time = Timer()
    total_time_minimax = Timer()
    total_time_successors = Timer()
    total_time_evaluation = Timer()
    @staticmethod
    def print_time_results():
        print("Total time : ", Utils.total_time.elapsed)
        print("    Minimax time : ", Utils.total_time_minimax.elapsed)
        print("        Successors time : ", Utils.total_time_successors.elapsed)
        print("        Evaluation time : ", Utils.total_time_evaluation.elapsed)
        print("        Remaining :       ", Utils.total_time_minimax.elapsed-Utils.total_time_successors.elapsed-Utils.total_time_evaluation.elapsed)
        print("Remaining :  ", Utils.total_time.elapsed-Utils.total_time_minimax.elapsed)
    
    
    
    
    # Method to find shortest path
    @staticmethod
    def a_star_search_optimized(board, player):        
        def f(node):
            return node.path_cost + abs(node.pos[0]-GOAL)

        # Ugly optimization, we hope we access local variables faster
        GOAL = board.goals[player]
        INDEXMAX = board.size-1
        (a, b) = board.pawns[player]
        
        if a == GOAL: return 0
        
        visited = [[False for i in range(board.size)] for i in range(board.size)] # Visited states matrix

        neighbors = PriorityQueue(f,min);
        neighbors.append(Node(board.pawns[player], 0))
        
        
        while len(neighbors) > 0:
            neighbor = neighbors.pop()
            (x, y) = neighbor.pos
            visited[x][y] = True
            if x == GOAL: # Solution found !
                return neighbor.path_cost
            
            for n_ in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                (x_, y_) = n_
                if 0 <= x_ <= INDEXMAX and 0 <= y_ <= INDEXMAX and not visited[x_][y_] and not n_ in neighbors.A and board.is_pawn_move_ok_bis_simplified(neighbor.pos, n_) :
                    neighbors.append(Node(n_, neighbor.path_cost+1))
        
        raise NoPath()
    
    @staticmethod
    def a_star_search_optimized_path(board, player):
        return Utils.a_star_search_optimized_path_position(board, board.pawns[player], board.goals[player]);
        
    @staticmethod
    def a_star_search_optimized_path_position(board, pawn, goal):        
        def f(node):
            return node.path_cost + abs(node.pos[0]-GOAL)

        # Ugly optimization, we hope we access local variables faster
        GOAL = goal
        INDEXMAX = board.size-1
        (a, b) = pawn

        if a == GOAL: return []
        
        visited = [[False for i in range(board.size)] for i in range(board.size)] # Visited states matrix
        prede = [[None for i in range(board.size)] for i in range(board.size)] # Predecessor matrix

        neighbors = PriorityQueue(f,min);
        neighbors.append(Node(pawn, 0))
        
        
        while len(neighbors) > 0:
            neighbor = neighbors.pop()
            (x, y) = neighbor.pos
            visited[x][y] = True
            if x == GOAL: # Solution found !
                succ = [neighbor.pos]
                curr = prede[x][y]
                while curr is not None and curr != pawn:
                    succ.append(curr.pos)
                    (x_, y_) = curr.pos
                    curr = prede[x_][y_]
                succ.reverse()
                return succ
            
            for n_ in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                (x_, y_) = n_
                if 0 <= x_ <= INDEXMAX and 0 <= y_ <= INDEXMAX and not visited[x_][y_] and not n_ in neighbors.A and board.is_simplified_pawn_move_ok(neighbor.pos, n_) :#board.is_pawn_move_ok_bis_simplified(neighbor.pos, n_, board.pawns[1-player]) :
                    neighbors.append(Node(n_, neighbor.path_cost+1))
                    prede[x_][y_] = neighbor

        print(board.__str__())
        raise NoPath()