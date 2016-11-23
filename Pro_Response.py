from HandleData import sFindDataID, HandleDateType
from sFindIDFun import sFindErrID
from shared_functions import *  # NOQA


def Pro8901(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    ListSum = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— 代理服务器 SEQUENCE OF个数=' + str(ListSum))
    tmpAPDULen = tmpAPDULen + 1
    for i in range(0, ListSum):
        # 一个目录服务地址
        LenServerAddr = int(int(data_in[offset + tmpAPDULen], 16) % 8)
        StaServerAddr = int(int(data_in[offset + tmpAPDULen], 16) / 64)
        sAddr = data_in[offset + tmpAPDULen]
        tmpAPDULen = tmpAPDULen + 1

        ServerAddr = ''
        if StaServerAddr == 0:
            ServerAddr = ServerAddr + '单地址 '
        else:
            if StaServerAddr == 1:
                ServerAddr = ServerAddr + '通配地址 '
            else:
                if StaServerAddr == 2:
                    ServerAddr = ServerAddr + '组地址 '
                else:
                    if StaServerAddr == 3:
                        ServerAddr = ServerAddr + '广播地址 '

        for k in range(0, LenServerAddr):
            ServerAddr = ServerAddr + data_in[offset + tmpAPDULen]
            sAddr = sAddr + ' ' + data_in[offset + tmpAPDULen]
            tmpAPDULen = tmpAPDULen + 1
        if ServerAddr[len(ServerAddr) - 1:len(ServerAddr)] == 'F':
            ServerAddr = ServerAddr[0:len(ServerAddr) - 1]
        output(sAddr + ' —— TSA ' + ServerAddr)

        # 若干个对象属性描述符及其结果
        ListSum1 = int(data_in[offset + tmpAPDULen], 16)
        output(data_in[offset + tmpAPDULen] + ' —— 对象属性 SEQUENCE OF个数=' + str(ListSum1))
        tmpAPDULen = tmpAPDULen + 1
        for j in range(0, ListSum1):

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


def Pro8902(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    # 一个目录服务地址
    LenServerAddr = int(int(data_in[offset + tmpAPDULen], 16) % 8)
    StaServerAddr = int(int(data_in[offset + tmpAPDULen], 16) / 64)
    sAddr = data_in[offset + tmpAPDULen]
    tmpAPDULen = tmpAPDULen + 1

    ServerAddr = ''
    if StaServerAddr == 0:
        ServerAddr = ServerAddr + '单地址 '
    else:
        if StaServerAddr == 1:
            ServerAddr = ServerAddr + '通配地址 '
        else:
            if StaServerAddr == 2:
                ServerAddr = ServerAddr + '组地址 '
            else:
                if StaServerAddr == 3:
                    ServerAddr = ServerAddr + '广播地址 '

    for k in range(0, LenServerAddr):
        ServerAddr = ServerAddr + data_in[offset + tmpAPDULen]
        sAddr = sAddr + ' ' + data_in[offset + tmpAPDULen]
        tmpAPDULen = tmpAPDULen + 1
    if ServerAddr[len(ServerAddr) - 1:len(ServerAddr)] == 'F':
        ServerAddr = ServerAddr[0:len(ServerAddr) - 1]
    output(sAddr + ' —— TSA ' + ServerAddr)

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


def Pro8903(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    ListSum = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— 代理服务器 SEQUENCE OF个数=' + str(ListSum))
    tmpAPDULen = tmpAPDULen + 1
    for i in range(0, ListSum):
        # 一个目录服务地址
        LenServerAddr = int(int(data_in[offset + tmpAPDULen], 16) % 8)
        StaServerAddr = int(int(data_in[offset + tmpAPDULen], 16) / 64)
        sAddr = data_in[offset + tmpAPDULen]
        tmpAPDULen = tmpAPDULen + 1

        ServerAddr = ''
        if StaServerAddr == 0:
            ServerAddr = ServerAddr + '单地址 '
        else:
            if StaServerAddr == 1:
                ServerAddr = ServerAddr + '通配地址 '
            else:
                if StaServerAddr == 2:
                    ServerAddr = ServerAddr + '组地址 '
                else:
                    if StaServerAddr == 3:
                        ServerAddr = ServerAddr + '广播地址 '

        for k in range(0, LenServerAddr):
            ServerAddr = ServerAddr + data_in[offset + tmpAPDULen]
            sAddr = sAddr + ' ' + data_in[offset + tmpAPDULen]
            tmpAPDULen = tmpAPDULen + 1
        if ServerAddr[len(ServerAddr) - 1:len(ServerAddr)] == 'F':
            ServerAddr = ServerAddr[0:len(ServerAddr) - 1]
        output(sAddr + ' —— TSA ' + ServerAddr)

        # 若干个对象属性描述符及其结果
        ListSum1 = int(data_in[offset + tmpAPDULen], 16)
        output(data_in[offset + tmpAPDULen] + ' —— 对象属性 SEQUENCE OF个数=' + str(ListSum1))
        tmpAPDULen = tmpAPDULen + 1
        for j in range(0, ListSum1):
            sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
            tmpAPDULen = tmpAPDULen + 4

            sFindErrID(data_in[offset + tmpAPDULen])
            tmpAPDULen = tmpAPDULen + 1

    return tmpAPDULen


def Pro8904(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    ListSum = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— 代理服务器 SEQUENCE OF个数=' + str(ListSum))
    tmpAPDULen = tmpAPDULen + 1
    for i in range(0, ListSum):
        # 一个目录服务地址
        LenServerAddr = int(int(data_in[offset + tmpAPDULen], 16) % 8)
        StaServerAddr = int(int(data_in[offset + tmpAPDULen], 16) / 64)
        sAddr = data_in[offset + tmpAPDULen]
        tmpAPDULen = tmpAPDULen + 1

        ServerAddr = ''
        if StaServerAddr == 0:
            ServerAddr = ServerAddr + '单地址 '
        else:
            if StaServerAddr == 1:
                ServerAddr = ServerAddr + '通配地址 '
            else:
                if StaServerAddr == 2:
                    ServerAddr = ServerAddr + '组地址 '
                else:
                    if StaServerAddr == 3:
                        ServerAddr = ServerAddr + '广播地址 '

        for k in range(0, LenServerAddr):
            ServerAddr = ServerAddr + data_in[offset + tmpAPDULen]
            sAddr = sAddr + ' ' + data_in[offset + tmpAPDULen]
            tmpAPDULen = tmpAPDULen + 1
        if ServerAddr[len(ServerAddr) - 1:len(ServerAddr)] == 'F':
            ServerAddr = ServerAddr[0:len(ServerAddr) - 1]
        output(sAddr + ' —— TSA ' + ServerAddr)

        # 若干个对象属性描述符及其结果
        ListSum1 = int(data_in[offset + tmpAPDULen], 16)
        output(data_in[offset + tmpAPDULen] + ' —— 对象属性 SEQUENCE OF个数=' + str(ListSum1))
        tmpAPDULen = tmpAPDULen + 1
        for j in range(0, ListSum1):
            sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
            tmpAPDULen = tmpAPDULen + 4

            sFindErrID(data_in[offset + tmpAPDULen])
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


def Pro8905(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    ListSum = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— 代理服务器 SEQUENCE OF个数=' + str(ListSum))
    tmpAPDULen = tmpAPDULen + 1
    for i in range(0, ListSum):
        # 一个目录服务地址
        LenServerAddr = int(int(data_in[offset + tmpAPDULen], 16) % 8)
        StaServerAddr = int(int(data_in[offset + tmpAPDULen], 16) / 64)
        sAddr = data_in[offset + tmpAPDULen]
        tmpAPDULen = tmpAPDULen + 1

        ServerAddr = ''
        if StaServerAddr == 0:
            ServerAddr = ServerAddr + '单地址 '
        else:
            if StaServerAddr == 1:
                ServerAddr = ServerAddr + '通配地址 '
            else:
                if StaServerAddr == 2:
                    ServerAddr = ServerAddr + '组地址 '
                else:
                    if StaServerAddr == 3:
                        ServerAddr = ServerAddr + '广播地址 '

        for k in range(0, LenServerAddr):
            ServerAddr = ServerAddr + data_in[offset + tmpAPDULen]
            sAddr = sAddr + ' ' + data_in[offset + tmpAPDULen]
            tmpAPDULen = tmpAPDULen + 1
        if ServerAddr[len(ServerAddr) - 1:len(ServerAddr)] == 'F':
            ServerAddr = ServerAddr[0:len(ServerAddr) - 1]
        output(sAddr + ' —— TSA ' + ServerAddr)

        # 若干个对象属性描述符及其结果
        ListSum1 = int(data_in[offset + tmpAPDULen], 16)
        output(data_in[offset + tmpAPDULen] + ' —— 对象属性 SEQUENCE OF个数=' + str(ListSum1))
        tmpAPDULen = tmpAPDULen + 1
        for j in range(0, ListSum1):
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


def Pro8906(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    ListSum = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— 代理服务器 SEQUENCE OF个数=' + str(ListSum))
    tmpAPDULen = tmpAPDULen + 1
    for i in range(0, ListSum):
        # 一个目录服务地址
        LenServerAddr = int(int(data_in[offset + tmpAPDULen], 16) % 8)
        StaServerAddr = int(int(data_in[offset + tmpAPDULen], 16) / 64)
        sAddr = data_in[offset + tmpAPDULen]
        tmpAPDULen = tmpAPDULen + 1

        ServerAddr = ''
        if StaServerAddr == 0:
            ServerAddr = ServerAddr + '单地址 '
        else:
            if StaServerAddr == 1:
                ServerAddr = ServerAddr + '通配地址 '
            else:
                if StaServerAddr == 2:
                    ServerAddr = ServerAddr + '组地址 '
                else:
                    if StaServerAddr == 3:
                        ServerAddr = ServerAddr + '广播地址 '

        for k in range(0, LenServerAddr):
            ServerAddr = ServerAddr + data_in[offset + tmpAPDULen]
            sAddr = sAddr + ' ' + data_in[offset + tmpAPDULen]
            tmpAPDULen = tmpAPDULen + 1
        if ServerAddr[len(ServerAddr) - 1:len(ServerAddr)] == 'F':
            ServerAddr = ServerAddr[0:len(ServerAddr) - 1]
        output(sAddr + ' —— TSA ' + ServerAddr)

        # 若干个对象属性描述符及其结果
        ListSum1 = int(data_in[offset + tmpAPDULen], 16)
        output(data_in[offset + tmpAPDULen] + ' —— 对象属性 SEQUENCE OF个数=' + str(ListSum1))
        tmpAPDULen = tmpAPDULen + 1
        for j in range(0, ListSum1):
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


def Pro8907(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
    tmpAPDULen = tmpAPDULen + 4

    DataResult = data_in[offset + tmpAPDULen]
    tmpAPDULen = tmpAPDULen + 1
    if DataResult == '01':  # octet-string
        output(DataResult + ' —— octet-string')

        SumData = int(data_in[offset + tmpAPDULen], 16)
        output(data_in[offset + tmpAPDULen] + ' —— 透传返回命令长度=' + str(SumData))
        tmpAPDULen = tmpAPDULen + 1

        DataText = ''
        for k in range(0, SumData):
            DataText = DataText + data_in[offset + tmpAPDULen] + ' '
            tmpAPDULen = tmpAPDULen + 1
        output(DataText + ' —— 透传返回命令')

    else:
        if DataResult == '00':
            output(DataResult + ' —— DAR')
            sFindErrID(data_in[offset + tmpAPDULen])
            tmpAPDULen = tmpAPDULen + 1
        else:
            output(DataResult + ' —— 报文有误')

    return tmpAPDULen
