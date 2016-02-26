'''
Created on 17/set/2015

@author: koelio
'''
from serv2.Server import Server

import zmq
import sys


HOST = 'tcp://*'
DATA_PORT = '40666'
REQ_PORT = '30666'
CONF_PORT = '50666'
BUFF = 1024
    
    
class Main(object):
    
    server = None
    
    def run(self):
        context = zmq.Context()
    
        self.server = Server(context, HOST + ":" + DATA_PORT, HOST + ":" + REQ_PORT, HOST + ":" + CONF_PORT, BUFF)
        
        while self.server.thrd_Status:
            pass
            
        print("Server Down")
        sys.exit()

if __name__ == '__main__':
    Main().run()    