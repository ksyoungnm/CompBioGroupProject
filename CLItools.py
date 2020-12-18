import numpy as np
import os,sys,argparse

class noErrorParser(argparse.ArgumentParser):
    def error(self,message):
        self.exit(2)

def matrixgenCLI():
    parser = noErrorParser()
    parser.add_argument('-L','--LAMBDA',default=None)
    try:
        args = parser.parse_args()
        LAMBDA = float(args.LAMBDA)
    except:
        print("Where's the LAMBDA??")
        sys.exit(2)
    
    directory = 'L%g'%LAMBDA
    if os.path.exists(directory):
        print('Data already exists homie!')
        sys.exit(2)
    os.mkdir(directory)
    return(directory,LAMBDA)

def writematrix(directory,matrix,cvector,unlabeled):
    labelfile = directory+'/labels.txt'
    matrixfile = directory+'/matrix'
    cvectorfile = directory+'/cvector'
    with open(labelfile,'w') as f:
        [f.write(node+'\n') for node in unlabeled]
    np.save(matrixfile,matrix)
    np.save(cvectorfile,cvector)

def distributionCLI():
    parser = noErrorParser()
    parser.add_argument('direc')
    # parser.add_argument('-i','--iters',default=None)
    try:
        args = parser.parse_args()
        labelfile = args.direc+'/labels.txt'
        matrixfile = args.direc+'/matrix.npy'
        cvectorfile = args.direc+'/cvector.npy'
        assert os.path.exists(labelfile)
        assert os.path.exists(matrixfile)
        assert os.path.exists(cvectorfile) 
    except:
        print("Where the Data at")
        sys.exit(2)
    # try:
    #     iters = int(args.iters)
    # except:
    #     print("How many times u want that?")
    #     sys.exit(2)
    return(labelfile,matrixfile,cvectorfile)