'''
Created on Mar 3, 2015

@author: Solaman
'''
import unittest
from DedekindNode import DedekindNode

class Test(unittest.TestCase):

    
    def setUp(self):
        self.invalidConfigurations = [15, 14, 13, 4 ]
        self.unorderedConfigurations = [14, 13, 15]
        self.orderedConfigurationsByLevel = [ [15], \
                                             [14, 13] \
                                             ]
        self.orderedConfigurations = [15, 14, 13]
        self.levelOneConfigurations = [ 14, 13, 11, 7]

        self.dedekindNode = DedekindNode(4, self.orderedConfigurations)

    def tearDown(self):
        pass
    
    def testGeneratePossibleConfigurationsFullLevel(self):
        '''
        Given that we have all combinations of a level k,
        Do we get all combinations at level k+1?
        (here, input size n=4, so we have k=2 and k+1=3)
        '''
        configurationsUpToLevel3 = [15, 14, 13, 11, 7, 10, 12, 6, 5, 9, 3]
        node = DedekindNode(4, configurationsUpToLevel3)
        possibleCombinations = node.generatePossibleConfigurations()
        self.assertEquals(set(possibleCombinations), set([8, 4, 2, 1]))
        
    def testGeneratePossibleConfigurationsSatisfiedLevelNoOutput(self):
        '''
        When at level k, possible level k+1 configurations are a boolean
        "and" of k+1 of the level k configurations such that they  belong 
        at level k+1. E.G.
        11100 &
        00111 &
        01110 =
        00100
        Which is not a valid k+1 configuration, so it is not included
        '''
        configurations = [31, 30, 29, 27, 23, 15, 28, 7, 14]
        node = DedekindNode(5, configurations)
        possibleCombinations = node.generatePossibleConfigurations()
        self.assertEquals(possibleCombinations, [])
        
    def testGeneratePossibleConfigurationsSatisfiedLevelOutput(self):
        '''
        When at level k, possible level k+1 configurations are a boolean
        "and" of k+1 of the level k configurations such that they  belong 
        at level k+1. E.G.
        11100 &
        01110 &
        01101 =
        01100
        Which is a valid k+1 configuration, so it should be included
        '''
        configurations = [31, 30, 29, 27, 23, 15, 28, 14, 13]
        node = DedekindNode(5, configurations)
        possibleCombinations = node.generatePossibleConfigurations()
        self.assertEquals(possibleCombinations, [12])
        
        configurations= [31, 30, 29, 27, 23, 15, 28, 7, 14, 22, 13 ]
        node = DedekindNode(5, configurations)
        possibleCombinations = node.generatePossibleConfigurations()
        self.assertEquals( set(possibleCombinations), set([12, 6]))
        
        
    def testGetLevelOneConfigurations(self):
        self.assertEquals(self.dedekindNode.getLevelOneConfigurations(), self.levelOneConfigurations)

    def testGetIndex(self):
        self.assertEquals(self.dedekindNode.getIndex(), 57344)
        
    def testAcceptedConfigurationsAsList(self):
        self.assertEquals(self.dedekindNode.acceptedConfigurationsAsList(), self.orderedConfigurations)
        
    def testUnorderedConfigurations(self):
        dedekindNode = DedekindNode( 4, self.unorderedConfigurations)
        self.assertEquals( dedekindNode.acceptedConfigurations, self.orderedConfigurationsByLevel)
        
    def testBadConfigurations(self):
        '''
        Tests if the constructor will raise an error if a bad list
        of configurations is given (one configuration is two levels above all others)
        '''
        self.assertRaises( Exception, DedekindNode, (4, self.invalidConfigurations) )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testBadConfigurations']
    unittest.main()