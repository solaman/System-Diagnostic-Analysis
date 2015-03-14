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
        self.lattice = {}
        
        #bit mask refers to the possible bit values
        #of a given configuration. E.G. boolean functions with 4 inputs
        #Will have a bit mask of 0xF
        self.bitMask = 2**(inputSize) - 1
        self.inputSize = inputSize
        
        self.nodeQueue = Queue()
        
        emptyFunction = DedekindNode(self.inputSize, [])
        self.lattice[ emptyFunction.getIndex()] = emptyFunction
        self.nodeQueue.put(emptyFunction)
        
        baseFunction = DedekindNode(self.inputSize, [self.bitMask])
        self.lattice[ baseFunction.getIndex()] = baseFunction  
        self.nodeQueue.put(baseFunction)
        
    def getNextNode(self):     
        '''
        Returns the most recently added node to the queue 
        if it is not empty.
        '''
        if self.nodeQueue.empty():
            return None
        node = self.nodeQueue.get()
        children = node.generateChildren()
        for child in children:
            self.nodeQueue.put(child)
            self.lattice[child.getIndex()] = child
        return node
        
        
    def fillLattice(self):
        while self.getNextNode() != None:
            x = 1
           
    def generateDotFiles(self):
        import os
        directoryName = os.path.join("GeneratedDedekindLattices", str(self.inputSize) + "_DedekindLattice")
        if not os.path.exists(directoryName):
            os.mkdir(directoryName)
        updateTime = self.monotoneCount/10
        generatedFiles = 0
        for function in self.lattice.itervalues():
            function.writeToDotFile(directoryName)
            generatedFiles += 1
            if generatedFiles % updateTime == 0:
                print generatedFiles, " written so far"
        


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "Error: must provide the input size of the Dedekind Lattice"
    inputSize = sys.argv[1]
    dedekind = DedekindLattice(int(inputSize))
    dedekind.fillLattice()
    
    if len(sys.argv) > 2:
        if sys.argv[2] == "true":
            dedekind.generateDotFiles()
    print dedekind.monotoneCount