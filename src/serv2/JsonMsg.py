'''
Created on 17/set/2015

@author: koelio
'''
from serv2.data_parser.DataParser import DataParser
import traceback

class JsonMsg(object):
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
        '''
        Parsing incoming JSON messages through DataParser and building up the data structure. 
        '''
        try:
            
            JsonMsg.prsd = self.parser.parseData(rcvd)
            
            JsonMsg.devices = JsonMsg.prsd['devices']
            for device in JsonMsg.devices:
        
                JsonMsg.metering_point_id = device.get("meteringPointId")
                JsonMsg.device_id = device.get("deviceId")
                JsonMsg.description = device.get("description")
                JsonMsg.privacy = device.get("privacy")
                
                for measurement in device["measurements"]["values"]:
                    JsonMsg.timestamp = measurement.get("timestamp")
                    JsonMsg.value = measurement.get("value")
                    JsonMsg.error = measurement.get("error")
            
                JsonMsg.latitude = device["location"].get('latitude')
                JsonMsg.longitude = device["location"].get("longitude")
                JsonMsg.loc_name = device["location"].get("name")             
#
        except:
            print(traceback.format_exc())
            print("JSON parsing failed.")
            
    def _getMsg(self):
        return JsonMsg.prsd
    
    def printMsg(self):
        '''
        For testing purposes
        '''
        print("\n metering point id: %s\n device id:  %s\n privacy: %s\n timestamp: %s\n latitude: %s\n longitude: %s\n name: %s\n description: %s\n " 
          % (
             str(JsonMsg.metering_point_id),
             str(JsonMsg.device_id),
             str(JsonMsg.privacy),
             str(JsonMsg.timestamp),
             str(JsonMsg.latitude),
             str(JsonMsg.longitude),
             str(JsonMsg.loc_name),
             str(JsonMsg.description)
            ) 
        )
        
        print("\n keys: %s\n" % str(JsonMsg.prsd.keys()))