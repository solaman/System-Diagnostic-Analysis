'''
Created on Apr 23, 2015

@author: Solaman
'''
from LogarithmicExtraction import computeSingleMIS
from sets import ImmutableSet
def computeAllMIS(setDescription, constraints):
    '''
    Taken from 'A Hybrid Diagnosis Approach Combining Black-Box
    and White-Box Reasoning'. This attempts to find all Minimal Subset of Constraints
    that will be inconsistent for the given Set Description.
    @param setDescription- A set of rules linking several items together. 
    Think of this as boolean equation in Conjunctive Normal Form.
    @param Constraints- a set of items we would like to include.
    Think of this as an assignment for the previous boolean equation.
    '''
    return computeSingleMIS(setDescription, constraints)
    misSet= set()
    currPath = ImmutableSet() 
    paths = set()
    misSets = computeAllMISHelper(setDescription, constraints,
                                   misSet, currPath, paths)
    return misSets
    
def computeAllMISHelper(setDescription, constraints, misSet, currPath, paths):
    #paths holds all previously visited paths of the hitting set tree
    #currPath is the current. If any previous path is a subset of this one
    #the we have already computed all MIS that would be found in the current path's subtree.
    for path in paths:
        if path in currPath:
            return misSet
       
    #if the current set of constraints is consistent
    #Then there cannot be anymore MIS in its subtree
    #so we add the current path to the set of paths enumerated and return. 
    if not setDescription.isAccepted(constraints):
        paths.add(currPath)
        return misSet
    #In order to avoid redundant MIS computations
    #We check the current set of MIS misSet
    #If it is possible to find any of the already computed MIS in the current iteration
    #(it does not share an element in the currPath) then we just use that MIS
    #and continue down the tree
    currentMIS = ImmutableSet()
    for mis in misSet:
        if mis.intersect(currPath) == ImmutableSet():
            currentMIS = mis
            break
    #If not MIS matches the previous description, we will need to 
    #compute a new one.
    if currentMIS == ImmutableSet():
        currentMIS = computeSingleMIS(setDescription, constraints)
        misSet.add(currentMIS)
        return misSet
        
    #iterate through the children of the current path
    for element in currentMIS:
        childPath = currPath.union( set(element))
        computeAllMISHelper(setDescription, constraints - set(element), misSet, childPath, paths)