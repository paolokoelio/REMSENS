'''
Created on 17/set/2015

@author: koelio
'''
from serv2.data_parser.DataParser import DataParser
import traceback

class JsonReqMsg(object):
    '''
    Data structure for parsed JSON messages with print() testing feature.
    '''
    
    prsd = None
    
    def __init__(self):
        '''
        Constructor
        '''
        self.parser = DataParser()
        
    def parseMsg(self, rcvd):
        
        try:
            JsonReqMsg.prsd = self.parser.parseData(rcvd)   
            JsonReqMsg.org = JsonReqMsg.prsd.get('org_name')
            JsonReqMsg.device = JsonReqMsg.prsd.get("dev_name")
            JsonReqMsg.code = JsonReqMsg.prsd.get("code")
            
            JsonReqMsg.description = JsonReqMsg.prsd.get("desc")


        except:
            print(traceback.format_exc())
            print("JSON parsing failed.")          
    
    def _getMsg(self):
        return JsonReqMsg.prsd
    
    def printMsg(self):
        
        print("\n Org name: %s\n Ddevice name:  %s\n conf_code: %s\n desc: %s\n" 
          % (
             str(JsonReqMsg.org),
             str(JsonReqMsg.device),
             str(JsonReqMsg.code),
             str(JsonReqMsg.description)
            ) 
        )
        
        print("\n keys: %s\n" % str(JsonReqMsg.prsd.keys()))