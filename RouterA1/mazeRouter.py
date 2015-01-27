# mazeRouter.py

import graphics
import routerGUI
import time

state = {'free':0,'obs':-1,'wire':1,'pin':2}

def start(win,blocks,nets,mode,verbose):
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
        #pins = net[2]             
        pinsVisited, pinsQueue = set(), []
        
        #pinsQueue.extend(pins)
        pinsQueue.extend(net.pins)
               
        pinsSrc = pinsQueue.pop(0)
        pinsVisited.clear()
        wireLen = 0
    
        #Subnet
        #subnets = net[4]
        #subnets.append([[pinsSrc],(0,0)])      
        net.subnets.append([[pinsSrc],(0,0)])
        
        indexSrc = routerGUI.getBlockInd(win,pinsSrc)
        #blocks[indexSrc][3] = 1
        blocks[indexSrc].subnet = 1
       
        #CONNECT ALL PINS
        while pinsQueue:                  
            
            pinsVertex = pinsQueue.pop(0)
                
            if pinsVertex not in pinsVisited:
                pinsVisited.add(pinsVertex) 
                
                tags = [0]*len(blocks)
                
                vertexIndex = routerGUI.getBlockInd(win,pinsVertex)
                #If block is not already on subnet
                #if (blocks[vertexIndex][3] == 0):                
                if (blocks[vertexIndex].subnet == 0):
                    pathLen, matchBlock = bfsNB(win,pinsSrc,blocks,pinsVertex,tags,net,1000,mode,verbose) #TODO: 1000 arbitrary big number
                
                    if (matchBlock):
                        indexMatch = routerGUI.getBlockInd(win,matchBlock)
                          
                        #subnetNum = blocks[indexMatch][3]
                        subnetNum = blocks[indexMatch].subnet
                        if (subnetNum):
                            #Add vertex to subnet pins list
                            #subnets[subnetNum-1][0].append(pinsVertex)
                            net.subnets[subnetNum-1][0].append(pinsVertex)
                            #TODO: Explore adding matchBlock to subnet and consider for closest subnet intra-subnet route
                        else:
                            #Found terminal of same net. Create subnet with terminals
                            #subnetNum = len(subnets)+1
                            #subnets.append([[pinsVertex,matchBlock],(0,0)])
                            subnetNum = len(net.subnets)+1
                            net.subnets.append([[pinsVertex,matchBlock],(0,0)])
                            
                            #blocks[indexMatch][3] = subnetNum
                            blocks[indexMatch].subnet = subnetNum
                                 
                        if (pathLen!=0):
                            traceBack(win,matchBlock,pathLen,blocks,tags,net,subnetNum)
                             
                
            wireLen += (pathLen-2)
        #PINS CONNECTED
        
        if verbose:
            routerGUI.delMarks(win,blocks)
        
        #CONNECT ALL SUBNETS IF ANY

        #subnetCnt = len(subnets)
        subnetCnt = len(net.subnets)
        print subnetCnt, " SUBNETS!"
        #netCtr = findCenter(pins) #TODO: This is center of all net. Find center between subnets? Center between closest pins?
        netCtr = findCenter(net.pins)

        while (subnetCnt != 1) :
            #anchorBlock = closestBlock(subnets[subnetCnt-1][0],netCtr)
            anchorBlock = closestBlock(net.subnets[subnetCnt-1][0],netCtr)
            print "CENTER ", netCtr, "ANCHOR ", anchorBlock, "SUBNET ", subnetCnt
            
            tags = [0]*len(blocks)
                        
            pathLen, matchBlock = bfsNB(win,anchorBlock,blocks,netCtr,tags,net,subnetCnt,mode,verbose)
            print pathLen , matchBlock
            
            if (matchBlock):
                if (pathLen!=0):
                    traceBack(win,matchBlock,pathLen,blocks,tags,net,subnetCnt)
        
            subnetCnt -= 1
        #SUBNETS CONNECTED
        
        
         
        #print "Result", subnets
        print "Result", net.subnets
        net.wlen = wireLen
        print "Finished pins"
          
    print "Finished nets"


def closestBlock(netBlocks, targetBlock):
    """"From a list of blocks, find closest Manhattan distance"""    
    closestVal = abs(netBlocks[0][0] - targetBlock[0]) + abs(netBlocks[0][1] - targetBlock[1])
    closest = netBlocks[0]
    iterBlocks = iter(netBlocks)
    next(iterBlocks)

    for block in iterBlocks:
        dist = abs(block[0] - targetBlock[0]) + abs(block[1] - targetBlock[1])
        if (dist < closestVal):
            closestVal = dist
            closest = block
    
    return closest          


def findCenter(netBlocks):
    """Find block at the geometric center of the net"""
    hiXVal, hiYVal = netBlocks[0][0], netBlocks[0][1]
    
    loXVal, loYVal = netBlocks[0][0], netBlocks[0][1]
          
    blockCnt = 1
    for block in netBlocks:
        if (block[0]>hiXVal):
            hiXVal = block[0]
            
        elif (block[0]<loXVal):
            loXVal = block[0]
            
            
        if (block[1]>hiYVal):
            hiYVal = block[1]
            
        elif (block[0]<loYVal):
            loYVal = block[1]
        blockCnt+=1
    
    #TODO: BFS around center to find non-obs, non-otherNet block
    
    return (int((loXVal+hiXVal)/2),int((loYVal+hiYVal)/2))

def traceBack(win,trackBlk,pathLen,blocks,tags,net,subnet):
    """Trace Back over tags by expanding around trackBlk. Mark blocks: Color, state:'wire', net, and subnet"""
        
    while(pathLen!=1):

        pathLen -= 1
        
        neighbours = routerGUI.getBlockNB(trackBlk)

        for neighbour in neighbours:
            indexNB = routerGUI.getBlockInd(win,neighbour)
            
            #TODO: Do something so that if traceback finds wire from other subnet it connects 
            if (tags[indexNB]==(pathLen)):
                #blocks[indexNB][0].setFill(net[1])
                blocks[indexNB].setFill(net.color)
                
                #blocks[indexNB][1] = state['wire']
                blocks[indexNB].state = 'wire'
                
                #blocks[indexNB][2] = net[0]
                blocks[indexNB].net = net.id
                
                #blocks[indexNB][3] = subnet
                blocks[indexNB].subnet = subnet 
                trackBlk = neighbour
                break

def bfsNB(win,pinsSrc,blocks,pinsVertex,tags,net,subnet,mode,verbose):
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
                #stateNB = blocks[indexNB][1]
                stateNB = blocks[indexNB].state
                #netNB = blocks[indexNB][2]
                netNB = blocks[indexNB].net
                #subnetNB = blocks[indexNB][3]
                subnetNB = blocks[indexNB].subnet
                if (tags[indexNB] == 0):
                    if (stateNB == state['free']):
                        tags[indexNB] = tag
                        if verbose:
                            #routerGUI.markBlock(win,blocks[indexNB][0],tag)
                            blocks[indexNB].setTag(win,tag)
                        blocksQueue.append(neighbour)
                        #TODO: A* tag with Manhattan distance |xc-xt|+|yc-yt|                   
                    #elif (netNB == net[0]):
                    elif (netNB == net.id):
                        if (subnetNB != subnet):
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


