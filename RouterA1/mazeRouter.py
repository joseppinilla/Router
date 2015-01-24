# mazeRouter.py

import graphics
import routerGUI
import time

def start(win,blocks,nets):
    while (True):
        key = win.getKey()
        if key == 'q': #quit 
            break
        #if key == 's': #step          
        if key == 'r': #run
            netCnt = 0      
            for netCnt,net in enumerate(nets):
                #TODO: Routing order by input file appearance, change to left-edge or other
                pins = net[2]             
                pinsSrc = pins[0]
                pinsI = 1
                pinsSink  = pins[pinsI] 
                pinsVisited, pinsQueue = set(), [pinsSink]               
                pinsVisited.clear()
                print "Routing net ", netCnt             
                while pinsQueue:                  
                    
                    pinsVertex = pinsQueue.pop(0)                   
                    if pinsVertex not in pinsVisited:
                        pinsVisited.add(pinsVertex) 
                        blocksVisited, blocksQueue = set(), [pinsVertex]
                        
                        tag = 1
                        
                        while blocksQueue:
                            blocksVertex = blocksQueue.pop(0)
                            
                            if pinsSrc == blocksVertex:
                                print "FOUND"
                                break
                            
                            if blocksVertex not in blocksVisited:
                                blocksVisited.add(blocksVertex)
                                block_x, block_y = int(blocksVertex[0]), int(blocksVertex[1])
                                index = routerGUI.getBlockInd(win,block_x, block_y)
                                
                                #Routing algorithm
                                if (blocks[index][1]==0):
                                    routerGUI.markBlock(win,blocks[index][0],tag)
                                    blocks[index][2] = tag
                                    
                                    
                                #TODO: Look for wire of same net, connect to it 
                                elif (blocks[index][1]==(netCnt+1)):
                                    if blocksVertex != pinsSink:
                                        routerGUI.markBlock(win,blocks[index][0],"FOUND")
                                        break
                              
                                neighbours = routerGUI.getBlockNB(block_x, block_y)
                                blocks[index].append(neighbours)
                                blocksQueue.extend(neighbours)
                                #print blocksQueue
                            #time.sleep(1)
                            tag+=1 
                                        
                        print "Finished Blocks Queue"

                    pinsI += 1
                    if pinsI < len(pins):
                        pinsQueue.append(pins[pinsI])
                    
                    #print pinsQueue
                    print "Finished pin"
                
                routerGUI.printGridStates(blocks)
                
                break #DEBUG (ONE NET)     
            print "Finished net"
    



