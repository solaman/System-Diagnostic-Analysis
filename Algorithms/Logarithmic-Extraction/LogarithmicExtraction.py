'''
Created on Apr 23, 2015

@author: Solaman
'''

def computeSingleMIS(setDescription, contraints):
    '''
    Taken from 'A Hybrid Diagnosis Approach Combining Black-Box
    and White-Box Reasoning'. This attempts to find the Minimal Subset of Constraints
    that will be inconsistent for the given Set Description.
    @param setDescription- A set of rules linking several items together. 
    Think of this as boolean equation in Conjunctive Normal Form.
    @param Constraints- a set of items we would like to include.
    Think of this as an assignment for the previous boolean equation.
    '''
    return computeSingleMISHelper(SetDescription, set(), Constraints)

def computeSingleMISHelper(setDescription, currentConstraints, constraintsToAdd):
    if len(constraintsToAdd) == 1:
        return constraintsToAdd
    
    constraintsToAddLeft = set(random.sample(constraintsToAdd, len(constraintsToAdd)))
    constraintsToAddRight = constraintsToAdd - constraintsToAddLeft
    
    #If either subset unioned with the current constraints is inconsistent
    #then an MIS exists in the subet of them
    if not setDescription.isConsistent( currentConstraints.union(constraintsToAddLeft) ):
        return computeSingleMISHelper(setDescription, currentConstraints, constraintsToAddLeft)
    if not setDescription.isConsistent( currentConstraints.union(constraintsToAddRight)):
        return computeSingleMISHelper(setDescription, currentConstraints, constraintsToAddRight)
    
    #The both subsets unioned with the current constraints is consistent
    #Then an MIS of the current constraints must use elements from both subsets. 
    #This will find such an MIS
    potentialSolutionLeft = computeSingleMISHelper(setDescription, 
                                                   constraintsToAdd.union(constraintsToAddRight), constraintsToAddLeft)
    potentialSolutionRight = computeSingleMISHelper(setDescription,
                                                    constraintsToAdd.union(potentialSolutionLeft), constraintsToAddRight)
    return potentialSolutionLeft.union(potentialSolutionRight) 
    