'''
Created on Mar 3, 2015

@author: Solaman
'''

class DedekindNode(object):
    '''
    A boolean function. It is up to the user to ensure that it is monotone.
    '''
    
    def __init__(self, inputSize, acceptedConfigurations, nodeToCopy = None):
        '''
        Each function has a set of accepted configurations. To aid in the book keeping of this algorithm,
        each accepted configuration is stored by "level", namely, how many of the given inputs must be "off"
        in the configuration. so if the configuration 0b0001 is accepted and the bitmask is 0b1111, 
        then the configuration would be stored at the 3rd level.
        For rudimentary checking, the accepted configurations are added by descending level.
        '''
        self.inputSize = inputSize
        self.bitMask = self.bitMask = 2**(inputSize) - 1
        
        if nodeToCopy != None:
            temp = nodeToCopy.acceptedConfigurationsAsList()
            temp.extend(acceptedConfigurations)
            acceptedConfigurations = temp
        self.acceptedConfigurations = []
        
        acceptedConfigurations = sorted(acceptedConfigurations, \
               key=lambda configuration: self.getConfigurationLevel(configuration))
        
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
        newMaxLevel = len(self.acceptedConfigurations)
        if newMaxLevel == 1:
            possibleConfigurations = self.getLevelOneConfigurations()
        elif newMaxLevel == self.inputSize \
        and len(self.acceptedConfigurations[-1]) == self.inputSize:
            possibleConfigurations = [0]      
        elif newMaxLevel == 0:
            return []
        elif newMaxLevel< self.inputSize:
            possibleConfigurations = {}
            configurationLevel = self.acceptedConfigurations[-1]
            for configurationOne in configurationLevel:
                for configurationTwo in self.acceptedConfigurations[-1][configurationLevel.index(configurationOne)+1:]:
                    possibleConfiguration = configurationOne & configurationTwo
                    if self.getConfigurationLevel(possibleConfiguration) == newMaxLevel:
                        possibleConfigurations[ configurationOne & configurationTwo] = 0
            possibleConfigurations = possibleConfigurations.keys()
        
        return possibleConfigurations
            
    def getLevelOneConfigurations(self):
        '''
        Possible level One configurations are generated uniquely from all others. Given that the current
        function only accepts the state where all inputs are "on", possible level one configurations are any
        input such that one input is "off".
        E.G. if input size is 4, the children of {0b1111} can potentially have any of {0b0111, 0b1011, 0b1101, 0b1110}
        '''
        levelOneConfigurations = []
        for inputIndex in range(0, self.inputSize):
            levelOneConfigurations.append( (1 << inputIndex) ^ self.bitMask ) 
            
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
        return hamming_distance(self.bitMask, configuration)
        

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