'''
Created on 23/set/2015

@author: koelio
'''

class Writer(object):
    '''
    Abstrac Writer for data being written on the DB.
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
#     def writeClient(self, client):  # metodo astratto, per convenienza
#         raise NotImplementedError("Subclass must implement abstract method")
    
    def writeSensor(self, sensor):
        raise NotImplementedError("Subclass must implement abstract method")
        
    def writeMeasure(self, measurement):
        raise NotImplementedError("Subclass must implement abstract method")
