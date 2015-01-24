# mazeRouter.py

import graphics
import routerGUI
import time

state = {'free':0,'obs':-1,'wire':1,'pin':2}

def start(win,blocks,nets,mode):

    for net in nets:
        #TODO: Routing order by input file appearance, change to left-edge or other
        pins = net[2]             
        pinsVisited, pinsQueue = set(), []
        pinsQueue.extend(pins)
        pinsSrc = pinsQueue.pop(0)
        pinsVisited.clear()
        wireLen = 0
    
        #Subnet
        subnets = net[4]
        subnets.append([pinsSrc])
        subnets.append(0)
        indexSrc = routerGUI.getBlockInd(win,pinsSrc)
        blocks[indexSrc][3] = 1
    
        #CONNECT ALL PINS
        while pinsQueue:                  
            
            pinsVertex = pinsQueue.pop(0)
                
            if pinsVertex not in pinsVisited:
                pinsVisited.add(pinsVertex) 
                
                tags = [0]*len(blocks)
                pathLen, matchBlock = bfsNB(win,pinsSrc,blocks,pinsVertex,tags,net,mode)
                
                if (matchBlock):
                    indexMatch = routerGUI.getBlockInd(win,matchBlock)
                    
                    if (blocks[indexMatch][3]):
                        subnets
                    else 
                
                for subnet in subnets:
                    if (matchBlock in subnet):
                             
                #===============================================================
                # if (matchBlock):
                #     targetBlock = matchBlock
                #     pinsQueue.append(pinsSrc)
                # else:
                #     targetBlock = pinsSrc
                #  
                # if (pathLen!=0):
                #     traceBack(win,targetBlock,pathLen,blocks,tags,net)
                #===============================================================

                
            wireLen += (pathLen-2)
        #PINS CONNECTED
         
        net[3] = wireLen
        print "Finished pins"
          
    print "Finished nets"


#Trace Back over tags
def traceBack(win,pinsSrc,pathLen,blocks,tags,net):
    print "TRACEBACK!", pathLen
    
    track = pinsSrc
    
    while(pathLen!=1):

        pathLen -= 1
        neighbours = routerGUI.getBlockNB(track)

        for neighbour in neighbours:
            indexNB = routerGUI.getBlockInd(win,neighbour)
            
            if (tags[indexNB]==(pathLen)):
                blocks[indexNB][0].setFill(net[1])
                blocks[indexNB][1] = state['wire']
                blocks[indexNB][2] = net[0]
                track = neighbour
                break

        

# Breadth First search starting on pin Vertex looking for pin Source
def bfsNB(win,pinsSrc,blocks,pinsVertex,tags,net,mode):

    
    indexPin = routerGUI.getBlockInd(win,pinsVertex)
    tags[indexPin] = 1

    blocksVisited, blocksQueue = set(), [pinsVertex]                      
    
    while blocksQueue:
        
        blocksVertex = blocksQueue.pop(0)                                                    
        if blocksVertex not in blocksVisited:
            blocksVisited.add(blocksVertex)
            
            index = routerGUI.getBlockInd(win,blocksVertex)        
            tag = tags[index]+1
            
            for neighbour in routerGUI.getBlockNB(blocksVertex):
                indexNB = routerGUI.getBlockInd(win,neighbour)
                stateNB = blocks[indexNB][1]
                netNB = blocks[indexNB][2]
                if (tags[indexNB] == 0):
                    if (stateNB == state['free']):
                        tags[indexNB] = tag
                        routerGUI.markBlock(win,blocks[indexNB][0],tag)
                        blocksQueue.append(neighbour)
                        #TODO: A* tag with manhattan distance |xc-xt|+|yc-yt|                   
                    elif (netNB == net[0]):
                        print "On net ", net[0]
                        print "StateNB ", stateNB
                        return tag, neighbour
       
       
        #Run mode (clocked, stepped)
        key = win.checkKey()
        if (key == 'c'):
            mode = 'r'      
        if (mode.isdigit()):
            time.sleep(int(mode)*0.1)
        if (mode=='s'):
            while (key != 's'):
                key = win.getKey()
                if (key == 'c'):
                    mode = 'r'
                    break
            
            
       
    return 0, None

