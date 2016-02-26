'''
Created on 20/set/2015

@author: koelio
'''

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from serv2.JsonMsg import JsonMsg
from serv2.data_writer.ConcreteWriter import ConcreteWriter
from serv2.processor.Processor import Processor
from server.models import Client, Sensor, Measurement
from serv2.JsonForGraph import JsonForGraph


class DataProcessor(Processor):
    '''
    Concrete processor for incoming data.
    '''
    jsonMsg = JsonMsg()
    writer = ConcreteWriter()
    jsonForGraph = JsonForGraph()

    def __init__(self):
        '''
        Constructor
        '''    
    def process(self, data):
        
        self.parseData(data)
        
        #to log
#         print(" \n parsed Data: " + str(prsd) + "\n")
#         self.jsonMsg.printMsg()
#         print(self.jsonMsg.device_id)
        
        self.client = self.checkClient(self.jsonMsg.metering_point_id)    
        self.sensor = self.checkSensor(self.jsonMsg.device_id) 
        self.measurement = self.writeMeasurement(self.jsonMsg.timestamp, self.sensor)

            
    def checkClient(self, metering_point):
        try:
            client = Client.objects.get(uuid=metering_point)
            return client
        except ObjectDoesNotExist:
            print("No metering point with " + str(metering_point) + " exists.")
            
    def checkSensor(self, device_id):
        try: 
            sensor = Sensor.objects.get(uuid=self.jsonMsg.device_id)
            return sensor
        except ObjectDoesNotExist:
            print("No device with " + str(device_id) + " exists. You may need to create one.")
            return None
       
    def writeMeasurement(self, timestamp, sensor):
        try: 
            measurement = Measurement.objects.create(timestamp=timestamp, sensor=sensor)
            
            self.checkMeasureValue(measurement)
            
            measurement.timestamp = self.jsonMsg.timestamp
            self.writer.writeMeasure(measurement)
            
            return measurement
           
        except IntegrityError:
            #if the measure already exists, overwrite
            measurement = Measurement.objects.get(timestamp=self.jsonMsg.timestamp)
            
            self.checkMeasureValue(measurement)
                
            measurement.timestamp = self.jsonMsg.timestamp
            self.writer.writeMeasure(measurement)
            
            return measurement
        
    def checkMeasureValue(self, measurement):
        
        if self.jsonMsg.value:  # il tipo e' dato da JsonMsg (true e false)
            measurement.value = self.jsonMsg.value
            measurement.error = None
            # return measurement
        elif self.jsonMsg.error:
            measurement.value = None
            measurement.error = self.jsonMsg.error
            # return measurement
                                     
    def parseData(self, data):
        self.jsonMsg.parseMsg(data)
        return self.jsonMsg._getMsg()
