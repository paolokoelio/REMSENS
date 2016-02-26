'''
Created on 20/set/2015

@author: koelio
'''

#classe astratta per l'implementazione di un processore di dati

class Processor:
    '''
    Abstract class for concrete implementation of a data processor.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def process(self, data):  # metodo astratto, per convenienza
        raise NotImplementedError("Subclass must implement abstract method")
