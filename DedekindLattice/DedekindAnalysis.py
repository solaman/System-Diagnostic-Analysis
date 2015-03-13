'''
Created on Mar 13, 2015

@author: Solaman
'''
import cProfile
from DedekindNode import DedekindNode
from DedekindLattice import DedekindLattice

node = DedekindNode(4, [15])
lattice = DedekindLattice(5)

def analyzeDedekindNode():
    cProfile.run("node.generatePossibleConfigurations()")

def analyzeDedekindLattice():  
    cProfile.run("lattice.fillLattice()")
    
if __name__ == '__main__':
    #analyzeDedekindNode()
    analyzeDedekindLattice()