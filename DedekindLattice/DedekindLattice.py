'''
Created on Feb 26, 2015

@author: Solaman
'''
from Queue import Queue
import TransitionError
from DedekindNode import DedekindNode

class DedekindLattice(object):
    '''
    We aim to generate the Dedekind Lattices using this class. Namely,
    We want to generate all monotone boolean functions given an n input size.
    Currently, we will aim to only generate the lattices in working memory.
    Future implementations will hopefully be able to dynamically
    Generate a node of a given Lattice.
    '''


    def __init__(self, inputSize):
        '''
        Constructor. For now, we will store each monotone boolean function
        as an object. Future implementations will store them as a single bit
        for lean memory usage
        '''
        if inputSize < 0:
            raise Exception("Input size must be greater than or equal to 0")
        self.lattice = [None] * (2**(2**inputSize))
        
        #bit mask refers to the possible bit values
        #of a given configuration. E.G. boolean functions with 4 inputs
        #Will have a bit mask of 0xF
        self.bitMask = 2**(inputSize) - 1
        self.inputSize = inputSize
        
        
    def fillLattice(self):
        emptyFunction = DedekindNode(self.inputSize, [])
        self.lattice[ emptyFunction.getIndex()] = emptyFunction
        
        baseFunction = DedekindNode(self.inputSize, [self.bitMask])
        self.lattice[ baseFunction.getIndex()] = baseFunction
        
        self.nodeQueue = Queue()
        self.nodeQueue.put(baseFunction)
        while not self.nodeQueue.empty():
            node = self.nodeQueue.get()
            possibleConfigurations = node.generatePossibleConfigurations()
            self.addAllCombinations(node, possibleConfigurations)
            
        self.monotoneCount = 0
        for functionIndex in range(0, len(self.lattice)):
            if self.lattice[functionIndex] != None:
                self.monotoneCount += 1
            
    def addAllCombinations(self, node, possibleConfigurations, configurationsToAdd = []):
        if possibleConfigurations == []:
            if configurationsToAdd != []:
                function = DedekindNode(self.inputSize, configurationsToAdd, node)
                #print str(function.acceptedConfigurations)
                self.lattice[ function.getIndex()] = function
                self.nodeQueue.put(function)
        else:
            configurationsToAdd.append( possibleConfigurations[0] )
            self.addAllCombinations(node, possibleConfigurations[1:], configurationsToAdd)
            configurationsToAdd.pop(-1)
            self.addAllCombinations(node, possibleConfigurations[1:], configurationsToAdd)
        
                
        
        


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print "Error: must provide the input size of the Dedekind Lattice"
    inputSize = sys.argv[1]
    dedekind = DedekindLattice(int(inputSize))
    dedekind.fillLattice()
    print dedekind.monotoneCount