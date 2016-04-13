'''
Created on 17/set/2015

@author: koelio
'''
from serv2.Server import Server

import zmq
import sys
import ConfigParser


config = ConfigParser.ConfigParser()
config.read('config.cfg')

HOST = str(config.get('Server', 'host'))
DATA_PORT = config.getint('Server', 'data_port')
REQ_PORT = config.getint('Server', 'req_port')
CONF_PORT = config.getint('Server', 'conf_port')
BUFF = config.getint('Server', 'buff')
    
    
class Main(object):
    
    server = None
    
    def run(self):
        context = zmq.Context()
    
        self.server = Server(context, HOST + ":" + DATA_PORT, HOST + ":" + REQ_PORT, HOST + ":" + CONF_PORT, BUFF)
        
        while self.server.thrd_Status:
            pass
            
        print("Server Down - Exiting")
        sys.exit()

if __name__ == '__main__':
    Main().run()    
