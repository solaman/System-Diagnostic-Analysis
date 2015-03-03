'''
Created on Mar 2, 2015

@author: Solaman
'''
import unittest
from DedekindLattice import DedekindLattice

class Test(unittest.TestCase):

    def setUp(self):
        self.dedekindLattice = DedekindLattice(3)


    def tearDown(self):
        pass


    def testConstructor(self):
        self.assertEquals(self.dedekindLattice.bitMask, 7)
        self.assertEquals(len(self.dedekindLattice.lattice), 256)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConstructor']
    unittest.main()