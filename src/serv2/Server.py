import zmq
import sys
import thread
import os
import django
import time
import ConfigParser

from serv2.processor.ConcreteProcessor import DataProcessor
from serv2.processor.ReqProcessor import ReqProcessor
from serv2.processor.ConfProcessor import ConfProcessor
from serv2.JsonForGraph import JsonForGraph
from serv2.utils import conf_updater

class Server(object):
    '''
    The most important component which manages the threads for the communication sockets.
    '''
    REPLY = "ok"  # defined in common with the client
    msg = None
    __buff = 1024  # default
    __my_bind = ""
    __rcvd_message = None
    thrd_Status = True
    #Loading confs from configuration file
    __config = ConfigParser.ConfigParser()
    __config.read('config.cfg')

    processor = DataProcessor()
    req_processor = ReqProcessor()
    conf_processor = ConfProcessor()
    jsonWriter = JsonForGraph()
    django.setup()
    ConfUpdated = True

    def __init__(self, my_context, data_bind, req_bind, conf_bind, buff):
        '''
        The socket instantiation may lead to show error on some IDEs due to REP constant of ZMQ
        '''
        Server.__data_bind = data_bind
        Server.__req_bind = req_bind
        Server.__conf_bind = conf_bind

        Server.__buff = buff


        print('creating sockets... ')

        self.my_socket = my_context.socket(zmq.REP)
        self.req_socket = my_context.socket(zmq.REP)
        self.conf_socket = my_context.socket(zmq.REP)

        try:
            self.my_socket.bind(data_bind)
            self.req_socket.bind(req_bind)
            self.conf_socket.bind(conf_bind)
        except:
            print("One or more binds failed.")
            sys.exit()

        try:
            print('...starting threads by socket')
            thread.start_new_thread(self.data_handler, (self.my_socket,))
            time.sleep(1)
            thread.start_new_thread(self.req_handler, (self.req_socket,))
            time.sleep(1)
            thread.start_new_thread(self.conf_handler, (self.conf_socket,))
        except Exception:
            import traceback
            print(traceback.format_exc())
            print("Thread start failed. Restarting.")
            # time.sleep(2) testing purposes
            self.restart_program()

    def data_handler(self, clientsock):
        '''
        Thread for data handling
        '''
        print("\nData thread " + repr(thread.get_ident()) + " started")
        print("\nListening on: " + str(self.__data_bind))

        while 1:

            data = clientsock.recv(Server.__buff)
            if not data: break

            self.processData(data)

            sent_data = self.REPLY
            clientsock.send(sent_data)

        clientsock.close()
        print("-  connection closed")
        self.restart_program()


    def req_handler(self, clientsock):
        '''
        Thread for requests handling
        '''
        print("\nRequest thread " + repr(thread.get_ident()) + " started\n")
        print("Listening on: " + str(self.__req_bind))


        while 1:
            data = clientsock.recv(Server.__buff)

            print(' received req data:' + repr(data))

            self.processReq(data)

            sent_data = self.req_processor.getUuid()

            print('\nSending MeteringPoinId to client: ' + str(sent_data))
            clientsock.send(sent_data)


        clientsock.close()
        print("- closed connection")
        self.restart_program()

    def conf_handler(self, clientsock):
        '''
        Thread for configuration handling
        '''
        print("\nConf thread " + repr(thread.get_ident()) + " started\n")
        print("Listening on: " + str(self.__conf_bind))

        while 1:
            self.ConfUpdated = conf_updater.getFlag()
            if self.ConfUpdated:

                data = clientsock.recv(Server.__buff)

                print(' received config data:' + repr(data))

                self.processConf(data)

                sent_data = self.conf_processor.getConf()
                print('Sending Configuration to client: ' + str(sent_data))
                clientsock.send(sent_data)
                time.sleep(self.__config.getint('Section', 'timeout_upd'))
                conf_updater.setFlag2(False)

        clientsock.close()
        print("- connection closed")
        self.restart_program()

    def setConfUpdate(self, upd):
        self.ConfUpdated = upd

    def processData(self, data):
        self.processor.process(data)

    def processReq(self, data):
        self.req_processor.process(data)

    def processConf(self, data):
        self.conf_processor.process(data)

    def writeJson(self, data):
        self.jsonWriter.writeData(data)

    def restart_program(self):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python = sys.executable
        os.execl(python, python, * sys.argv)
