# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
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
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

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


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # Route to reach the goal state
    route = []

    # Initialize the search-tree with the root-node
    currentNode = problem.getStartState()
    stateType = type(currentNode)
    searchTree = []
    searchTree.append({'node': currentNode, 'childs': [], 'parent': None})

    # Initialize the opened-list with root-node
    openedList = util.Stack()
    openedList.push(currentNode)

    # Iterating
    while 1:
        # If the open list is empty error 
        if openedList.isEmpty():
            return None

        # Getting the node from the stack to expand it and adding it to the search tree
        currentNode = openedList.pop()

        # Looking for the parent of the current node
        parent = None
        for node in searchTree:
            if parent != None:
                break
            for child in node['childs']:
                if child[0] == currentNode[0]:
                    # Adding just tupples
                    parent = node['node'][0] if stateType == type(node['node'][0]) else node['node']
                    break

        # Checking if the node is in the tree
        if (stateType == type(currentNode) or stateType == type(currentNode[0])) and not any(node['node'] == currentNode for node in searchTree):
            searchTree.append({'node': currentNode, 'childs': [], 'parent': None})
            searchTree[-1]['parent'] = parent

        # Checking if this is the goal
        if problem.isGoalState(currentNode[0]):
            # Creating the route, we start from the end and we check the father of every node
            parent = searchTree[-1]['parent']
            route.append(searchTree[-1]['node'][1])

            # looking for the parent
            while parent != None:
                # We traverse the node in reverse order, from the end to the beginning
                for node in searchTree[::-1]:
                    state = node['node'][0] if type(node['node'][0]) else node['node']
                    if state == parent and node['parent'] != None:
                        parent = node['parent']
                        route.append(node['node'][1])
                    elif problem.getStartState() == parent:
                        return route[::-1]
        else:
            # Iterating through the successors and adding them. Excluding the nodes that have been visited
            # Checking if the element is a tuple to avoid exceptions
            position = currentNode[0] if stateType == type(currentNode[0]) else currentNode
            for child in problem.getSuccessors(position):
                # Checking if the childs are already in the tree
                if not any(node['node'][0] == child[0] for node in searchTree):
                    openedList.push(child)
                    searchTree[-1]['childs'].append(child)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    # Route to reach the goal state
    route = []

    # Initialize the search-tree with the root-node
    currentNode = problem.getStartState()
    stateType = type(currentNode)
    searchTree = []
    searchTree.append({'node': currentNode, 'childs': [], 'parent': None})

    # Initialize the opened-list with root-node
    openedList = util.Queue()
    openedList.push(currentNode)

    # Iterating
    while 1:
        # If the open list is empty error
        if openedList.isEmpty():
            return None

        # Getting the node from the queue
        # to expand it and adding it to the search tree
        currentNode = openedList.pop()

        # Looking for the parent of the current node
        parent = None
        for node in searchTree:
            if parent != None:
                break
            for child in node['childs']:
                if child[0] == currentNode[0]:
                    # Adding just tupples
                    parent = node['node'][0] if stateType == type(node['node'][0]) else node['node']
                    break

        # Checking if the node is in the tree
        if (stateType == type(currentNode) or stateType == type(currentNode[0])) and not any(node['node'] == currentNode for node in searchTree):
            searchTree.append({'node': currentNode, 'childs': [], 'parent': None})
            searchTree[-1]['parent'] = parent

        # Checking if this is the goal
        if problem.isGoalState(currentNode[0]):
            # Creating the route, we start from the end and we check the father of every node
            parent = searchTree[-1]['parent']
            route.append(searchTree[-1]['node'][1])

            # looking for the parent
            while parent != None:
                # We traverse the node in reverse order, from the end to the beginning
                for node in searchTree[::-1]:
                    state = node['node'][0] if type(node['node'][0]) else node['node']
                    if state == parent and node['parent'] != None:
                        parent = node['parent']
                        route.append(node['node'][1])
                    elif problem.getStartState() == parent:
                        return route[::-1]
        else:
            # Iterating through the successors and adding them. Excluding the nodes that have been visited
            # Checking if the element is a tuple to avoid exceptions
            position = currentNode[0] if stateType == type(currentNode[0]) else currentNode
            for child in problem.getSuccessors(position):
                # Checking if the childs are already in the tree
                if not any(node['node'][0] == child[0] for node in searchTree):
                    openedList.push(child)
                    searchTree[-1]['childs'].append(child)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # Route to reach the goal state
    route = []

    # Initialize the search-tree with the root-node
    currentNode = problem.getStartState()
    stateType = type(currentNode)
    searchTree = []
    searchTree.append({'node': currentNode, 'childs': [], 'parent': None})

    # Initialize the opened-list with root-node
    openedList = util.PriorityQueue()
    openedList.push(currentNode, 1)

    # Iterating
    while 1:
        # If the open list is empty error
        if openedList.isEmpty():
            return None

        # Getting the node from the queue
        # to expand it and adding it to the search tree
        currentNode = openedList.pop()

        # Looking for the parent of the current node
        parent = None
        for node in searchTree:
            if parent != None:
                break
            for child in node['childs']:
                if child[0] == currentNode[0]:
                    # Adding just tupples
                    parent = node['node'][0] if stateType == type(node['node'][0]) else node['node']
                    break

        # Checking if the node is in the tree
        if (stateType == type(currentNode) or stateType == type(currentNode[0])) and not any(node['node'] == currentNode for node in searchTree):
            searchTree.append({'node': currentNode, 'childs': [], 'parent': None})
            searchTree[-1]['parent'] = parent

        # Checking if this is the goal
        if problem.isGoalState(currentNode[0]):
            # Creating the route, we start from the end and we check the father of every node
            parent = searchTree[-1]['parent']
            route.append(searchTree[-1]['node'][1])

            # looking for the parent
            while parent != None:
                # We traverse the node in reverse order, from the end to the beginning
                for node in searchTree[::-1]:
                    state = node['node'][0] if type(node['node'][0]) else node['node']
                    if state == parent and node['parent'] != None:
                        parent = node['parent']
                        route.append(node['node'][1])
                    elif problem.getStartState() == parent:
                        return route[::-1]

        else:
            # Iterating through the successors and adding them. Excluding the nodes that have been visited
            # Checking if the element is a tuple to avoid exceptions
            position = currentNode[0] if stateType == type(currentNode[0]) else currentNode
            for child in problem.getSuccessors(position):
                # Checking if the childs are already in the tree
                if not any(node['node'][0] == child[0] for node in searchTree):
                    openedList.push(child, child[2])
                    searchTree[-1]['childs'].append(child)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
