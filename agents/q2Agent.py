import logging
import random

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState
from util import manhattanDistance


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class Q2_Agent(Agent):

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '3'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    @log_function
    def getAction(self, gameState: GameState):
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
        logger = logging.getLogger('root')
        logger.info('MinimaxAgent')
        "*** YOUR CODE HERE ***"
        #test_state = copy.deepcopy(gameState)
        num_of_ghost = len(gameState.getGhostStates())
        num_of_agent = num_of_ghost + 1
        beta = float('inf')
        alpha = float('-inf')
        max_value = float('-inf')
        final_move = Directions.STOP
        
        
        for move in gameState.getLegalActions(0):
            new = gameState.generateSuccessor(0,move)
            value = self.alpha_beta( 2*num_of_agent-1 ,alpha,beta,1,num_of_agent,new)
            print(value,move)
            if value>max_value:
                max_value = value
                final_move = move
            
            
        
        
        #time.sleep(1)
        #print(gameState.getFood())
        return final_move
        #util.raiseNotDefined()
    @log_function
    def alpha_beta(self, depth, alpha, beta, agent_index, num_of_agent, gameState: GameState):
        #print(depth)
        
        if depth == 0 or gameState.isWin() or gameState.isLose():  # terminal condition
            return self.evaluate1(gameState,depth)  # evaluate current situation
        
        if agent_index == 0:  # pacman
            max_eval = float('-inf')
            for move in gameState.getLegalActions(agent_index):  
                new = gameState.generateSuccessor(agent_index,move)
                newindex = (agent_index + 1) % num_of_agent
                eval = self.alpha_beta(depth - 1, alpha, beta,newindex,num_of_agent,new)  
                
                max_eval = max(max_eval, eval)  
                alpha = max(alpha, eval)  

                if beta <= alpha:  # cutoff
                    break  
            return max_eval

        else:  # ghost
            min_eval = float('inf')
            for move in gameState.getLegalActions(agent_index):
                new = gameState.generateSuccessor(agent_index,move)
                newindex = (agent_index + 1)% num_of_agent
                eval = self.alpha_beta(depth - 1, alpha, beta, newindex, num_of_agent, new)
                
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)

                if beta <= alpha:  # cutoff
                    break  
            return min_eval
    @log_function
    def evaluate(self,gameState: GameState):
        if gameState.isWin():
            score = float('inf')
            return score
        if gameState.isLose():
            score = -1000
            return score
        score = gameState.getScore()
        return score
    @log_function
    def evaluate1(self,gameState: GameState,depth):
        #pacman_pos = gameState.getPacmanPosition()
        num_of_ghost = len(gameState.getGhostStates())
        #num_of_food = gameState.getNumFood()
        capsules = gameState.getCapsules()
        score = gameState.getScore()  
         
        min_scared_dis = 10000
        #min_ghost_dis = 10000

        plus = 0
        scared = False
        for i in range(1,num_of_ghost+1):
            ghost = gameState.getGhostState(i)
            if ghost.scaredTimer > 0:
                scared = True
                break
                
        

        
        if gameState.isLose():
            score = -9999999-depth
            return score
        if gameState.isWin() and len(capsules)>0:
            score = -1000
            return score
        if scared:
            
            min_scared_dis = BFS_scared(gameState)
            
            plus = plus-min_scared_dis*100 
            
        if scared == False :
            #print(len(capsules),min_food_dist,min_capsule_dist)
            min_food_dist,min_capsule_dist = BFS(gameState)
            #print(min_food_dist,min_capsule_dist)
            #time.sleep(5)
            plus = plus - 100*len(capsules)-(min_food_dist+5*min_capsule_dist) 
                
        score = score * 1000000 + scared*100000 + plus
        return score

