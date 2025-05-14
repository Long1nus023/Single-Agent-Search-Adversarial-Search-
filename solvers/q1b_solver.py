#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1b_problem import q1b_problem

def q1b_solver(problem: q1b_problem):
    astarData = astar_initialise(problem)
    num_expansions = 0
    terminate = False
    while not terminate:
        num_expansions += 1
        terminate, result = astar_loop_body(problem, astarData)
    print(f'Number of node expansions: {num_expansions}')
    return result

#-------------------#
# DO NOT MODIFY END #
#-------------------#

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
    
    
def astar_initialise(problem: q1b_problem):
    # YOUR CODE HERE
    astarData = AStarData()
    problem.getStartState()

    starth = astar_heuristic(problem.current,problem.goal)
    start = successornode(problem.current[0],problem.current[1],starth,0)
    astarData.closelist.append(start)
    return astarData

def astar_loop_body(problem: q1b_problem, astarData: AStarData):
    # YOUR CODE HERE
    last = len(astarData.closelist) - 1
    currentresult = problem.isGoalState(astarData)
    if currentresult:
        print("=====path=====")
        for i in astarData.closelist:
            print(i.x,i.y)
        print(problem.current)
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
        print("====open====")
        for i in astarData.openlist:
            print(i.x,i.y)
        print("====close====")
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
