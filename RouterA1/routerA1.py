import graphics
import random
import time
import sys
import getopt

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
    x_size = int(tmpList[0])
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
            #block : Corresponding graphics, -1(obs),X (net#)]
            block = [graphics.Rectangle(point1, point2),0]
            block[0].draw(win)
            blocks.append(block)
    
    #Draw obstacles
    obs = int(fin.readline())
    for ob in range(0,obs):       
        tmpList  = fin.readline().split()
        index = getBlockInd(int(tmpList[0]),int(tmpList[1]),x_size)
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
            index = getBlockInd(int(tmpList[offset]),int(tmpList[offset+1]),x_size)
            pin = [tmpList[offset],tmpList[offset+1]]
            blocks[index][0].setFill(net[1])
            blocks[index][1] = -1
            wires.append(pin)
        
        net.append(wires)
        nets.append(net)
          

    start_lives = 20 
    while start_lives > 0:
        mouse = win.getMouse()
        mouse_x = mouse.getX()
        mouse_y = mouse.getY()
        
        for index in range(0, len(blocks)):
            center = blocks[index][0].getCenter()
            center_x = center.getX()
            center_y = center.getY()
            
            if abs(center_x - mouse_x) < scale_x / 2:
                if abs(center_y - mouse_y) < scale_y / 2:
                    blocks[index][0].setFill(color)
                    blocks[index][1] = "alive"
                    start_lives -= 1

def getBlockInd(x,y,w):
    return (y*w)+x

if __name__ == "__main__":
    main(sys.argv[1:])		



