'''
Created on Feb 26, 2015

@author: Solaman
'''
import TransitionError.TransitionError

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
        #Will have a bit mask of 0x4
        self.bitMask = 2**(inputSize + 1) - 1
        self.inputSize = inputSize
        apexFunction = DedekindNode(self, [self.bitMask])
        self.lattice[ apexFunction.getIndex()] = apexFunction
        
        
class DedekindNode(object):
    '''
    A boolean function. It is up to the user to ensure that it is monotone.
    '''
    def __init__(self, dedekindLattice, acceptedConfigurations):
        '''
        Each function has a set of accepted configurations. To aid in the book keeping of this algorithm,
        each accepted configuration is stored by "level", namely, how many of the given inputs must be "off"
        in the configuration. so if the configuration 0b0001 is accepted and the bitmask is 0b1111, 
        then the configuration would be stored at the 3rd level.
        For rudimentary checking, the accepted configurations are added by descending level.
        '''
        self.acceptedConfigurations = []
        self.dedekindLattice = dedekindLattice
        for acceptedConfiguration in acceptedConfigurations:
            level = self.getConfigurationLevel( acceptedConfiguration)
            if level > len( self.acceptedConfigurations):
                raise TransitionError("Cannot add configurations beyond the highest level + 1")
            if level == len(self.acceptedConfigurations):
                self.acceptedConfigurations.append( [acceptedConfiguration])
            else:
                self.acceptedConfigurations[level].append( acceptedConfiguration)
                          
                
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
        return self.dedekindLattice.bitMask - hamming_distance(self.dedekindLattice.bitMask, configuration)
        

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