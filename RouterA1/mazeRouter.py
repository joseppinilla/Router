# mazeRouter.py

import graphics
import routerGUI
import time

state = {'free':0,'obs':-1,'wire':1,'pin':2}

def start(win,blocks,nets,mode):
    """Start maze router process iterating over nets to create subnets
        BLOCK:
        PIN:
        NET: 
        WIRE:
        TAG:
        SUBNET:
        FREE:
        SOURCE:
        VERTEX:
        NEIGHBOUR:
        
        """

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
        subnets.append([[pinsSrc],1]) #TODO: Change initialize pcenter 1 => value that is useful
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
                      
                    subnetNum = blocks[indexMatch][3]
                    if (subnetNum):
                        #Add vertex to subnet pins list
                        subnets[subnetNum-1][0].append(pinsVertex)
                    else:
                        #Found terminal of same net. Create subnet with terminals
                        subnetNum = len(subnets)+1
                        subnets.append([[pinsVertex,matchBlock],subnetNum]) #TODO: change index data to pcenter #TODO:Change so that only pinMatch is added not netMatch
                        blocks[indexMatch][3] = subnetNum
                             
                    if (pathLen!=0):
                        traceBack(win,matchBlock,pathLen,blocks,tags,net,subnetNum)
                             
                
            wireLen += (pathLen-2)
        #PINS CONNECTED
        
        #CONNECT ALL SUBNETS IF ANY
        #if (len(subnets))
        
        #SUBNETS CONNECTED
        
        
         
        print "Result", subnets
        net[3] = wireLen
        print "Finished pins"
          
    print "Finished nets"



def traceBack(win,trackBlk,pathLen,blocks,tags,net,subnet):
    """Trace Back over tags by expanding around trackBlk. Mark blocks: Color, state:'wire', net, and subnet"""
        
    while(pathLen!=1):

        pathLen -= 1
        
        neighbours = routerGUI.getBlockNB(trackBlk)

        for neighbour in neighbours:
            indexNB = routerGUI.getBlockInd(win,neighbour)
            
            if (tags[indexNB]==(pathLen)):
                blocks[indexNB][0].setFill(net[1])
                blocks[indexNB][1] = state['wire']
                blocks[indexNB][2] = net[0]
                blocks[indexNB][3] = subnet #TODO: This is not adding subnets to sink and src 
                trackBlk = neighbour
                break

        


def bfsNB(win,pinsSrc,blocks,pinsVertex,tags,net,mode):
    """ Breadth First search starting on pin Vertex looking for pin Source """
    
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

