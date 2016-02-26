'''
Created on 20/set/2015

@author: koelio
'''

from django.core.exceptions import ObjectDoesNotExist

from serv2.JsonReqMsg import JsonReqMsg
from serv2.data_writer.ConcreteWriter import ConcreteWriter
from serv2.processor.Processor import Processor
from server.models import ClientRequest
import uuid
import json


class ReqProcessor(Processor):
    '''
    Concrete processor for incoming requests for new clients.
    '''
    jsonMsg = JsonReqMsg()
    writer = ConcreteWriter()
    complete_json = None

    def __init__(self):
        '''
        Constructor
        '''
        self.uuid = None
        
    def process(self, data):
        
        prsd = self.parseData(data)  
        #to log
        print(" \n parsed in req Data: " + str(prsd) + "\n")  
        self.jsonMsg.printMsg()
               
        if self.checkClientReq(self.jsonMsg.code):
            self.uuid = uuid.uuid4()
            client_req = ClientRequest.objects.create(uuid=self.uuid)
            client_req.token = self.jsonMsg.code
            client_req.organization = self.jsonMsg.org
            client_req.name = self.jsonMsg.device
            client_req.desc = self.jsonMsg.description
            client_req.save()
            print("Client added!")
            
        else:
            print("Metering point request with code " + str(self.jsonMsg.code) + " already exists.")
            # updating existent req
            client_req = ClientRequest.objects.get(token=self.jsonMsg.code)
            client_req.organization = self.jsonMsg.org
            client_req.name = self.jsonMsg.device
            client_req.desc = self.jsonMsg.description
            self.uuid = client_req.uuid
            
            self.complete_json = {"meteringPointId": str(self.uuid)}
            
    def checkClientReq(self, code):
        try:
            ClientRequest.objects.get(token=code)
            return False
        except ObjectDoesNotExist:
            return True
                                     
    def parseData(self, data):
        self.jsonMsg.parseMsg(data)
        return self.jsonMsg._getMsg()
    
    def getUuid(self):
        # TODO refactor
        return json.dumps(self.complete_json)
