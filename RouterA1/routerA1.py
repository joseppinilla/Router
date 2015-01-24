import graphics
import time
import sys
import getopt
import mazeRouter
import routerGUI


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
   
    fin = open(inputfile,'r') 
       
    #Draw window with grid. Create blocks and nets   
    blocks = []
    nets = []
    win = routerGUI.drawRouter(fin,blocks,nets)
    while (True):
        key = win.getKey()
        if key == 'q': #quit 
            sys.exit()     
        elif (key in ('r','s','t')):
            if (key=='t'):
                key = win.getKey()
            mazeRouter.start(win,blocks,nets,key)
            for net in nets:
                print "Wire Len ", net[0], net[3]
    
                   

if __name__ == "__main__":
    main(sys.argv[1:])		



