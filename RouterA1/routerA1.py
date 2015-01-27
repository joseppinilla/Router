import sys
import getopt
import mazeRouter
import routerGUI

def main(argv):
    
    
    #=================Get options=================#
    inputfile = ''
    outputfile = ''
    verbose = False
    try:
        opts, args = getopt.getopt(argv, "hvi:o:", ["ifile=", "ofile="])
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
        elif opt in ("-v", "--verbose"):
            verbose = True
    
    #=================Draw window with grid. Create blocks and nets=================#   
    blocks = []
    nets = []
    fin = open(inputfile,'r')
    win = routerGUI.drawRouter(fin,blocks,nets)
    fin.close()
    
    #===================Wait for user input on execution mode================#
    key = win.getKey()
    if key == 'q': #quit 
        sys.exit()     
    elif (key in ('r','s','t')): #Run, Stepped, Timed
        if (key=='t'):
            key = win.getKey() #X * 0.1s
        mazeRouter.start(win,blocks,nets,key,verbose)
        for net in nets:
            print "Wire Len ", net.id, net.wlen
    
    
    #Stop to observe result
    while (True):
        key = win.getKey()
        if key == 'q': #quit 
            sys.exit()                    

if __name__ == "__main__":
    main(sys.argv[1:])		



