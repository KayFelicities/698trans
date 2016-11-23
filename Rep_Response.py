from HandleData import sFindDataID
from shared_functions import *


def Rep0801(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    RepSum = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— RCSD，SEQUENCE OF个数=' + str(RepSum))
    tmpAPDULen = tmpAPDULen + 1

    for i in range(0, RepSum):
        sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
        tmpAPDULen = tmpAPDULen + 4

    return tmpAPDULen
