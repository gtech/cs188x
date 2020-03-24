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
import random, util, pdb, random

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
        foodList = newFood.asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        curFoodList = currentGameState.getFood().asList()

        eatGhost = 0
        distanceToGhost = manhattanDistance(newGhostStates[0].getPosition(), newPos)
        avoidGhost = 0

        foodDistances = [manhattanDistance(food, newPos) for food in curFoodList]
        bestFoodDistance = min(foodDistances)
        bestFoods = [index for index in range(len(foodDistances)) if foodDistances[index] == bestFoodDistance]
        chosenFood = curFoodList[random.choice(bestFoods)]
        chosenFoodDistance = manhattanDistance(newPos,chosenFood)

        foodPenalty = sum([manhattanDistance(food, newPos) for food in foodList])

        if distanceToGhost > 2:
            avoidGhost = 2000

        if newScaredTimes[0] > 2:
            eatGhost = 10000
        
#        score = successorGameState.getScore() + avoidGhost - foodPenalty/100 - chosenFoodDistance*20 - distanceToGhost * eatGhost 
        score = successorGameState.getScore() + avoidGhost - foodPenalty/100 - chosenFoodDistance*20
        return score

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
        """
        pacmanIndex = 0 
        actions = gameState.getLegalActions(pacmanIndex)

        bestActionValue = float('-inf')
        bestAction = actions[0]

        for action in actions:
            successor = gameState.generateSuccessor(pacmanIndex,action)
            actionValue = self.value(successor, 1, 0)

            if float(actionValue) > bestActionValue:

                bestAction = action
                bestActionValue = actionValue

        return bestAction

    def value(self, gameState, agentIndex, depth):
        #If we're at the bottom depth, give the state's util
 
        if agentIndex == gameState.getNumAgents():
            depth += 1
            agentIndex = 0
 
        if depth == self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        if agentIndex == 0:
            return self.maxValue(gameState,agentIndex, depth)
        else:
            return self.minValue(gameState,agentIndex, depth)

    def maxValue(self,gameState,agentIndex, depth):
        v = float('-inf')
        actions = gameState.getLegalActions(agentIndex)
        nextAgentIndex = agentIndex + 1
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex,action)
            v = max(v,self.value(successor, nextAgentIndex, depth))
        return v

    def minValue(self,gameState,agentIndex, depth):
        v = float('inf')
        actions = gameState.getLegalActions(agentIndex)
        nextAgentIndex = agentIndex + 1
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex,action)
            v = min(v,self.value(successor, nextAgentIndex, depth))
        return v
        
 #    def maxChoice(choices, choiceFunction):

#        lambda action: value(gameState.generateSuccessor(action), 0, 0)]
#         actionValues = [value for choice in choices: choiceFunction(choice)]

#         bestActionValue = min(actionValues)
#         bestActions = [index for index in range(len(foodDistances)) if foodDistances[index] == bestFoodDistance]
#         chosenFood = curFoodList[random.choice(bestFoods)]
    



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        pacmanIndex = 0 
        actions = gameState.getLegalActions(pacmanIndex)

        alpha = float('-inf')
        beta = float('inf')
        bestAction = actions[0]

        for action in actions:
            successor = gameState.generateSuccessor(pacmanIndex,action)
            actionValue = self.value(successor, 1, 0, alpha, beta)

            if float(actionValue) > alpha:
                bestAction = action
                alpha = actionValue

        return bestAction

    def value(self, gameState, agentIndex, depth, alpha, beta):
        #If we're at the bottom depth, give the state's util
 
        if agentIndex == gameState.getNumAgents():
            depth += 1
            agentIndex = 0
 
        if depth == self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        if agentIndex == 0:
            return self.maxValue(gameState,agentIndex, depth, alpha, beta)
        else:
            return self.minValue(gameState,agentIndex, depth, alpha, beta)

    def maxValue(self,gameState,agentIndex, depth, alpha, beta):
        v = float('-inf')
        actions = gameState.getLegalActions(agentIndex)
        nextAgentIndex = agentIndex + 1
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex,action)
            v = max(v,self.value(successor, nextAgentIndex, depth, alpha, beta))
            if v > beta: return v
            alpha = max(alpha, v)
        return v

    def minValue(self,gameState,agentIndex, depth, alpha, beta):
        v = float('inf')
        actions = gameState.getLegalActions(agentIndex)
        nextAgentIndex = agentIndex + 1
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex,action)
            v = min(v,self.value(successor, nextAgentIndex, depth, alpha, beta))
            if v < alpha: return v
            beta = min(beta, v)
        return v


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

        pacmanIndex = 0 
        actions = gameState.getLegalActions(pacmanIndex)

        alpha = float('-inf')
        beta = float('inf')
        bestAction = actions[0]

        for action in actions:
            successor = gameState.generateSuccessor(pacmanIndex,action)
            actionValue = self.value(successor, 1, 0, alpha, beta)

            if float(actionValue) > alpha:
                bestAction = action
                alpha = actionValue

        return bestAction

    def value(self, gameState, agentIndex, depth, alpha, beta):
        #If we're at the bottom depth, give the state's util
 
        if agentIndex == gameState.getNumAgents():
            depth += 1
            agentIndex = 0
 
        if depth == self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        if agentIndex == 0:
            return self.maxValue(gameState,agentIndex, depth, alpha, beta)
        else:
            return self.minValue(gameState,agentIndex, depth, alpha, beta)

    def maxValue(self,gameState,agentIndex, depth, alpha, beta):
        v = float('-inf')
        actions = gameState.getLegalActions(agentIndex)
        nextAgentIndex = agentIndex + 1
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex,action)
            v = max(v,self.value(successor, nextAgentIndex, depth, alpha, beta))
            if v > beta: return v
            alpha = max(alpha, v)
        return v

    def minValue(self,gameState,agentIndex, depth, alpha, beta):
        v = float('inf')
        actions = gameState.getLegalActions(agentIndex)
        nextAgentIndex = agentIndex + 1
        vTotal = 0
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex,action)
            vTotal += min(v,self.value(successor, nextAgentIndex, depth, alpha, beta))
            #            if v < alpha: return v
            #           beta = min(beta, v)
        
        return vTotal/len(actions)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: Pacman LOVES eating scared ghosts, he feels cold when he's away from his closest food, and has an extreme aversion to being within 2 spaces of a dangerous ghost.
      
    """
    # Useful information you can extract from a GameState (pacman.py)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    foodList = newFood.asList()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    curFoodList = currentGameState.getFood().asList()

    eatGhost = 0
    distanceToGhost = manhattanDistance(newGhostStates[0].getPosition(), newPos)
    avoidGhost = 0
    
    chosenFoodDistance = 0
    foodDistances = [manhattanDistance(food, newPos) for food in curFoodList] 
    if len(foodDistances) > 0:
        bestFoodDistance = min(foodDistances)
        bestFoods = [index for index in range(len(foodDistances)) if foodDistances[index] == bestFoodDistance]
        chosenFood = curFoodList[random.choice(bestFoods)]
        chosenFoodDistance = manhattanDistance(newPos,chosenFood)

    foodPenalty = sum([manhattanDistance(food, newPos) for food in foodList])

    if distanceToGhost > 2:
        avoidGhost = 2000

    if newScaredTimes[0] > 2:
        eatGhost = 10000
        score = currentGameState.getScore() + eatGhost - distanceToGhost*20
    else:
        score = currentGameState.getScore() + avoidGhost - chosenFoodDistance


    return score

#        score = successorGameState.getScore() + avoidGhost - foodPenalty/100 - chosenFoodDistance*20 - distanceToGhost * eatGhost 
# Abbreviation
better = betterEvaluationFunction

