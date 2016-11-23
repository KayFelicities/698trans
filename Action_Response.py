from HandleData import sFindDataID, HandleDateType
from sFindIDFun import sFindErrID
from shared_functions import *  # NOQA


def Action8701(offset, *data_in):
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

    sFindErrID(data_in[offset + tmpAPDULen])
    tmpAPDULen = tmpAPDULen + 1

    tmpLenLen = HandleDateType(tmpAPDULen + offset, 1, 1, *data_in)
    tmpAPDULen = tmpAPDULen + tmpLenLen

    return tmpAPDULen


def Action8702(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1
    SetReadSum = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— SEQUENCE OF的个数=' + str(SetReadSum))
    tmpAPDULen = tmpAPDULen + 1
    for i in range(0, SetReadSum):

        sFindDataID(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1])
        tmpAPDULen = tmpAPDULen + 2

        output(data_in[offset + tmpAPDULen] + ' —— 方法标识')
        tmpAPDULen = tmpAPDULen + 1

        output(data_in[offset + tmpAPDULen] + ' —— 操作模式')
        tmpAPDULen = tmpAPDULen + 1

        sFindErrID(data_in[offset + tmpAPDULen])
        tmpAPDULen = tmpAPDULen + 1

        tmpLenLen = HandleDateType(tmpAPDULen + offset, 1, 1, *data_in)
        tmpAPDULen = tmpAPDULen + tmpLenLen

    return tmpAPDULen


def Action8703(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1
    SetReadSum = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— SEQUENCE OF的个数=' + str(SetReadSum))
    tmpAPDULen = tmpAPDULen + 1
    for i in range(0, SetReadSum):

        sFindDataID(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1])
        tmpAPDULen = tmpAPDULen + 2

        output(data_in[offset + tmpAPDULen] + ' —— 方法标识')
        tmpAPDULen = tmpAPDULen + 1

        output(data_in[offset + tmpAPDULen] + ' —— 操作模式')
        tmpAPDULen = tmpAPDULen + 1

        sFindErrID(data_in[offset + tmpAPDULen])
        tmpAPDULen = tmpAPDULen + 1

        tmpLenLen = HandleDateType(tmpAPDULen + offset, 1, 1, *data_in)
        tmpAPDULen = tmpAPDULen + tmpLenLen

        sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
        tmpAPDULen = tmpAPDULen + 4

        DataResult = data_in[offset + tmpAPDULen]
        tmpAPDULen = tmpAPDULen + 1
        if DataResult == '01':
            output(DataResult + ' —— Data')

            tmpLenLen = HandleDateType(tmpAPDULen + offset, 1, 1, *data_in)
            tmpAPDULen = tmpAPDULen + tmpLenLen

        else:

            if DataResult == '00':
                output(DataResult + ' —— DAR')
                sFindErrID(data_in[offset + tmpAPDULen])
                tmpAPDULen = tmpAPDULen + 1
            else:
                output(DataResult + ' —— 报文有误')

    return tmpAPDULen
