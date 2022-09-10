#!/usr/bin/env python3

import numpy as np 
import cv2


def Draw_Horizontal(Array,Index1,Index2):   #Draws A horizontal Line from index1 to index2
    Local_Counter = Index1[1]
    while(Local_Counter <= Index2[1]):
        Array[Index1[0],Local_Counter]= 0
        Local_Counter+=1
        
def Draw_Vertical(Array,Index1,Index2):    #Draws A Vertical Line from index1 to index2
    Local_Counter = Index1[0]
    while(Local_Counter <= Index2[0]):
        Array[Local_Counter,Index1[1]]= 0
        Local_Counter+=1



def BFS(Map,Start,Goal,Direction):  # Direction for CCW -1  for CW 1

    Flag = False # Flag indicating if goal node is found
    
    # Initializing a queue 
    queue = []
    queue.append(Start)

    # Visited Nodes
    Visited = []

    # Parent Node Mapping
    Parents = np.zeros([10,10,2],dtype = int)


    while queue:   # If queue is not empty 

        Node = queue.pop(0)  # Pop first element in the queue

        if Node==Goal:   # Did we reach the goal?
            Flag = True
            break

        Neighbours = get_Neighbours(Node,Direction) # Get neighbours of this node

        for N in Neighbours: # For each neighbour of this node
            if not N in Visited and Map[N[0],N[1]]!=0:   # if this neighbour wasnt visited before and doesnt equal 0 (ie not an obstacle)
                queue.append(N)      # add to the queue
                Visited.append(N)     # add it to the visited
                Parents[N[0],N[1]] = Node  # add its parent node 

    if Flag == False:
        print('No path can be found')

    if Flag == True:
        path = get_Path(Parents,Goal,Start) # this function returns the path to the goal 
        return path


def DFS(Map,Start,Goal,Direction):  
    Flag = False 
    
    queue = []
    queue.append(Start)

    Visited = []

    Parents = np.zeros([10,10,2],dtype = int)


    while queue:  

        Node = queue.pop(-1)  

        if Node==Goal:  
            Flag = True
            break

        Neighbours = get_Neighbours(Node,Direction) 

        for N in Neighbours: 
            if not N in Visited and Map[N[0],N[1]]!=0:   
                queue.append(N)      
                Visited.append(N)    
                Parents[N[0],N[1]] = Node  

    if Flag == False:
        print('No path could be found')

    if Flag == True:
        path = get_Path(Parents,Goal,Start) 
        return path


        
    

def get_Path(Parents,Goal,Start):

    path = []
    Node = Goal  # start backward 
    path.append(Goal)
   
    while not np.array_equal(Node, Start):

       path.append(Parents[Node[0],Node[1]])  # add the parent node 
       Node = Parents[Node[0],Node[1]]        # search for the parent of that node 
     
    path.reverse()
    return path

    

def get_Neighbours(Node,Direction):    # Returns neighbours of the parent node   Direction = 1 for Clockwise/ Direction = -1 for CCW 

    Neighbours = []
    
    if Direction==1:
        Neighbours.append([Node[0],Node[1]+1])
        Neighbours.append([Node[0]+1,Node[1]+1])
        Neighbours.append([Node[0]+1,Node[1]])
        Neighbours.append([Node[0]+1,Node[1]-1])
        Neighbours.append([Node[0],Node[1]-1])
        Neighbours.append([Node[0]-1,Node[1]-1])
        Neighbours.append([Node[0]-1,Node[1]])
        Neighbours.append([Node[0]-1,Node[1]+1])
                        
    if Direction==-1:
        Neighbours.append([Node[0],Node[1]+1])
        Neighbours.append([Node[0]-1,Node[1]+1])
        Neighbours.append([Node[0]-1,Node[1]])
        Neighbours.append([Node[0]-1,Node[1]-1])
        Neighbours.append([Node[0],Node[1]-1])
        Neighbours.append([Node[0]+1,Node[1]-1])
        Neighbours.append([Node[0]+1,Node[1]])
        Neighbours.append([Node[0]+1,Node[1]+1])

    return Neighbours

if __name__ == '__main__':     
    Map = np.array ([[0,0,0,0,0,0,0],[0,1,1,1,1,1,0],[0,1,1,1,1,1,0],[0,1,1,0,1,1,0],[0,1,1,0,1,1,0],[0,1,1,0,1,1,0],[0,0,0,0,0,0,0]])
    #Map = img = cv2.imread('map.png',0)   #an option to draw the map instead of writing it manually
######################Here u type the start and goal fot the path planner############### 
         
    start=[1,1] #-----------<----------- 
    goal=[4,1]  #-----------<----------- 
    
########################################################################################    


    start[0],start[1]=6-start[1],start[0]
    goal[0],goal[1]=6-goal[1],goal[0]
    
    
######################Here we choose the path planning technique (BFS or DFS)###########    

    path = BFS(Map,start,goal,1) #-----------<-----------

########################################################################################    
    path = np.array(path)
    for i in range(len(path)):
        path[i][1],path[i][0]=6-path[i][0],path[i][1]
    print(path)
    print(Map)
        

