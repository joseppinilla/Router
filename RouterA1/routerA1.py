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
    
    
    tmpList = fin.readline().split()
    x_size = int(tmpList[0])
    y_size = int(tmpList[1])

    win_max_x = 1000
    win_max_y = (win_max_x*y_size)/x_size
    start_lives = 20
    
    print x_size
    print y_size
    
    fps = 1
    color = graphics.color_rgb(random.randrange(255),random.randrange(255), random.randrange(255))
    tickrate = 1 / fps
    scale_x = round(win_max_x / x_size)
    scale_y = round(win_max_y / y_size)
    ticker = tickrate
    blocks = []
    neighbours = 0
    
    print win_max_x
    print win_max_y
    
    win = graphics.GraphWin("Assignment 1", win_max_x, win_max_y)
    
    for cut in range(int(scale_x), int(win_max_x + 1), int(scale_x)):
 
        for cut2 in range(int(scale_y), int(win_max_y + 1), int(scale_y)):
 
            point1 = graphics.Point(cut, cut2)
            point2 = graphics.Point(cut - scale_x, cut2 - scale_y)
            block = [graphics.Rectangle(point1, point2), "dead", neighbours, "die"]
 
            block[0].draw(win)
 
            blocks.append(block)
             
            
            
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

if __name__ == "__main__":
    main(sys.argv[1:])		



