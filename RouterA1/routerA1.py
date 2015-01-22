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
    
    x_scale = 50
    win_max = 500
    start_lives = 20
    
    fps = 1
    color = graphics.color_rgb(random.randrange(255),random.randrange(255), random.randrange(255))
    tickrate = 1 / fps
    scale = round(win_max / x_scale)
    ticker = tickrate
    blocks = []
    neighbours = 0
    
    win = graphics.GraphWin("Assignment 1", win_max, win_max)
    
    for cut in range(int(scale), int(win_max + 1), int(scale)):

        for cut2 in range(int(scale), int(win_max + 1), int(scale)):

            point1 = graphics.Point(cut, cut2)
            point2 = graphics.Point(cut - scale, cut2 - scale)
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
            
            if abs(center_x - mouse_x) < scale / 2:
                if abs(center_y - mouse_y) < scale / 2:
                    blocks[index][0].setFill(color)
                    blocks[index][1] = "alive"
                    start_lives -= 1

if __name__ == "__main__":
    main(sys.argv[1:])		