def BFS(gameState: GameState):
    walls = gameState.getWalls()
    goalmap = gameState.getFood()
    visited = [[0] * (walls.height+1) for _ in range(walls.width+1)]
    current = gameState.getPacmanPosition()
    queue = []
    start = []
    start.append(current[0])
    start.append(current[1])
    start.append(0)
    queue.append(start)
    capsules = gameState.getCapsules()
    min_food_dist = 0
    min_capsule_dist = 0
    while 1:
        if len(queue) == 0:
            return 0,0
        
        node = queue[0]

        if goalmap[node[0]][node[1]] and min_food_dist==0 :
            min_food_dist= node[2]
        if len(capsules)>0:
            for i in capsules:
                if i[0] == node[0] and i[1] == node[1] and min_capsule_dist==0:
                    min_capsule_dist = node[2]
                    break
        if len(capsules)==0 and min_food_dist!=0:
            return min_food_dist,0 
        if min_food_dist!=0 and min_capsule_dist!= 0:
            return min_food_dist,min_capsule_dist
        if visited[node[0]][node[1]] == 0:
            visited[node[0]][node[1]] = 1
        if node[0]+1 < goalmap.width and walls[node[0]+1][node[1]] == False and visited[node[0]+1][node[1]] == 0:
            queue.append([node[0]+1,node[1],node[2]+1])
            visited[node[0]+1][node[1]] = 1
        if node[0]- 1 >= 0 and walls[node[0]-1][node[1]] == False and visited[node[0]-1][node[1]]==0:
            queue.append([node[0]-1,node[1],node[2]+1])
            visited[node[0]-1][node[1]] = 1
        if node[1]+1 < goalmap.height and walls[node[0]][node[1]+1] == False and visited[node[0]][node[1]+1]==0:
            queue.append([node[0],node[1]+1,node[2]+1])
            visited[node[0]][node[1]+1] = 1
        if node[1]-1 >=0 and walls[node[0]][node[1]-1] == False and visited[node[0]][node[1]-1]==0:
            queue.append([node[0],node[1]-1,node[2]+1])
            visited[node[0]][node[1]-1] = 1
        queue.pop(0)
def BFS_scared(gameState: GameState):
    walls = gameState.getWalls()
    goalmap = gameState.getFood()
    visited = [[0] * (walls.height+1) for _ in range(walls.width+1)]
    current = gameState.getPacmanPosition()
    num_of_ghost = len(gameState.getGhostStates())
    queue = []
    start = []
    start.append(current[0])
    start.append(current[1])
    start.append(0)
    queue.append(start)
    
    
    while 1:
        if len(queue) == 0:
            return 0
        
        node = queue[0]

        
        for i in range(1,num_of_ghost+1):
            ghost = gameState.getGhostState(i)
            ghost_pos = gameState.getGhostPosition(i)
            if ghost.scaredTimer>0 and int(ghost_pos[0])==node[0] and int(ghost_pos[1]) == node[1]:
                return node[2]
            
        
        if visited[node[0]][node[1]] == 0:
            visited[node[0]][node[1]] = 1
        if node[0]+1 < goalmap.width and walls[node[0]+1][node[1]] == False and visited[node[0]+1][node[1]] == 0:
            queue.append([node[0]+1,node[1],node[2]+1])
            visited[node[0]+1][node[1]] = 1
        if node[0]- 1 >= 0 and walls[node[0]-1][node[1]] == False and visited[node[0]-1][node[1]]==0:
            queue.append([node[0]-1,node[1],node[2]+1])
            visited[node[0]-1][node[1]] = 1
        if node[1]+1 < goalmap.height and walls[node[0]][node[1]+1] == False and visited[node[0]][node[1]+1]==0:
            queue.append([node[0],node[1]+1,node[2]+1])
            visited[node[0]][node[1]+1] = 1
        if node[1]-1 >=0 and walls[node[0]][node[1]-1] == False and visited[node[0]][node[1]-1]==0:
            queue.append([node[0],node[1]-1,node[2]+1])
            visited[node[0]][node[1]-1] = 1
        queue.pop(0)
        