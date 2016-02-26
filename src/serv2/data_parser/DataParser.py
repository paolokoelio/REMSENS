'''
Created on 27/mag/2015

@author: koelio
'''
import json
class DataParser(object):
    '''
    It parses the incoming JSON formatted string
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
    def parseData(self, data):
        parsed_json = json.loads(data)
        return parsed_json