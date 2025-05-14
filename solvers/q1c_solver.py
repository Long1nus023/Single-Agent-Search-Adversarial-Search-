#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1c_problem import q1c_problem

#-------------------#
# DO NOT MODIFY END #
#-------------------#

def q1c_solver(problem: q1c_problem):
    astarData = astar_initialise(problem)
    pretreatment(problem)
    
    terminate = False
    flag = 0
    final_result = []
    if problem.possible_node ==0:
        final_result.append('Stop')
        return final_result
    while 1:
        terminate = False
        flag += 1
        if flag > problem.possible_node:
            break
        if flag > 1:
            astarData = AStarData()
            # find new goal
            problem.goal.pop(0)
            problem.goal.pop(0)
            step = problem.BFS()
            print(step)
            print(problem.possible_node)
            print(problem.finalreward)
            if step>((problem.possible_node - flag + 1)*10 + problem.finalreward):
                break
            starth = astar_heuristic(problem.current,problem.goal)
            start = successornode(problem.current[0],problem.current[1],starth,0)
            astarData.closelist.append(start)
        
        while not terminate:
            terminate, result = astar_loop_body(problem, astarData)
        #delete visited food
        problem.goalmap[problem.current[0]][problem.current[1]] = False
        print(problem.current)
        print(problem.goal)
        final_result = final_result + result
    print(problem.finalreward,problem.possible_node)
    print(final_result)
    final_result.append('Stop')
    return final_result
    


class successornode:
    def __init__(self,x,y,h,cost):
        self.x = x
        self.y = y
        self.h = h
        self.cost = cost
        self.f = h + cost
        self.actionlist = []
class AStarData:
    # YOUR CODE HERE
    def __init__(self):
        self.openlist = []
        self.closelist = []
def Delete_redundancy(astarData: AStarData):
    target = astarData.openlist[0]
    for j in astarData.closelist:
        if j.x == target.x and target.y == j.y:
            astarData.openlist.pop(0)
            return Delete_redundancy(astarData) 
    return
def compare_h(astarData: AStarData):
    minh = 100000000
    minpos = 0
    f = astarData.openlist[0].f
    for i in range(len(astarData.openlist)):
        if astarData.openlist[i].f > f:
            break
        if astarData.openlist[i].h < minh:
            minpos = i
            minh = astarData.openlist[i].h
    c = astarData.openlist[0]
    astarData.openlist[0] = astarData.openlist[minpos]
    astarData.openlist[minpos] = c
    
    
def astar_initialise(problem: q1c_problem):
    # YOUR CODE HERE
    astarData = AStarData()
    step = problem.getStartState()
    if step == 0:
        return astarData
    starth = astar_heuristic(problem.current,problem.goal)
    start = successornode(problem.current[0],problem.current[1],starth,0)
    astarData.closelist.append(start)
    return astarData

def astar_loop_body(problem: q1c_problem, astarData: AStarData):
    # YOUR CODE HERE
    last = len(astarData.closelist) - 1
    currentresult = problem.isGoalState(astarData)
    if currentresult:
        """print("=====path=====")
        for i in astarData.closelist:
            print(i.x,i.y)"""
        return currentresult, astarData.closelist[last].actionlist
    else:
        #get successors, put it in openlist, sort it, get minimum and put it into closelist
        successors = problem.getSuccessors(problem)
        
        for i in successors:
            flag = 0
            x = successors[i][0]
            y = successors[i][1]
            for j in astarData.closelist:
                if j.x == x and j.y == y:
                    flag=1
                    break
            if flag==1 :
                continue
            current = [x,y]
            goal = problem.goal
            h = astar_heuristic(current,goal)
            cost = astarData.closelist[last].cost + 1
            """print("---")
            print(x,y,h,cost)
            print("---")"""
            kidnode = successornode(x,y,h,cost)
            kidnode.actionlist += astarData.closelist[last].actionlist 
            kidnode.actionlist.append(i)
            #print(kidnode.actionlist)
            astarData.openlist.append(kidnode)
        
        astarData.openlist = sorted(astarData.openlist, key=lambda p: p.f)
        Delete_redundancy(astarData)
        
        compare_h(astarData)
        """print("====open====")
        for i in astarData.openlist:
            print(i.x,i.y)
        print("====close====")"""
        astarData.closelist.append(astarData.openlist[0])
        astarData.openlist.pop(0)
        #openlist pop, put it in closelist
        #astarData.cost = 父节点cost + 1
        #change  current state
        return currentresult, astarData.closelist[last].actionlist
            
    

def astar_heuristic(current, goal):
    # YOUR CODE HERE
    manhattan_distance = abs(current[0]-goal[0])+abs(current[1]-goal[1])
    return manhattan_distance
def pretreatment(problem: q1c_problem):
    finalreward = 500
    total = 0
    for i in range(problem.goalmap.width):
        for j in range(problem.goalmap.height):
            if problem.goalmap[i][j]:
                total += 1

                
    possible_node = BFS1(problem)

    if possible_node<total:
        finalreward = 0
    print("+++")
    print(finalreward,possible_node)
    problem.finalreward = finalreward
    problem.possible_node = possible_node
    
def BFS1(problem: q1c_problem):
        visited = [[0] * (problem.goalmap.height+1) for _ in range(problem.goalmap.width+1)]
        queue = []
        queue.append(problem.current)
        total = 0
        while 1:
            if len(queue) == 0:
                break
            
            node = queue[0]
            if problem.goalmap[node[0]][node[1]] :
                total += 1
            if visited[node[0]][node[1]] == 0:
                visited[node[0]][node[1]] = 1
            if node[0]+1 < problem.goalmap.width and problem.walls[node[0]+1][node[1]] == False and visited[node[0]+1][node[1]] == 0:
                queue.append([node[0]+1,node[1]])
                visited[node[0]+1][node[1]] = 1
            if node[0]- 1 >= 0 and problem.walls[node[0]-1][node[1]] == False and visited[node[0]-1][node[1]]==0:
                queue.append([node[0]-1,node[1]])
                visited[node[0]-1][node[1]] = 1
            if node[1]+1 < problem.goalmap.height and problem.walls[node[0]][node[1]+1] == False and visited[node[0]][node[1]+1]==0:
                queue.append([node[0],node[1]+1])
                visited[node[0]][node[1]+1] = 1
            if node[1]-1 >=0 and problem.walls[node[0]][node[1]-1] == False and visited[node[0]][node[1]-1]==0:
                queue.append([node[0],node[1]-1])
                visited[node[0]][node[1]-1] = 1
            queue.pop(0)
        return total