'''
Created on Mar 2, 2015

@author: Solaman
'''

class Error(Exception):
    pass

class TransitionError(Error):
    '''
    Raised when an operation attempts a state transition that is 
    not allowed.
    '''
    
    def __init__(self, msg):
        self.msg = msg