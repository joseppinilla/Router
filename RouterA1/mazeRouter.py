# mazeRouter.py

import graphics
import routerGUI
import time

#TODO: change all representation of blocks XandY to tuples

def start(win,blocks,nets):
    while (True):
        key = win.getKey()
        if key == 'q': #quit 
            break
        #if key == 's': #step          
        if key == 'r': #run
            for netCnt,net in enumerate(nets):
                #TODO: Routing order by input file appearance, change to left-edge or other
                pins = net[2]             
                pinsVisited, pinsQueue = set(), []
                pinsQueue.extend(pins)
                pinsSrc = pinsQueue.pop(0)
                pinsVisited.clear()
           
                while pinsQueue:                  
                    
                    pinsVertex = pinsQueue.pop(0)                   
                    if pinsVertex not in pinsVisited:
                        pinsVisited.add(pinsVertex) 
                        
                        pathLen = bfsNB(win,pinsSrc,blocks,pinsVertex) 
                        if (pathLen!=0):
                            print "FOUND: TraceBack!", pathLen
                            #TODO:Traceback
                        
                            
                        print "Finished Blocks Queue"                        
                    print "Finished pin"
                print "Now tags"    
            print "Finished net"
    

def bfsNB(win,pinsSrc,blocks,pinsVertex):

    indexPin = routerGUI.getBlockInd(win,pinsVertex)
    tags = [0]*len(blocks)
    tags[indexPin] = 1

    blocksVisited, blocksQueue = set(), [pinsVertex]                      
    
    while blocksQueue:
        
        blocksVertex = blocksQueue.pop(0)                                                    
        if blocksVertex not in blocksVisited:
            blocksVisited.add(blocksVertex)
            
            print "vertex", blocksVertex
            index = routerGUI.getBlockInd(win,blocksVertex)        
            tag = tags[index]+1
            
            for neighbour in routerGUI.getBlockNB(blocksVertex):
                if pinsSrc == neighbour:
                    return tag
                indexNB = routerGUI.getBlockInd(win,neighbour)
                if ((blocks[indexNB][1] | tags[indexNB]) == 0):
                    tags[indexNB] = tag
                    routerGUI.markBlock(win,blocks[indexNB][0],tag)
                    print "Neighbour", neighbour
                    blocksQueue.append(neighbour)
                    #TODO: elif Look for wire of same net, connect to it
       
        time.sleep(0.1)
       
    return 0

