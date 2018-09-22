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
	from game import Directions
	s = Directions.SOUTH
	w = Directions.WEST
	return  [s, s, w, s, w, w, s, w]


 




def depthFirstSearch(problem):
	"""
	Search the deepest nodes in the search tree first.

	Your search algorithm needs to return a list of actions that reaches the
	goal. Make sure to implement a graph search algorithm.

	To get started, you might want to try some of these simple commands to
	understand the search problem that is being passed in:

	print "Start:", problem.getStartState()
	print "Is the start a goal?", problem.isGoalState(problem.getStartState())
	print "Start's successors:", problem.getSuccessors(problem.getStartState())
	"""
	"*** YOUR CODE HERE ***"  
	fringe = util.Stack()
	explored = []
	fringe.push((problem.getStartState(),[],0))

	while not fringe.isEmpty():
		current_state, current_action, current_cost = fringe.pop()

		if problem.isGoalState(current_state):
			return current_action;

		if(current_state in explored):
			continue

		explored.append(current_state);

		suc=problem.getSuccessors(current_state)

		for next_state, next_action, next_cost in suc:
			fringe.push((next_state, current_action+[next_action], current_cost+next_cost));
	return []
	  

def breadthFirstSearch(problem):
	"""Search the shallowest nodes in the search tree first."""
	"*** YOUR CODE HERE ***"
	
	fringe = util.Queue()
	explored = []
	fringe.push((problem.getStartState(),[],0))

	while not fringe.isEmpty():
		current_state, current_action, current_cost = fringe.pop()

		if problem.isGoalState(current_state):
			return current_action
		elif(current_state in explored):
			continue

		explored.append(current_state);

		suc=problem.getSuccessors(current_state)

		for next_state, next_action, next_cost in suc:
			fringe.push((next_state, current_action+[next_action], current_cost+next_cost));
	return []



	#util.raiseNotDefined()

def uniformCostSearch(problem):
	"""Search the node of least total cost first."""
	"*** YOUR CODE HERE ***"
	from game import Directions
	direction_table = {'South': Directions.SOUTH, 'North': Directions.NORTH,
					  'West': Directions.WEST, 'East': Directions.EAST}
	explored = []
	queue = util.PriorityQueue()

	queue.push((problem.getStartState(), []), 0)

	while not queue.isEmpty():
	  node = queue.pop()
	  current_node = node[0]
	  next_node = node[1]

	  if problem.isGoalState(current_node):
		  return next_node
	  if current_node not in explored:
		  explored.append(current_node)
		  for i in problem.getSuccessors(current_node):
			  if i[0] not in explored:
				  
				  total_cost = problem.getCostOfActions(next_node + [direction_table[i[1]]])
				  queue.push((i[0], next_node + [direction_table[i[1]]]), total_cost)


	#mediumMaze cost = 68
	#mediumDottedMaze cost = 1
	#mediumScaryMaze cost = 68719479864
	#util.raiseNotDefined()

def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0

def aStarSearch(problem, heuristic=nullHeuristic):
	"""Search the node that has the lowest combined cost and heuristic first."""
	"*** YOUR CODE HERE ***"
	from game import Directions
	direction_table = {'South': Directions.SOUTH, 'North': Directions.NORTH,
					  'West': Directions.WEST, 'East': Directions.EAST}
	explored = []
	queue = util.PriorityQueue()

	queue.push((problem.getStartState(), []), 0)

	while not queue.isEmpty():
	  node = queue.pop()
	  current_node = node[0]
	  next_node = node[1]

	  if problem.isGoalState(current_node):
		  return next_node
	  if current_node not in explored:
		  explored.append(current_node)
		  for i in problem.getSuccessors(current_node):
			  if i[0] not in explored:
				  
				  total_cost = problem.getCostOfActions(next_node + [direction_table[i[1]]])
				  queue.push((i[0], next_node + [direction_table[i[1]]]), total_cost + heuristic(i[0], problem))
	
	#util.raiseNotDefined()
	#Astar bigmaze cost = 210
	#ucs bigmaze cost = 620
	#dfs openMaze cost = 298
	#bfs openMaze cost = 54
	#ucs openMaze cost = 54
	#astar openMaze cost = 54
	# The openMaze cost for astar, bfs, ucs is the same whereas for dfs has a high cost 298.


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
