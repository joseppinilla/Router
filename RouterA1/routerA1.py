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

    print 'Input file is "', inputfile
    print 'Output file is "', outputfile
    
    fin = open(inputfile,'r') 
       
    #Draw window with grid. Create blocks and nets   
    blocks = []
    nets = []
    win = routerGUI.drawRouter(fin,blocks,nets)


    mazeRouter.start(win,blocks,nets)
    
                   

if __name__ == "__main__":
    main(sys.argv[1:])		



