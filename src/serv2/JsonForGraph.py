'''
Created on 14/ott/2015

@author: koelio
'''

from server.models import Client
import json
from django.utils.dateformat import format

class JsonForGraph(object):
    '''
    A class to load data from DB and write it in a json file to be rendered with Javascript for data display.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.client = None
        self.JSON_PATH = 'server/static/firas/Library/data.json'
        
    def composeJson(self, client_id):
        
        self.client = Client.objects.get(uuid=client_id)
        
        self.out_file = open(self.JSON_PATH, "w")
        self.out_file.write(self.writeData())
        self.out_file.close()
    
    def writeData(self):
        
        self.sensor_list = []
        self.collectedData = []
        
        for sensor in self.client.sensor_set.all():           
            jsonToWrite = {}        
            tmp = {"measurementUnit": sensor.meas_unit, "sensorName": sensor.description,
                   }
            
            for meas in sensor.measurement_set.all():
                
                if meas.value != None: #avoiding nulls
                    
                    #truncating from unix epoch for Firas
                    time = str(format(meas.timestamp, 'c'))
                    time_tr = time[:19] if len(time) > 18 else time
                    
                    tmp2 = {"date": time_tr,
                           "value":meas.value}
                    
                    self.collectedData.append(tmp2)
                
            jsonToWrite = {"collectedData": self.collectedData}
            
            #free collectedData
            self.collectedData = []
            
            jsonToWrite.update(tmp)
            self.sensor_list.append(jsonToWrite)
            
        self.completeJson = {"sensors": self.sensor_list}
        
        return json.dumps(self.completeJson)