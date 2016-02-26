'''
Created on 23/set/2015

@author: koelio
'''
from django.db import Error
from serv2.data_writer.Writer import Writer


class ConcreteWriter(Writer):
    '''
    Concrete writer to the DB. 
    '''

    def __init__(self):
        '''
        Constructor
        '''
#     def writeClient(self, client):
#         try:
#             client.save()
#         except (Exception, Error):
#             self.printTraceback()
        
    def writeSensor(self, sensor):
        try:
            sensor.save()
        except (Exception, Error):
            print("Error writing sensor: " + str(sensor.uuid))
            self.printTraceback()
            
    def writeMeasure(self, measurement):
        try:
            measurement.save()
        except (Exception, Error):
            print("Error writing measure: " + str([measurement.value][measurement.error]))
            self.printTraceback()
            
    def printTraceback(self):
        import traceback
        print(traceback.format_exc())
        print("Error writing DB.")