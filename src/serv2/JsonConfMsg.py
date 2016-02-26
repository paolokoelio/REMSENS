'''
Created on 17/set/2015

@author: koelio
'''
from serv2.data_parser.DataParser import DataParser
import traceback

class JsonConfMsg(object):
    '''
    Data structure for parsed JSON messages with print() testing feature.
    ''' 
    prsd = None
    
    def __init__(self):
        '''
        Constructor
        '''       
        self.parser = DataParser()
        self.REQ = 'request'
         
    def parseMsg(self, rcvd):
        
        try:

            JsonConfMsg.prsd = self.parser.parseData(rcvd)
            
            JsonConfMsg.mtr_point = JsonConfMsg.prsd.get('meteringPointId')        
            JsonConfMsg.request_type = JsonConfMsg.prsd.get(self.REQ)
           
        except:
            print(traceback.format_exc())
            print("JSON parsing failed.")
            
    def _getMsg(self):
        return JsonConfMsg.prsd
    
    def printMsg(self):
        
        print("\n In JsonConf, metering point id: %s\n request type:  %s\n" 
          % (
             str(JsonConfMsg.mtr_point),
             str(JsonConfMsg.request_type)
            ) 
        )
        
        print("\n keys: %s\n" % str(JsonConfMsg.prsd.keys()))