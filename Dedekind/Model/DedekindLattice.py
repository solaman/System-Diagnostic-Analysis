'''
Created on Feb 26, 2015

@author: Solaman
'''
from DedekindNode import DedekindNode
from Model.LevelPermutor import LevelPermutor
from DedekindNode import getIndex

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
        
        self.emptyFunction = DedekindNode(self.inputSize, [])
        self.lattice[ getIndex(self.emptyFunction)] = self.emptyFunction
        
        self.baseFunction = DedekindNode(self.inputSize, [self.bitMask])
        self.lattice[ getIndex(self.baseFunction)] = self.baseFunction
        
    def getNextNode(self):     
        '''
        Returns the most recently added node to the queue 
        if it is not empty.
        '''
        if self.nodeList == []:
            return None
        node = self.nodeList.pop()
        children = node.generateChildren()
        for child in children:
            self.nodeList.append(child)
            self.lattice[getIndex(child)] = child
        return node
        
        
    def fillLattice(self):
        self.nodeList = []
        self.nodeList.append(self.baseFunction)
        while self.getNextNode() != None:
            x = 1
        self.monotoneCount= len( self.lattice.values())
            
    def findUniqueFunctions(self):
        #We don't need to compute functions that are isomorphisms of each other.
        #We store each function by there level, and then counts by the number of possible children for the function
        #It is proven that functions by level that have the same number of possible children are isomorphisms
        #{"level" : {"isomorphismCount": count, "children" : children } }
        self.nodeList = []
        functionCount = 1
        
        self.baseFunction.isVisited = False
        self.baseFunction.parent = None
        self.nodeList.append(self.baseFunction)
        
        what = 10000
        mileMarker = 10000
        
        levelPermutor = LevelPermutor(self.inputSize)
        
        while self.nodeList != []:
            node = self.nodeList.pop()
            if node.isVisited == True:
                if node.parent == None:
                    functionCount += node.childrenCount
                    print len(self.lattice.keys())
                    return functionCount
                else:
                    node.parent.childrenCount += node.childrenCount
                    if node.parent.childrenCount >= what:
                        print "marker: ", what
                        what = node.parent.childrenCount * 2
                    continue
            
            if self.getKey(node) in levelPermutor:
                node.parent.childrenCount += levelPermutor[self.getKey(node)].childrenCount
            else:
                self.lattice[ getIndex(node) ] = node
                node.childrenCount = 1
                levelPermutor[node.acceptedConfigurations[-1]] = node
                children = node.generateChildren()
                node.isVisited = True
                self.nodeList.append(node)
                for child in children:
                    child.parent = node
                    child.isVisited = False
                    self.nodeList.append(child)
        
    def getKey(self, node):
        from DedekindNode import getIndex
        if hasattr(node, "key"):
            return node.key
        else:
            node.key = getIndex(node.acceptedConfigurations[-1])
        return node.key
                    
            
            
            
           
    def generateDotFiles(self):
        '''
        
        '''
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
        print "Done"
        

def getDedekindNumber(userInput):
    '''
    Constructs the Dedekind Lattice for the given input size and 
    returns the dedekind number associated with that input.
    Values that return within a minute are currently n <= 5.
    '''
    inputSize = int(userInput[0])
    dedekindLattice = DedekindLattice(inputSize)
    print dedekindLattice.findUniqueFunctions()
    
def generateDotFiles(userInput):
    '''
    Constructs the Dedekind Lattice for the given input size and
    generates the dot files for each monotone boolean function with the given input size.
    '''
    inputSize = int(userInput[0])
    dedekindLattice = DedekindLattice(inputSize)
    dedekindLattice.fillLattice()
    dedekindLattice.generateDotFiles()