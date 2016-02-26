'''
Created on 18/ott/2015

@author: koelio
'''

UPDATE = "UPDATE"
NOT_UPDATE = "NOTUPDATE"
FLAG = None
GET_PATH = "variables/conf_FLAG.txt"
SET_PATH1 = "serv2/variables/conf_FLAG.txt"
SET_PATH2 = "variables/conf_FLAG.txt"

def update1(flag):
    out_file = open(SET_PATH1, "w")
    out_file.write(flag)
    out_file.close()

def update2(flag):
    out_file = open(SET_PATH2, "w")
    out_file.write(flag)
    out_file.close()

def writeData():      
    return FLAG

def getFlag():    
    fl = open(GET_PATH, "r")
    tmp = fl.read()
    if tmp == UPDATE:
        FLAG = True
        fl.close()
        return True
    elif tmp == NOT_UPDATE:
        FLAG = False
        fl.close()
        return False
    else:
        fl.close()

def setFlag1(flag):
    if flag:
        update1(UPDATE)
        FLAG = True
    else:
        update1(NOT_UPDATE)
        FLAG = False

def setFlag2(flag):
    if flag:
        update2(UPDATE)
        FLAG = True
    else:
        update2(NOT_UPDATE)
        FLAG = False