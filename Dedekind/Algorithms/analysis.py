'''
Created on Apr 28, 2015

@author: Solaman

Used to perform analysis on various
algorithms for computing Minimum Inconsistent Subsets.
'''
from Logarithmic_Extraction import HittingSetTree
from Model.DedekindLattice import DedekindLattice
from Model.DedekindSetMapping import getFullSet

algorithms = {}
algorithms["hitting_set_tree"] = HittingSetTree.computeAllMIS
isAcceptedOriginalFunction = None 

def runAnalysis(algorithmKey = None):
    algorithmKey = algorithmKey[0]
    if algorithmKey not in algorithms:
        print "sorry! That algorithm was not recognized."\
        , "\nHere are the options:"
        for _algorithmKey in algorithms.keys():
            print "\n\t", _algorithmKey
        return
    minCheck = -1
    maxCheck = 0
    algorithm = algorithms[algorithmKey]
    lattice = DedekindLattice(5)
    
    
    while True:
        currentNode = lattice.getNextNode()
        
        if currentNode == None:
            break
        
        modifyisAccepted(currentNode)
        fullConstraints = getFullSet(5)
        algorithm(currentNode, fullConstraints)
        if currentNode.callCount > maxCheck:
            maxCheck = currentNode.callCount
        if currentNode.callCount < minCheck or minCheck == -1:
            minCheck = currentNode.callCount
            
            
    print "min: ", minCheck, "max: ", maxCheck
      
def modifyisAccepted(setDescription):
    '''
    In order to properly analyze an algorithm, we need to check how
    many times it has to call "isAccepted" on the given setDescription.
    We make this modification here.
    '''
    
    setDescription.callCount = 0
    setDescription.tries = []
    import types
    setDescription.isAccepted = types.MethodType(isAccepted, setDescription)
    
    

  
def isAccepted(self, configuration):
    from Model.DedekindNode import isAccepted as isAcceptedOld
    self.callCount += 1
    return isAcceptedOld(self, configuration)  
    
