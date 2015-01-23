import graphics
import random
import time
import sys
import getopt

x_size = 0
y_size = 0

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    print 'Input file is "', inputfile
    print 'Output file is "', outputfile
    
    fin = open(inputfile,'r') 
       
    #Draw window
    tmpList = fin.readline().split()
    global x_size
    x_size = int(tmpList[0])
    global y_size 
    y_size = int(tmpList[1])
    win_max_x = 1000
    win_max_y = (win_max_x*y_size)/x_size
    scale_x = round(win_max_x / x_size)
    scale_y = round(win_max_y / y_size) 
    win = graphics.GraphWin("Assignment 1", win_max_x, win_max_y)
    
    #Draw grid, create blocks
    blocks = []
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
        index = getBlockInd(int(tmpList[0]),int(tmpList[1]))
        blocks[index][0].setFill(graphics.color_rgb(0,0,255))
        blocks[index][1] = -1
    
    
    #Draw pins, Create nets[wires]
    netCnt = int(fin.readline())
    nets = []
    for i in range(0,netCnt):
        color = graphics.color_rgb(random.randrange(255),random.randrange(255),random.randrange(255))
        net = [i,color]
        tmpList = fin.readline().split()
        pins = int(tmpList[0])
        wires = []
        for j in range(0,pins):
            offset = (j*2)+1
            index = getBlockInd(int(tmpList[offset]),int(tmpList[offset+1]))
            pin = [tmpList[offset],tmpList[offset+1],0]
            blocks[index][0].setFill(net[1])
            graphics.markBlock(win,blocks[index][0],i+1)
            blocks[index][1] = -1
            wires.append(pin)
        
        net.append(wires)
        nets.append(net)



    while (True):
        key = win.getKey()
        if key == 'q': #quit 
            break
        #if key == 's': #step          
        if key == 'r': #run
                      
            for net in nets:

                toConnect = len(net[2])
                #TODO: Create pins queue
                
                for pin in net[2]:
                    start = (pin[0],pin[1])
                    
                    #end = 
                    visited, queue = set(), [start]
                    while queue:
                        vertex = queue.pop(0)
                        if vertex not in visited:
                            visited.add(vertex) 
                            block_x, block_y = int(vertex[0]), int(vertex[1])
                            neighbours = getBlockNB(block_x, block_y)
                            print neighbours
                            for nb in neighbours:
                                nb_x, nb_y = int(nb[0]), int(nb[1])
                                index = getBlockInd(nb_x, nb_y)
                                if (blocks[index][1]==0):
                                    print "block ", index, " is free"
                                    graphics.markBlock(win,blocks[index][0],"hey")
                    print "Finished queue"
                    break #DEBUG
                print "Finished pin"
                break #DEBUG
            
            
            
            
            print "Finished net"
                     
                      
            
#Get Coordinates of Neighbour Blocks
def getBlockNB(x,y):
    return [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]

#Convert Coordinates to BlockList Index
def getBlockInd(x,y):
    global x_size
    return (y*x_size)+x

if __name__ == "__main__":
    main(sys.argv[1:])		



