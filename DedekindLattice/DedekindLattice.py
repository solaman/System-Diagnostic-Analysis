'''
Created on Feb 26, 2015

@author: Solaman
'''
from Queue import Queue
import TransitionError

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
        self.lattice = [None] * (2**(2**inputSize))
        
        #bit mask refers to the possible bit values
        #of a given configuration. E.G. boolean functions with 4 inputs
        #Will have a bit mask of 0xF
        self.bitMask = 2**(inputSize) - 1
        self.inputSize = inputSize
        
        
    def fillLattice(self):
        emptyFunction = DedekindNode(self, [])
        self.lattice[ emptyFunction.getIndex()] = emptyFunction
        
        baseFunction = DedekindNode(self, [self.bitMask])
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
                print self.lattice[functionIndex].acceptedConfigurations
                self.monotoneCount += 1
            
    def addAllCombinations(self, node, possibleConfigurations, configurationsToAdd = []):
        if possibleConfigurations == []:
            if configurationsToAdd != []:
                function = DedekindNode(self, configurationsToAdd, node)
                self.lattice[ function.getIndex()] = function
                self.nodeQueue.put(function)
        else:
            configurationsToAdd.append( possibleConfigurations[0] )
            self.addAllCombinations(node, possibleConfigurations[1:], configurationsToAdd)
            configurationsToAdd.pop(-1)
            self.addAllCombinations(node, possibleConfigurations[1:], configurationsToAdd)
        
                
        
        
class DedekindNode(object):
    '''
    A boolean function. It is up to the user to ensure that it is monotone.
    '''
    def __init__(self, dedekindLattice, acceptedConfigurations, nodeToCopy = None):
        '''
        Each function has a set of accepted configurations. To aid in the book keeping of this algorithm,
        each accepted configuration is stored by "level", namely, how many of the given inputs must be "off"
        in the configuration. so if the configuration 0b0001 is accepted and the bitmask is 0b1111, 
        then the configuration would be stored at the 3rd level.
        For rudimentary checking, the accepted configurations are added by descending level.
        '''
        if nodeToCopy != None:
            temp = nodeToCopy.acceptedConfigurationsAsList()
            temp.extend(acceptedConfigurations)
            acceptedConfigurations = temp
        self.acceptedConfigurations = []
        self.dedekindLattice = dedekindLattice
        for acceptedConfiguration in acceptedConfigurations:
            level = self.getConfigurationLevel( acceptedConfiguration)
            if level > len( self.acceptedConfigurations):
                exceptionMessage = "Cannot add configurations beyond the highest level + 1" \
                + "\n attempted level: " + str(level) \
                +"\n level limit: " + str(len(self.acceptedConfigurations))
                raise Exception( exceptionMessage)
            if level == len(self.acceptedConfigurations):
                self.acceptedConfigurations.append( [acceptedConfiguration])
            else:
                self.acceptedConfigurations[level].append( acceptedConfiguration)
                          
    def acceptedConfigurationsAsList(self):
        acceptedConfigurations = []
        for level in self.acceptedConfigurations:
            acceptedConfigurations.extend(level)
            
        return acceptedConfigurations
    
    def generatePossibleConfigurations(self):
        '''
        Generates possible configurations to add to the function such that the new functions would be monotone
        (given that this function is monotone). We observe that this can be done by level combinations.
        E.G. if the input size is 4, and the last level of the function is 1->[0b1011, 0b0111], then the children
        of the node in the lattice can have the level 2 configuration [0b0011]. 
        (if any other, then it would not be monotone).
        ''' 
        possibleConfigurations = []
        if len(self.acceptedConfigurations) == 1:
            possibleConfigurations = self.getLevelOneConfigurations()
        elif len(self.acceptedConfigurations) == self.dedekindLattice.inputSize \
        and len(self.acceptedConfigurations[-1]) == self.dedekindLattice.inputSize:
            possibleConfigurations = [0]      
        elif len(self.acceptedConfigurations) == 0:
            return []
        elif len(self.acceptedConfigurations)< self.dedekindLattice.inputSize:
            configurationLevel = self.acceptedConfigurations[-1]
            for configurationOne in configurationLevel:
                for configurationTwo in self.acceptedConfigurations[-1][configurationLevel.index(configurationOne)+1:]:
                    possibleConfigurations.append( configurationOne & configurationTwo)
        else:
            print "no more configurations to add"
        
        return possibleConfigurations
            
    def getLevelOneConfigurations(self):
        '''
        Possible level One configurations are generated uniquely from all others. Given that the current
        function only accepts the state where all inputs are "on", possible level one configurations are any
        input such that one input is "off".
        E.G. if input size is 4, the children of {0b1111} can potentially have any of {0b0111, 0b1011, 0b1101, 0b1110}
        '''
        levelOneConfigurations = []
        for inputIndex in range(0, self.dedekindLattice.inputSize):
            levelOneConfigurations.append( (1 << inputIndex) ^ self.dedekindLattice.bitMask ) 
            
        return levelOneConfigurations
        
    def getIndex(self):
        '''
        If we treat each configuration as its own integer value, we can combine each value into an integer
        of size 2**inputSize bits. E.G. if the input size is 4, then each configuration has a value between 0-15.
        So an integer of 16 bits, where each bit is for each configuration, will represent the function
        and its accepted configurations. Since this value is unique, we can also use it as an index for the function
        '''
        index = 0
        for configurationLevel in self.acceptedConfigurations:
            for configuration in configurationLevel:
                index |= (1 << configuration) 
        return index
    
    def getConfigurationLevel(self, configuration):
        return hamming_distance(self.dedekindLattice.bitMask, configuration)
        

def hamming_distance( x, y):
    '''
    Calculates hamming distance between two unsigned int values.
    Code was copied from http://en.wikipedia.org/wiki/Hamming_distance
    '''
    dist = 0
    val = x ^ y
    while( val != 0):
        dist += 1
        val &= val -1
        
    return dist  

if __name__ == "__main__":
    import sys
    inputSize = sys.argv[1]
    dedekind = DedekindLattice(int(inputSize))
    dedekind.fillLattice()
    print dedekind.monotoneCount