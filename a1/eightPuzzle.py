#Look for #IMPLEMENT tags in this file. These tags indicate changes in the 
#file to implement the required routines. 


'''8-Puzzle STATESPACE 
'''
from search import *

class eightPuzzle(StateSpace):
    StateSpace.n = 0
    
    def __init__(self, action, gval, state, parent = None):
        '''Create an 8-puzzle state object.
        The parameter state represents the puzzle configation as a list of 9 numbers in the range [0-8] 
        The 9 numbers specify the position of the tiles in the puzzle from the
        top left corner, row by row, to the bottom right corner. E.g.:

        [2, 4, 5, 0, 6, 7, 8, 1, 3] represents the puzzle configuration

        |-----------|
        | 2 | 4 | 5 |
        |-----------|
        |   | 6 | 7 |
        |-----------|
        | 8 | 1 | 3 |
        |-----------|
        '''
        #Note we represent the puzzle configuration in the state member.
        #the list of tile positions.
        StateSpace.__init__(self, action, gval, parent)
        self.state = state

    def successors(self) :
#IMPLEMENT
        '''Implement the actions of the 8-puzzle search space.'''
        #   IMPORTANT. The list of successor states returned must be in the ORDER
        #   Move blank down move, move blank up, move blank right, move blank left
        #   (with some successors perhaps missing if they are not available
        #   moves from the current state, but the remaining ones in this  
        #   order!)
        
        States = list()
        i = self.state.index(0)
        if i < 6: # can move down
            new_state = self.state[:]
            new_state[i], new_state[i+3] = new_state[i+3], new_state[i]
            States.append(eightPuzzle("Blank-Down", self.gval+1, new_state, self))
        if i > 2: # can move up
            new_state = self.state[:]
            new_state[i], new_state[i-3] = new_state[i-3], new_state[i]
            States.append(eightPuzzle("Blank-Up", self.gval+1, new_state, self))
        if i % 3 < 2: # can move right
            new_state = self.state[:]
            new_state[i], new_state[i+1] = new_state[i+1], new_state[i]
            States.append(eightPuzzle("Blank-Right", self.gval+1, new_state, self))
        if i % 3 > 0: # can move left
            new_state = self.state[:]
            new_state[i], new_state[i-1] = new_state[i-1], new_state[i]
            States.append(eightPuzzle("Blank-Left", self.gval+1, new_state, self))
        return States

    def hashable_state(self) :
#IMPLEMENT
        return tuple(self.state)

    def print_state(self):
#DO NOT CHANGE THIS METHOD
        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))


        print("|-----------|")
        print("| {} | {} | {} |".format(self.state[0],self.state[1],self.state[2]))
        print("|-----------|")
        print("| {} | {} | {} |".format(self.state[3],self.state[4],self.state[5]))
        print("|-----------|")
        print("| {} | {} | {} |".format(self.state[6],self.state[7],self.state[8]))
        print("|-----------|")

#Set up the goal.
#We allow any full configuration of the puzzle to be a goal state. 
#We use the class variable "eightPuzzle.goal_state" to store the goal configuration. 
#The goal test function compares a state's configuration with the goal configuration

eightPuzzle.goal_state = False

def eightPuzzle_set_goal(state):
    '''set the goal state to be state. Here state is a list of 9
       numbers in the same format as eightPuzzle.___init___'''
    eightPuzzle.goal_state = state

def eightPuzzle_goal_fn(state):
    return (eightPuzzle.goal_state == state.state)

def heur_zero(state):
    '''Zero Heuristic use to make A* search perform uniform cost search'''
    return 0

def h_misplacedTiles(state):
#IMPLEMENT
    #return the number of tiles (NOT INCLUDING THE BLANK) in state that are not in their goal position. (will need to access the class variable eigthPuzzle.goal_stategroping)

    return sum([state.state.index(i) != eightPuzzle.goal_state.index(i)
                for i in range(1, 9)])
    
def h_MHDist(state):
    #return the sum of the manhattan distances each tile (NOT INCLUDING
    #THE BLANK) is from its goal configuration. 
    #The manhattan distance of a tile that is currently in row i column j
    #and that has to be in row x column y in the goal is defined to be
    #  abs(i - x) + abs(j - y)

    def mhdist(a, b):
        '''Manhattan distance of two positions in puzzle'''
        ax, ay = a % 3, a // 3
        bx, by = b % 3, b // 3
        return abs(ax - bx) + abs(ay - by)
        
    return sum([mhdist(state.state.index(i), eightPuzzle.goal_state.index(i))
                for i in range(1, 9)])
