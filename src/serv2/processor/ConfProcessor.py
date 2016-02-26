'''
Created on 20/set/2015

@author: koelio
'''

from django.core.exceptions import ObjectDoesNotExist


from serv2.JsonConfMsg import JsonConfMsg
from serv2.data_writer.ConcreteWriter import ConcreteWriter
from serv2.processor.Processor import Processor
from server.models import Client
import json


class ConfProcessor(Processor):
    '''
    Concrete processor for incoming requests for new configuration.
    '''
    jsonMsg = JsonConfMsg()
    writer = ConcreteWriter()
    CONF = 'configuration'

    def __init__(self):
        '''
        Constructor
        '''
        self.devices_list = []
        
    def process(self, data):
        
        # to log
        prsd = self.parseData(data)     
        print(" \n parsed Data: " + str(prsd) + "\n")     
        self.jsonMsg.printMsg()
        
        if self.checkConfReq(self.jsonMsg.mtr_point):
            print('Searching available sensors')
            
            if self.jsonMsg.request_type == self.CONF:
                
                print("Configuration requested for %s\n" % self.jsonMsg.mtr_point)
                
                for sensor in self.client.sensor_set.all():
                    jsonToSend = {}
                    json = self.composeJson(sensor)
                    
                    jsonToSend.update(json)
                    self.devices_list.append(jsonToSend)

        else:
            print("Client ok, but no sensors associated.")
            pass
            
        
        self.complete_json = {"devices": self.devices_list}
  
  
    def composeJson(self, sensor):
        json = {"meteringPointId": str(self.client.uuid),
                "command": sensor.command,
                "deviceId": str(sensor.uuid),
                "configuration": self.configurationJson(sensor),
                "location": self.locationJson(sensor),
                "privacy": sensor.privacy,
                "sampling": self.samplingJson(sensor),
                "sending": self.sendingJson(sensor)
                }
        return json
    
    def configurationJson(self, sensor):
        json = {
                "description": sensor.description,
                "protocol": {
                    "name": sensor.protocol_name,
                        "parameters": {
                            "min": sensor.protocol_min,
                            "max": sensor.protocol_max
                                }
                            }
                }
        return json
    
    def locationJson(self, sensor):
        json = {
               "name": self.client.place_name,
                "latitude": self.client.latitude,
                "longitude": self.client.longitude
                }
        return json
    
    def samplingJson(self, sensor):
        json = {
                 "type": sensor.sampling_type,
                 "period": sensor.period,
                 "period_unit": sensor.period_unit,
                 "delta": sensor.delta,
                 "delta_type":sensor.delta_type,
                 "min":sensor.delta_min,
                 "max":sensor.delta_max,
                 "timeout":sensor.timeout,
                 "timeout_unit":sensor.timeout_unit
                }
        return json
    
    def sendingJson(self, sensor):
        json = {
                "type": sensor.sending_type,
                "quota": sensor.quota,
                "quota_unit":sensor.quota_unit              
                }
        return json
    
    def checkConfReq(self, my_uuid):
        try:
            self.client = Client.objects.get(uuid=my_uuid)
            return True
        except ObjectDoesNotExist:
            print('\nThe requested client doesn\'t exist: ' + str(my_uuid) + 'or not associated yet.')
            return False
                                     
    def parseData(self, data):
        self.jsonMsg.parseMsg(data)
        return self.jsonMsg._getMsg()
    
    def getConf(self):
        return json.dumps(self.complete_json)
