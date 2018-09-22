        #successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = currentGameState.getPacmanPosition()
        newFood = currentGameState.getFood()
        newGhostStates = currentGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        list_of_food = newFood.asList();
        next_ghost_pos = successorGameState.getGhostPositions()
        d_food = 1000

        for food in list_of_food:
          temp_d = util.manhattanDistance(food, newPos)

        d_ghost = 1000

        for ghost in next_ghost_pos:
          temp_d_ghost = manhattanDistance(ghost, newPos)
          d_ghost = min(d_ghost,temp_d_ghost)

        if currentGameState.isWin():
          return 100000

        if currentGameState.isLose():
          return -100000
  

        if len(list_of_food) == 0:
          return 1000000
        else:
          min_list_of_food = min(list_of_food)
          
        result = currentGameState.getScore()*5
        result = result + len(currentGameState.getCapsules())*5
        result = result - d_food*2           
        return result
