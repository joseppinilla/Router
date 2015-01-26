import graphics
import random

x_size = 0
y_size = 0

state = {'free':0,'obs':-1,'wire':1,'pin':2}

tList = []

def drawRouter(fin,blocks,nets):
    """From input file:
        Draw grid, obstacles and net pins
        Fill blocks list
        Fill nets list
        Uses graphics.py
    """
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
            #block : Rectangle, state, net,subnet
            block = [graphics.Rectangle(point1, point2),0,0,0]
            block[0].draw(win)
            blocks.append(block)
    
    #Draw obstacles
    obs = int(fin.readline())
    for ob in range(0,obs):       
        tmpList  = fin.readline().split()
        index = getBlockInd(win,(int(tmpList[0]),int(tmpList[1])))
        
        blocks[index][0].setFill(graphics.color_rgb(0,0,255))
        blocks[index][1] = state['obs']
    
    #Draw pins, Create nets[wires]
    netCnt = int(fin.readline())
    
    for i in range(0,netCnt):
        color = graphics.color_rgb(random.randrange(255),random.randrange(255),random.randrange(255))
        net = [i+1,color,[],0,[]]
        tmpList = fin.readline().split()
        pinCnt = int(tmpList[0])
        pins = []
        for j in range(0,pinCnt):
            offset = (j*2)+1
            index = getBlockInd(win,(int(tmpList[offset]),int(tmpList[offset+1])))
            pin = (int(tmpList[offset]),int(tmpList[offset+1]))
            blocks[index][0].setFill(net[1])
            markBlock(win,blocks[index][0],i+1)

            blocks[index][1] = state['pin']
            blocks[index][2] = i+1
            pins.append(pin)
        
        #TODO: Sort pins different ways: [Src, closer1, closer2, closer3....], [Src, closerN, closerN-1...closer1]
        #TODO: Sort so that Source is left-top-most, center, etc.
        net[2] = pins
        nets.append(net)
    
    return win


def getBlockNB(block):
    """Get Coordinates of Neighbour Blocks"""
    global x_size
    global y_size
    x=block[0]
    y=block[1]
    #TODO: Order of returned neighbours is fixed, could be changed
    neighbours = []
    
    if y > 0:
        neighbours.append((x,y-1))
    if y < (y_size-1):
        neighbours.append((x,y+1))
    if x > 0:
        neighbours.append((x-1,y))
    if x < (x_size-1):
        neighbours.append((x+1,y))
    
    return neighbours


def delMarks(win,blocks):
    for mark in tList:
        mark.undraw()

def markBlock(win,rectangle,text):
    """Write tag on block"""
    #TODO: save t text objetc to undraw later on graphics.delitem(win,t)
    t = graphics.Text(rectangle.getCenter(),text) 
    t.draw(win)
    tList.append(t)
    return 0


def getBlockInd(win,block):
    """Convert Coordinates to BlockList Index"""
    global x_size
    x = block[0]
    y = block[1]
    return (y*x_size)+x


def printGridStates(blocks):
    """Print grid matrix of States"""
    print "========GRID OF STATES========="
    for blockCnt, block in enumerate(blocks):
        global x_size
        if blockCnt%x_size == 0:
            print "/" 
        print block[1], "\t",
    print ""  


def printGridSubNets(blocks):
    """Print grid matrix of SubNets"""
    print "========GRID OF SUBNETS========="
    for blockCnt, block in enumerate(blocks):
        global x_size
        if blockCnt%x_size == 0:
            print "/" 
        print block[3], "\t",
    print ""  


def printGridNets(blocks):
    """Print grid matrix of Nets"""
    print "========GRID OF NETS========="
    for blockCnt, block in enumerate(blocks):
        global x_size
        if blockCnt%x_size == 0:
            print "/" 
        print block[2], "\t",
    print ""  
        

def printGridTags(tags):
    """Print grid matrix of Tags"""
    print "========GRID OF TAGS========="
    for tagCnt, tag in enumerate(tags):
        global x_size
        if tagCnt%x_size == 0:
            print "/" 
        print tag, "\t",
    print ""