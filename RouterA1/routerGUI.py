import graphics
import random

x_size = 0
y_size = 0


def drawRouter(fin,blocks,nets):
    tmpList = fin.readline().split()
    global x_size
    x_size = int(tmpList[0])
    global y_size 
    y_size = int(tmpList[1])
    win_max_x = 1200
    win_max_y = (win_max_x*y_size)/x_size
    scale_x = round(win_max_x / x_size)
    scale_y = round(win_max_y / y_size) 
    win = graphics.GraphWin("Assignment 1", win_max_x, win_max_y)
    
    for cut in range(int(scale_y), int(win_max_y + 1), int(scale_y)):
    
        for cut2 in range(int(scale_x), int(win_max_x + 1), int(scale_x)):
    
            point1 = graphics.Point(cut2, cut)
            point2 = graphics.Point(cut2 - scale_x, cut - scale_y)
            #block : Corresponding graphics, 0(free)/-1(obs)/X(net#)]
            block = [graphics.Rectangle(point1, point2),0]
            block[0].draw(win)
            blocks.append(block)
    
    #Draw obstacles
    obs = int(fin.readline())
    for ob in range(0,obs):       
        tmpList  = fin.readline().split()
        index = getBlockInd(win,(int(tmpList[0]),int(tmpList[1])))
        
        blocks[index][0].setFill(graphics.color_rgb(0,0,255))
        blocks[index][1] = -1
    
    #Draw pins, Create nets[wires]
    netCnt = int(fin.readline())
    
    for i in range(0,netCnt):
        color = graphics.color_rgb(random.randrange(255),random.randrange(255),random.randrange(255))
        net = [i,color]
        tmpList = fin.readline().split()
        pinCnt = int(tmpList[0])
        pins = []
        for j in range(0,pinCnt):
            offset = (j*2)+1
            index = getBlockInd(win,(int(tmpList[offset]),int(tmpList[offset+1])))
            pin = (int(tmpList[offset]),int(tmpList[offset+1]))
            blocks[index][0].setFill(net[1])
            markBlock(win,blocks[index][0],i+1)
            blocks[index][1] = i+1
            pins.append(pin)
        
        net.append(pins)
        nets.append(net)
    
    return win

#Get Coordinates of Neighbour Blocks
def getBlockNB(block):
    global x_size
    global y_size
    x=block[0]
    y=block[1]
    #TODO: Order of given neighbours is fixed, could be changed
    neighbours = []
    
    if x > 0:
        neighbours.append((x-1,y))
    if x < (x_size-1):
        neighbours.append((x+1,y))
    if y > 0:
        neighbours.append((x,y-1))
    if y < (y_size-1):
        neighbours.append((x,y+1))
    
    return neighbours

#Write tag on block
def markBlock(win,rectangle,text):
    t = graphics.Text(rectangle.getCenter(),text) 
    t.draw(win)
    return 0

#Convert Coordinates to BlockList Index
def getBlockInd(win,block):
    global x_size
    x = block[0]
    y = block[1]
    return (y*x_size)+x

#Print grid matrix
def printGridStates(blocks):
    for blockCnt, block in enumerate(blocks):
        global x_size
        if blockCnt%x_size == 0:
            print "/" 
        print block[1], "\t",
        
        
#Print grid matrix
def printGridTags(blocks,net):
    for blockCnt, block in enumerate(blocks):
        global x_size
        if blockCnt%x_size == 0:
            print "/" 
        print block[2], "\t",