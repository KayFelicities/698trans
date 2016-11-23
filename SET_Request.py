from HandleData import sFindDataID, HandleDateType
from shared_functions import *  # NOQA


def Set0601(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
    tmpAPDULen = tmpAPDULen + 4

    tmpLenLen = HandleDateType(tmpAPDULen + offset, 1, 1, *data_in)
    tmpAPDULen = tmpAPDULen + tmpLenLen

    return tmpAPDULen


def Set0602(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1
    SetListSum = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— SEQUENCE OF的个数=' + str(SetListSum))
    tmpAPDULen = tmpAPDULen + 1
    for i in range(0, SetListSum):
        sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
        tmpAPDULen = tmpAPDULen + 4

        tmpLenLen = HandleDateType(tmpAPDULen + offset, 1, 1, *data_in)
        tmpAPDULen = tmpAPDULen + tmpLenLen

    return tmpAPDULen


def Set0603(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1
    SetReadSum = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— SEQUENCE OF的个数=' + str(SetReadSum))
    tmpAPDULen = tmpAPDULen + 1
    for i in range(0, SetReadSum):
        sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
        tmpAPDULen = tmpAPDULen + 4

        tmpLenLen = HandleDateType(tmpAPDULen + offset, 1, 1, *data_in)
        tmpAPDULen = tmpAPDULen + tmpLenLen

        sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
        tmpAPDULen = tmpAPDULen + 4

        SecSum = int(data_in[offset + tmpAPDULen], 16)
        output(data_in[offset + tmpAPDULen] + ' —— 读取延时=' + str(SecSum))
        tmpAPDULen = tmpAPDULen + 1

    return tmpAPDULen
