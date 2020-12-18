import numpy as np
import os,sys

# -------------------------------------------------- #
# README
# -------------------------------------------------- #
# go check the other file, matrixgen.py first! that one
# has to be run first because it generates the matrix that
# this file uses. once that one has run, you can put the
# LAMBDA or the directory name in here and this will run
# the iterations. epsilon is the error rate to define when
# the system has converged. the lower this value the longer
# the computation will take. with EPSILON = 0.001, time is 
# maybe 20-30 seconds to compute.
LAMBDA = 0.1
DIRECTORY = 'L%g'%LAMBDA

EPSILON = 0.001

def readlabels(filename):
    # maybe a little unfortunately, this need to preserve order,
    # so that we can index into the M and c in the same way they
    # were entered. So this does return a list, because order is important.
    with open(filename) as f:
        return [line.strip() for line in f]

def pickindices(distribution, n):
    # returns a list of n indices s.t. the ith index is the ith highest
    # in the original distribution
    selection = []
    cp = distribution.copy()
    while len(selection) < n:
        i = np.argmax(cp)
        cp[i] = 0.0
        selection.append(i) 
    return selection

def epsiiterate(matrix,cvector,epsi):
    # starts an initial distribution of 0.5 for every protein, and interates
    # until the elementwise difference between the previous and new vectors is
    # less than some epsilon
    prevdist = np.full_like(cvector,0.5)
    dist = np.matmul(matrix,prevdist) + cvector
    i = 0
    while np.sum(np.abs(dist-prevdist)) > epsi:
        prevdist = dist
        dist = np.matmul(matrix,prevdist) + cvector
        i+=1
    print('Iterations to converge:',i)
    return dist


def iteriterate(matrix,cvector,iters):
    # starts an initial distribution of every protein at 0.5, and iterates
    # a set number of times
    dist = np.full_like(cvector,0.5)
    for _ in range(iters):
        dist = np.matmul(matrix,dist) + cvector
    return dist

def main():
    # double checks the right files exist!
    try:
        labelfile = DIRECTORY+'/labels.txt'
        matrixfile = DIRECTORY+'/matrix.npy'
        cvectorfile = DIRECTORY+'/cvector.npy'
        assert os.path.exists(labelfile)
        assert os.path.exists(matrixfile)
        assert os.path.exists(cvectorfile)
    except:
        print("Couldn't find the right data!")
        sys.exit()

    # loads in all the data
    labels = readlabels(labelfile)
    matrix = np.load(matrixfile)
    cvector = np.load(cvectorfile)

    #finds the final distribution, and gets the top 50 candidates
    finaldistribution = epsiiterate(matrix,cvector,EPSILON)
    bestindices = pickindices(finaldistribution, 50)

    #prints them to the console
    for i in bestindices:
        print(labels[i],'->',finaldistribution[i])

if __name__ == '__main__':
    main()


