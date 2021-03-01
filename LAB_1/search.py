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

class SearchTree:
    """
    Class that defines our own search tree.
    The search tree contains a list of dictionaries, in this dictionary we have:
        - The node. The root is a state, but the rest of the nodes are tuples contaning
        the state, how to get to it and the accumulated cost.
        - His children.
        - His parent. The root has None.
        - The route to get to that node. The route has None.
    The closed list contained in the searchTree. If we only traverse through the 'node' 
    elements of the tree, we are traversing the closed list.
    """
    def __init__(self, root):
        """Constructor of the searchTree class, we receive as an argument the root

        Args:
            root (state): Root node of the tree
        """
        self.tree = [{'node': root, 'childs': [], 'parent': None, 'route': None, 'cost': 0}]


    def add(self, node):
        """Method to add a node in the tree

        Args:
            node (tuple): Node to be added
        """
        if self.isRoot(node):
            return 
        self.tree.append({'node': node, 'childs': [], 'parent': None, 'route': [], 'cost': 0})


    def setParent(self, node):
        """Method to set the parent of a node

        Args:
            node (tuple): Node to have setted the parent
        """
        if self.isRoot(node):
            return
        
        # We get the parent
        parent = self.getParentOf(node)

        # We set in the tree the parent
        ele = self.getTreeNode(node)
        ele['parent'] = parent[0] if not self.isRoot(parent) else parent

        
    def getParentOf(self, node):
        """Method to get the parent of an specific node in a tree

        Args:
            node (tuple): Node which needs to finds his parent
        
        Returns:
            state: Parent
        """
        if self.isRoot(node):
            return None

        for ele in self.tree:        
            for child in ele['childs']:
                if child == node:
                    if self.isRoot(ele['node']):
                        return self.getRoot()
                    else:
                        return ele['node']
                    break
            else:
                # If the inner loop didn't break, continue
                continue
            break
        return None


    def getRoot(self):
        """Method to get the root of the tree

        Returns:
            state: Root
        """
        return self.tree[0]['node']


    def getTreeNode(self, node):
        """Method to get a row in the list of the node

        Args:
            node (tuple): Node

        Returns:
            Row in the list
        """
        if self.isRoot(node):
            return self.tree[0]

        for ele in self.tree:
            if ele['node'][0] == node[0]:
                return ele  
        return None 


    def isInClosedList(self, node):
        """Method to get if a node is in the closed list

        Args:
            node (tuple): Node to check if it is in the closed list
        """
        if self.isRoot(node):
            return True
        return any(ele['node'][0] == node[0] for ele in self.tree) 


    def isInTree(self, node):
        """Method to avoid adding repeated nodes. If a node is already in the whole tree
        we return True

        Args:
            node (tuple): Node to check if it is in the entire tree
        """
        if self.isRoot(node):
            return True

        if self.isInClosedList(node):
            return True

        for ele in self.tree:
            for child in ele['childs']:
                if child[0] == node[0]:
                    return True
        return False


    def addChild(self, node, child):
        """Method to add a child to a node in the tree

        Args:
            node (tuple): Parent
            child (tuple): chikd
        """
        ele = self.getTreeNode(node)
        ele['childs'].append(child)


    def isRoot(self, node):
        """Method to get if a node is the root of the tree

        Args:
            node (tuple): Node to check

        Returns:
            Bool: True if it is, False if not
        """
        if node[0] == self.tree[0]['node'] or node == self.tree[0]['node']:
            return True
        else:
            return False


    def getParentRoute(self, node):
        """Method to get the parent's route

        Args:
            node (tuple): Node to get the parent's route
        """
        if self.isRoot(node):
            return None
        parent = self.getParentOf(node)
        ele = self.getTreeNode(parent)
        return ele['route']

    
    def setRoute(self, node):
        """Method to set the route to a node. The route is from the root
        to the node

        Args:
            node (tuple): Node
        """
        if self.isRoot(node):
            return
        ele = self.getTreeNode(node)
        parent_route = self.getParentRoute(node)
        if parent_route == None: 
            pass
        else:
            ele['route'] = parent_route.copy()
        ele['route'].append(node[1]) # In the tuple, node[1] correspond to the route


    def getNodeRoute(self, node):
        """Method to get the route of a node

        Args:
            node (tuple): Node

        Returns:
            A list with the operators to execute to reach the node
        """
        ele = self.getTreeNode(node)
        return ele['route']

    def getNodeCost(self, node):
        """Method to get the node's cost

        Args:
            node ([tuple): Node

        Returns:
            int: Node's cost
        """
        ele = self.getTreeNode(node)
        return ele['cost']
    
    def setCost(self, node):
        """Method to set the cost in a node

        Args:
            node (tuple): Node
        """
        if self.isRoot(node):
            return
        parent_cost = self.getParentCost(node)  
        ele = self.getTreeNode(node)
        ele['cost'] = parent_cost + node[2]


    def getParentCost(self, node):
        """Method to get the parents cost of a node

        Returns:
            int: Cost of the parent
        """
        if self.isRoot(node):
            return 0
        parent = self.getParentOf(node)
        ele = self.getTreeNode(parent)
        return ele['cost']


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


def solveSimpleSearch(problem, utils, heuristic):
    """This method solves simple uninformed search algorithms which
        reuse same code. These algorithms are DFS, BFS and UCS
        
    Args:
        problem: problem to solve
        utils: name of the data structure of util.py which will be used
    """
    start_state = problem.getStartState()

    # Initialize the search-tree with the root-node
    search_tree = SearchTree(start_state) 

    # Initialize the opened-list with root-node
    openedList = utils
    if type(openedList) == util.Stack or type(openedList) == util.Queue:
        openedList.push(start_state)
    elif heuristic != None:
        openedList.push(start_state, heuristic(start_state, problem))
    else:
        openedList.push(start_state, 0)

    # Iterating
    while 1:
        # If the open list is empty error 
        if openedList.isEmpty():
            return None

        # Getting the node from the stack to expand it and adding it to the search tree
        currentNode = openedList.pop()
        if search_tree.isInClosedList(currentNode) and not search_tree.isRoot(currentNode):
            continue

        # Checking if the node is in the closed-list, if it is we dont add it
        if not search_tree.isInClosedList(currentNode):
            search_tree.add(currentNode)
            search_tree.setParent(currentNode) 
            search_tree.setRoute(currentNode) 
            search_tree.setCost(currentNode)     

        # Checking if this is the goal
        if problem.isGoalState(currentNode if search_tree.isRoot(currentNode) else currentNode[0]):
            return search_tree.getNodeRoute(currentNode)
        else:
            # Iterating through the successors and adding them. Excluding the nodes that have been visited
            for child in problem.getSuccessors(currentNode if search_tree.isRoot(currentNode) else currentNode[0]):
                # Checking if the childs are already in the tree
                if not search_tree.isInClosedList(child):
                    search_tree.addChild(currentNode, child)
                    if type(openedList) == util.Stack or type(openedList) == util.Queue:
                        openedList.push(child)
                    elif heuristic != None:
                        openedList.push(child, search_tree.getNodeCost(currentNode)+child[2]+heuristic(child[0], problem))
                    else:
                        openedList.push(child, search_tree.getNodeCost(currentNode)+child[2])      


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
    return solveSimpleSearch(problem, util.Stack(), None)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    return solveSimpleSearch(problem, util.Queue(), None)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    return solveSimpleSearch(problem, util.PriorityQueue(), None)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    return solveSimpleSearch(problem, util.PriorityQueue(), heuristic)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
