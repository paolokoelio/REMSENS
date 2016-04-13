'''
Created on 17/set/2015

@author: koelio
'''

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alpha.settings")

# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()
#
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

# HOST = 'tcp://*'
# DATA_PORT = '40666'
# REQ_PORT = '30666'
# CONF_PORT = '50666'
# BUFF = 1024

class Main(object):

    server = None

    def run(self):
        context = zmq.Context()

        self.server = Server(context, HOST + ":" + str(DATA_PORT), HOST + ":" + str(REQ_PORT), HOST + ":" + str(CONF_PORT), BUFF)

        while self.server.thrd_Status:
            pass

        print("Server Down - Exiting")
        sys.exit()

if __name__ == '__main__':
    Main().run()
