from HandleData import sFindDataID, HandleDateType
from shared_functions import *  # NOQA


def Action0701(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    sFindDataID(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1])
    tmpAPDULen = tmpAPDULen + 2

    output(data_in[offset + tmpAPDULen] + ' —— [' +
           str(int(data_in[offset + tmpAPDULen], 16)) + '] 方法标识')
    tmpAPDULen = tmpAPDULen + 1

    output(data_in[offset + tmpAPDULen] + ' —— 操作模式')
    tmpAPDULen = tmpAPDULen + 1

    tmpLenLen = HandleDateType(tmpAPDULen + offset, 1, 1, *data_in)
    tmpAPDULen = tmpAPDULen + tmpLenLen

    return tmpAPDULen


def Action0702(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    ActListSum = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— SEQUENCE OF个数=' + str(ActListSum))
    tmpAPDULen = tmpAPDULen + 1
    for i in range(0, ActListSum):

        sFindDataID(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1])
        tmpAPDULen = tmpAPDULen + 2

        output(data_in[offset + tmpAPDULen] + ' —— 方法标识')
        tmpAPDULen = tmpAPDULen + 1

        output(data_in[offset + tmpAPDULen] + ' —— 操作模式')
        tmpAPDULen = tmpAPDULen + 1

        tmpLenLen = HandleDateType(tmpAPDULen + offset, 1, 1, *data_in)
        tmpAPDULen = tmpAPDULen + tmpLenLen

    return tmpAPDULen


def Action0703(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    ActListSum = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— SEQUENCE OF个数=' + str(ActListSum))
    tmpAPDULen = tmpAPDULen + 1
    for i in range(0, ActListSum):

        sFindDataID(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1])
        tmpAPDULen = tmpAPDULen + 2

        output(data_in[offset + tmpAPDULen] + ' —— 方法标识')
        tmpAPDULen = tmpAPDULen + 1

        output(data_in[offset + tmpAPDULen] + ' —— 操作模式')
        tmpAPDULen = tmpAPDULen + 1

        tmpLenLen = HandleDateType(tmpAPDULen + offset, 1, 1, *data_in)
        tmpAPDULen = tmpAPDULen + tmpLenLen

        sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
        tmpAPDULen = tmpAPDULen + 4

        SecSum = int(data_in[offset + tmpAPDULen], 16)
        output(data_in[offset + tmpAPDULen] + ' —— 读取延时=' + str(SecSum))
        tmpAPDULen = tmpAPDULen + 1

    return tmpAPDULen
