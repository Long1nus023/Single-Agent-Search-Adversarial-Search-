import logging
import time
from typing import Tuple

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState
from collections import deque

class q1b_problem:
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
    """
    def __str__(self):
        return str(self.__class__.__module__)

    def __init__(self, gameState: GameState):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.goal=[]
        self.current=[]
        self.walls=[]
        self.goalmap=[]
        self.startingGameState: GameState = gameState
        self.startingGameState: GameState = gameState
    @log_function
    def BFS(self):
        visited = [[0] * (self.goalmap.height+1) for _ in range(self.goalmap.width+1)]
        queue = []
        queue.append(self.current)
        
        while 1:
            node = queue[0]
            if self.goalmap[node[0]][node[1]]:
                self.goal.append(node[0])
                self.goal.append(node[1])
                return
            else:
                if visited[node[0]][node[1]] == 0:
                    visited[node[0]][node[1]] = 1
                    if self.walls[node[0]+1][node[1]] == False:
                        queue.append([node[0]+1,node[1]])
                    if self.walls[node[0]-1][node[1]] == False:
                        queue.append([node[0]-1,node[1]])
                    if self.walls[node[0]][node[1]+1] == False:
                        queue.append([node[0],node[1]+1])
                    if self.walls[node[0]][node[1]-1] == False:
                        queue.append([node[0],node[1]-1])
            queue.pop(0)
                        
        
    @log_function
    def getStartState(self):
        "*** YOUR CODE HERE ***"
        self.current = self.startingGameState.getPacmanPosition()
        self.walls = self.startingGameState.getWalls()
        self.goalmap = self.startingGameState.getFood()
        print(self.goalmap)
        print(self.goalmap.width,self.goalmap.height)
        print("++++++++++++")
        self.BFS()
        print(self.goal)
        #util.raiseNotDefined()

    @log_function
    def isGoalState(self, state):
        "*** YOUR CODE HERE ***"
        last = len(state.closelist) - 1
        self.current = [state.closelist[last].x,state.closelist[last].y] #???
        #print(self.current)
        if self.current[0]==self.goal[0] and self.current[1]==self.goal[1]:
            return True
        return False
        #util.raiseNotDefined()

    @log_function
    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """
        "*** YOUR CODE HERE ***"
        result = {}
        x = state.current[0]
        y = state.current[1]
        #West
        if state.walls[x-1][y] == 0:
            result["West"] = [x-1,y]
        #East
        if state.walls[x+1][y] == 0:
            result["East"] = [x+1,y]
        #North
        if state.walls[x][y+1] == 0:
            result["North"] = [x,y+1]
        #South
        if state.walls[x][y-1] == 0:
            result["South"] = [x,y-1]
        return result
        #util.raiseNotDefined()

