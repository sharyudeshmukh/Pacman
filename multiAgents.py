# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util
from util import *

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        list_of_food = newFood.asList();
        next_ghost_pos = successorGameState.getGhostPositions()

        for pos_of_food in list_of_food:
          d_food = util.manhattanDistance(pos_of_food, newPos)

        for pos_of_ghost in next_ghost_pos:
          d_ghost = util.manhattanDistance(pos_of_ghost, newPos)


        ### return when pacman stops moving###
        if currentGameState.getPacmanPosition() == newPos:
          return -1000000

        if successorGameState.isWin():
          return 1000000

        if successorGameState.isLose():
          return -1000000
  

        if len(list_of_food) == 0:
          return 10000000
        else:
          min_list_of_food = min(list_of_food)
          
        result = successorGameState.getScore()*5
        result = result + len(successorGameState.getCapsules())*5
        result = result - d_food*2           
        return result


        
      

        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        maximum = 1000000
        agents_count = gameState.getNumAgents()

        def minVal(s, i, d):
            v = maximum
            _act = s.getLegalActions(i)
           
            new_ss = [s.generateSuccessor(i, action) for action in _act]
            for new_s in new_ss:
                v = min(v, _val(new_s, (i+1)%agents_count, d+1))
            return v
        
        def maxVal(s, i, d):
            v = -maximum
            _act = s.getLegalActions(i)
            new_ss = [s.generateSuccessor(i, action) for action in _act]
            for new_s in new_ss:
                v = max(v, _val(new_s, (i+1)%agents_count, d+1))
            return v
        
        def _val(s, i, d):
            if s.isWin() or s.isLose() or d > self.depth*agents_count:
                return self.evaluationFunction(s)
            if i>0:
                return minVal(s, i, d)
            else:
                return maxVal(s, i, d)

        best_v = -maximum
        best_action = None
        _act = gameState.getLegalActions()
    
        for action in _act:
            new_s = gameState.generateSuccessor(0, action)
            val = _val(new_s, 1, 2)
            if val>best_v:
                best_v = val
                best_action = action
       
        
        return best_action

        #util.raiseNotDefined()



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        maximum = 1000000
        agents_count = gameState.getNumAgents()

        def minVal(s, alpha, beta, i, d):
            v = maximum
            _act = s.getLegalActions(i)
           
            new_ss = [s.generateSuccessor(i, action) for action in _act]
            for new_s in new_ss:
                v = min(v, _val(new_s, alpha, beta, (i+1)%agents_count, d+1))
                if v<alpha: 
                  return v
                beta = min(beta, v)
            return v
        
        def maxVal(s, alpha, beta, i, d):
            v = -maximum
            _act = s.getLegalActions(i)
            new_ss = [s.generateSuccessor(i, action) for action in _act]
            for new_s in new_ss:
                v = max(v, _val(new_s, alpha, beta, (i+1)%agents_count, d+1))
                if v>beta: 
                  return v
                alpha = max(alpha,v)
            return v
        
        def _val(s, alpha, beta, i, d):
            if s.isWin() or s.isLose() or d > self.depth*agents_count:
                return self.evaluationFunction(s)
            if i>0:
                return minVal(s, alpha, beta, i, d)
            else:
                return maxVal(s, alpha, beta, i, d)

        alpha = -maximum
        beta = maximum
        best_v = -maximum
        best_action = None
        _act = gameState.getLegalActions()
    
        for action in _act:
            new_s = gameState.generateSuccessor(0, action)
            val = _val(new_s, alpha, beta, 1, 2)
            alpha = max(alpha, val)
            if val>best_v:
                best_v = val
                best_action = action
       
        
        return best_action



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        maximum = 1000000
        agents_count = gameState.getNumAgents()

        def expVal(s, i, d):
            v = 0.0
            _act = s.getLegalActions(i)
            new_ss = [s.generateSuccessor(i, action) for action in _act]
            for new_s in new_ss:
                v = v + _val(new_s, (i+1)%agents_count, d+1)
            return v/len(new_ss)

        def maxVal(s, i, d):
            v = -maximum
            _act = s.getLegalActions(i)
            new_ss = [s.generateSuccessor(i, action) for action in _act]
            for new_s in new_ss:
                v = max(v, _val(new_s, (i+1)%agents_count, d+1))
            return v
        
        def _val(s, i, d):
            if s.isWin() or s.isLose() or d > self.depth*agents_count:
                return self.evaluationFunction(s)
            if i>0:
                return expVal(s, i, d)
            else:
                return maxVal(s, i, d)

        best_v = -maximum
        best_action = None
        _act = gameState.getLegalActions()
    
        for action in _act:
            new_s = gameState.generateSuccessor(0, action)
            val = _val(new_s, 1, 2)
            if val>best_v:
                best_v = val
                best_action = action
       
        
        return best_action
        
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    #successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    list_of_food = newFood.asList();
    next_ghost_pos = currentGameState.getGhostPositions()
    d_food = 1000
    for food in list_of_food:
      temp_d = util.manhattanDistance(food, newPos)
      d_food = min(d_food, temp_d)

    d_ghost = 1000
    for ghost in next_ghost_pos:
      temp_d_ghost = manhattanDistance(ghost, newPos)
      d_ghost = min(d_ghost,temp_d_ghost)

    if currentGameState.isWin():
      return 1000000

    if currentGameState.isLose():
      return -1000000
  

    if len(list_of_food) == 0:
      return 10000000
    else:
      min_list_of_food = min(list_of_food)
          
    result = currentGameState.getScore()*5
    result = result - len(currentGameState.getCapsules())*5
    result = result - d_food*2           
    return result


#successorGameState = currentGameState.generatePacmanSuccessor(action)
    '''newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


    foodlist = newFood.asList();
    newghostposition = currentGameState.getGhostPositions()
    distancefromfood = 1000
    for food in foodlist:
      temp_dist = util.manhattanDistance(food, newPos)
      distancefromfood = min(distancefromfood,temp_dist)

    distancefromghost = 1000
    for ghost in newghostposition:
      temp_ghost_distance = manhattanDistance(ghost, newPos)
      distancefromghost = min(distancefromghost,temp_ghost_distance)

    if currentGameState.isWin():
      return 1000000

    if currentGameState.isLose():
      return -1000000
    ### return when pacman stops moving###
    #if currentGameState.getPacmanPosition() == newPos:
    #  return -100000

    ### save pacman from ghost ###
    ### scaredtimes if-else condition

    #for ghost_distance in distancefromghost:
    #  if ghost_distance < 2:  ## pacman dies with 3 and avg score less than 500 with 1
    #    return -100000 

    ##############################

    ### pacman went into infinite loop from 1 position away from food###

    ### pacman returned error after eating last food ###

    if len(foodlist) == 0:
      return 10000000
    else:
      min_foodlist = min(foodlist)
          

    ghost_dis = 0
    score = currentGameState.getScore()*5

    score -= len(currentGameState.getCapsules())*5
    #if distancefromghost:
    #  ghost_dis= 10/min(distancefromghost)

    score -= distancefromfood * 2  
    #score += 1000/distancefromfood            

    #score += ghost_dis
    #higher_number = 100000/len(foodlist) + score

    ## scaredtimes of ghost
    ## if pellet eaten chase ghosts else chase food and avoid ghosts


    #higher_number = 100000/len(foodlist)

    return score'''

# Abbreviation
better = betterEvaluationFunction

