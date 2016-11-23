from HandleData import sFindDataID, HandleDateType
from sFindIDFun import sFindErrID
from shared_functions import *  # NOQA


def Get8501(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

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


def Get8502(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    ListSum = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— SEQUENCE OF OAD，个数=' + str(ListSum))
    tmpAPDULen = tmpAPDULen + 1

    for i in range(0, ListSum):
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


def Get8503(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
    tmpAPDULen = tmpAPDULen + 4

    ListSum = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— RCSD，SEQUENCE OF个数=' + str(ListSum))
    tmpAPDULen = tmpAPDULen + 1

    for i in range(0, ListSum):
        DataResult = data_in[offset + tmpAPDULen]
        tmpAPDULen = tmpAPDULen + 1
        if DataResult == '00':
            output(DataResult + ' —— 第' + str(i + 1) + '列OAD')
            sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
            tmpAPDULen = tmpAPDULen + 4
        else:
            if DataResult == '01':
                output(DataResult + ' —— 第' + str(i + 1) + '列ROAD')

                sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
                tmpAPDULen = tmpAPDULen + 4

                ListSum1 = int(data_in[offset + tmpAPDULen], 16)
                output(data_in[offset + tmpAPDULen] + ' —— ROAD，SEQUENCE OF个数=' + str(ListSum1))
                tmpAPDULen = tmpAPDULen + 1
                for k in range(0, ListSum1):
                    sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
                    tmpAPDULen = tmpAPDULen + 4
            else:
                output(data_in[offset + tmpAPDULen] + ' —— RCSD列标识有误')

    DataResult = data_in[offset + tmpAPDULen]
    tmpAPDULen = tmpAPDULen + 1

    if DataResult == '01':
        output(DataResult + ' —— 记录数据')
        ListSum2 = int(data_in[offset + tmpAPDULen], 16)
        output(data_in[offset + tmpAPDULen] + ' —— M条记录，M=' + str(ListSum2))
        tmpAPDULen = tmpAPDULen + 1

        tmpLenLen = HandleDateType(tmpAPDULen + offset, ListSum2, ListSum, *data_in)
        tmpAPDULen = tmpAPDULen + tmpLenLen
    else:
        if DataResult == '00':
            output(DataResult + ' —— DAR')
            sFindErrID(data_in[offset + tmpAPDULen])
            tmpAPDULen = tmpAPDULen + 1
        else:
            output(DataResult + ' —— 报文有误')

    return tmpAPDULen


def Get8504(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1
    SumRecord = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— 记录型对象个数=' + str(SumRecord))
    tmpAPDULen = tmpAPDULen + 1
    for j in range(0, SumRecord):
        sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
        tmpAPDULen = tmpAPDULen + 4

        ListSum = int(data_in[offset + tmpAPDULen], 16)
        output(data_in[offset + tmpAPDULen] + ' —— RCSD，SEQUENCE OF个数=' + str(ListSum))
        tmpAPDULen = tmpAPDULen + 1

        for i in range(0, ListSum):
            DataResult = data_in[offset + tmpAPDULen]
            tmpAPDULen = tmpAPDULen + 1
            if DataResult == '00':
                output(DataResult + ' —— 第' + str(i + 1) + '列OAD')
                sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
                tmpAPDULen = tmpAPDULen + 4
            else:
                if DataResult == '01':
                    output(DataResult + ' —— 第' + str(i + 1) + '列ROAD')
                    ListSum1 = int(data_in[offset + tmpAPDULen], 16)
                    output(data_in[offset + tmpAPDULen] + ' —— ROAD，SEQUENCE OF个数=' + str(ListSum1))
                    tmpAPDULen = tmpAPDULen + 1
                    for k in range(0, ListSum1):
                        sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
                        tmpAPDULen = tmpAPDULen + 4
                else:
                    output(data_in[offset + tmpAPDULen] + ' —— RCSD列标识有误')

        DataResult = data_in[offset + tmpAPDULen]
        tmpAPDULen = tmpAPDULen + 1

        if DataResult == '01':
            output(DataResult + ' —— 记录数据')
            ListSum2 = int(data_in[offset + tmpAPDULen], 16)
            output(data_in[offset + tmpAPDULen] + ' —— M条记录，M=' + str(ListSum2))
            tmpAPDULen = tmpAPDULen + 1

            tmpLenLen = HandleDateType(tmpAPDULen + offset, ListSum2, ListSum, *data_in)
            tmpAPDULen = tmpAPDULen + tmpLenLen
        else:
            if DataResult == '00':
                output(DataResult + ' —— DAR')
                sFindErrID(data_in[offset + tmpAPDULen])
                tmpAPDULen = tmpAPDULen + 1
            else:
                output(DataResult + ' —— 报文有误')

    return tmpAPDULen


def Get8505(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    output(data_in[offset + tmpAPDULen] + ' —— 末帧标志')
    tmpAPDULen = tmpAPDULen + 1

    # 分帧序号
    FZNo = int(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1], 16)
    output(data_in[offset + tmpAPDULen] + ' ' +
           data_in[offset + tmpAPDULen + 1] + ' —— 分帧序号=' + str(FZNo))
    tmpAPDULen = tmpAPDULen + 2

    # 分帧响应
    FZFlag = data_in[offset + tmpAPDULen]
    tmpAPDULen = tmpAPDULen + 1

    if FZFlag == '01':
        output(FZFlag + ' —— 对象属性')
        ListSum = int(data_in[offset + tmpAPDULen], 16)
        output(data_in[offset + tmpAPDULen] + ' —— SEQUENCE OF OAD，个数=' + str(ListSum))
        tmpAPDULen = tmpAPDULen + 1

        for i in range(0, ListSum):
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

    else:
        if FZFlag == '02':
            output(FZFlag + ' —— 记录型对象属性')
            SumRecord = int(data_in[offset + tmpAPDULen], 16)
            output(data_in[offset + tmpAPDULen] + ' —— 记录型对象个数=' + str(SumRecord))
            tmpAPDULen = tmpAPDULen + 1
            for j in range(0, SumRecord):
                sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
                tmpAPDULen = tmpAPDULen + 4

                ListSum = int(data_in[offset + tmpAPDULen], 16)
                output(data_in[offset + tmpAPDULen] + ' —— RCSD，SEQUENCE OF个数=' + str(ListSum))
                tmpAPDULen = tmpAPDULen + 1

                for i in range(0, ListSum):
                    DataResult = data_in[offset + tmpAPDULen]
                    tmpAPDULen = tmpAPDULen + 1
                    if DataResult == '00':
                        output(DataResult + ' —— 第' + str(i + 1) + '列OAD')
                        sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
                        tmpAPDULen = tmpAPDULen + 4
                    else:
                        if DataResult == '01':
                            output(DataResult + ' —— 第' + str(i + 1) + '列ROAD')
                            sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
                            tmpAPDULen = tmpAPDULen + 4

                            ListSum1 = int(data_in[offset + tmpAPDULen], 16)
                            output(data_in[offset + tmpAPDULen] +
                                   ' —— ROAD，SEQUENCE OF个数=' + str(ListSum1))
                            tmpAPDULen = tmpAPDULen + 1
                            for k in range(0, ListSum1):
                                sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
                                tmpAPDULen = tmpAPDULen + 4
                        else:
                            output(data_in[offset + tmpAPDULen] + ' —— RCSD列标识有误')

                DataResult = data_in[offset + tmpAPDULen]
                tmpAPDULen = tmpAPDULen + 1

                if DataResult == '01':
                    output(DataResult + ' —— 记录数据')
                    ListSum2 = int(data_in[offset + tmpAPDULen], 16)
                    output(data_in[offset + tmpAPDULen] + ' —— M条记录，M=' + str(ListSum2))
                    tmpAPDULen = tmpAPDULen + 1

                    tmpLenLen = HandleDateType(tmpAPDULen + offset, ListSum2, ListSum, *data_in)
                    tmpAPDULen = tmpAPDULen + tmpLenLen
                else:
                    if DataResult == '00':
                        output(DataResult + ' —— DAR')
                        sFindErrID(data_in[offset + tmpAPDULen])
                        tmpAPDULen = tmpAPDULen + 1
                    else:
                        output(DataResult + ' —— 报文有误')

        else:
            if FZFlag == '00':
                output(FZFlag + ' —— DAR')
                sFindErrID(data_in[offset + tmpAPDULen])
                tmpAPDULen = tmpAPDULen + 1
            else:
                output(FZFlag + ' —— 报文有误')

    return tmpAPDULen
