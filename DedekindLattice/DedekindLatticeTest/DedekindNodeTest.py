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
    
    def testGeneratePossibleConfigurations(self):
        configurationsUpToLevel3 = [15, 14, 13, 11, 7, 10, 12, 6, 5, 9, 3]
        node = DedekindNode(4, configurationsUpToLevel3)
        possibleCombinations = node.generatePossibleConfigurations()
        self.assertEquals(possibleCombinations, [8, 4, 2, 1])
        
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