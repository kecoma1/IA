# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# Attribution Information: The Pacman AI projects were developed at
# UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
import util
from game import Directions


class SearchProblem:
    """
    This class outlines the structure of a search problem,
    but doesn't implement any of the methods
    (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def solveSimpleSearch(problem, openedList):
    """This method solves simple uninformed search algorithms which
        reuse same code. These algorithms are DFS, BFS, UCS and A*
    Args:
        problem: problem to solve
        openedList: name of the data structure of util.py which will be used
    """
    start_state = problem.getStartState()

    # Initialize the opened-list with root-node
    openedList.push([start_state, None, 0, []])

    # Initialize the closed-list as an empty list
    closedList = []

    # Iterating
    while True:
        # If the open list is empty error
        if openedList.isEmpty():
            return None

        # Getting the node from the opened list
        currentNode = openedList.pop()

        # Checking if this is the goal
        if problem.isGoalState(currentNode[0]) == -1:
            closedList.clear()
            while (openedList.isEmpty() != True): openedList.pop()
        if problem.isGoalState(currentNode[0]):
            return currentNode[3]

        # If the node is not in the closed list we add it and
        # we expand it and we add it to the ckised list
        if not any(currentNode[0] == node[0] for node in closedList):
            closedList.append(currentNode)
            # Iterating through the successors and adding them to the open list
            for child in problem.getSuccessors(currentNode[0]):
                child_list = list(child)
                # Adding to the child the route
                child_list.append(currentNode[3].copy())
                child_list[3].append(child[1])
                # Adding to the child the accumulated cost
                child_list[2] += currentNode[2]
                # Adding the node to the closed list
                openedList.push(child_list)


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    return solveSimpleSearch(problem, util.Stack())


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    return solveSimpleSearch(problem, util.Queue())


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # priorityFunction = lambda state: state[2]
    def priorityFunction(state):
        return state[2]
    openlist = util.PriorityQueueWithFunction(priorityFunction)
    return solveSimpleSearch(problem, openlist)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from
    the current state to the nearest goal in the
    provided SearchProblem. This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest
    combined cost and heuristic first."""
    # priorityFunction = lambda state: state[2] + heuristic(state[0], problem)
    def priorityFunction(state):
        return state[2] + heuristic(state[0], problem)
    openlist = util.PriorityQueueWithFunction(priorityFunction)
    return solveSimpleSearch(problem, openlist)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
