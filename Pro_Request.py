from HandleData import sFindDataID, HandleDateType
from shared_functions import *  # NOQA


def Pro0901(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    MaxTime = int(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1], 16)
    output(data_in[offset + tmpAPDULen] + ' ' + data_in[offset +
                                                        tmpAPDULen + 1] + ' —— 整个代理请求的超时时间=' + str(MaxTime) + 's')
    tmpAPDULen = tmpAPDULen + 2

    ListSum = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— SEQUENCE OF个数=' + str(ListSum))
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

        # 超时
        SecSum = int(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1], 16)
        output(data_in[offset + tmpAPDULen] + ' ' + data_in[offset +
                                                            tmpAPDULen + 1] + ' —— 代理一个服务器的超时时间=' + str(SecSum) + 's')
        tmpAPDULen = tmpAPDULen + 2

        ListOADSum = int(data_in[offset + tmpAPDULen], 16)
        output(data_in[offset + tmpAPDULen] + ' —— OAD SEQUENCE OF个数=' + str(ListOADSum))
        tmpAPDULen = tmpAPDULen + 1
        for i in range(0, ListOADSum):
            sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
            tmpAPDULen = tmpAPDULen + 4

    return tmpAPDULen


def Pro0902(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    MaxTime = int(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1], 16)
    output(data_in[offset + tmpAPDULen] + ' ' + data_in[offset +
                                                        tmpAPDULen + 1] + ' —— 代理请求的超时时间=' + str(MaxTime) + 's')
    tmpAPDULen = tmpAPDULen + 2

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

    ChoiceWay = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— RSD， 选择方法' + str(ChoiceWay))
    tmpAPDULen = tmpAPDULen + 1
    # RSD处理

    if ChoiceWay == 1:  # 选择方法1
        sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
        tmpAPDULen = tmpAPDULen + 4

        tmpLenLen = HandleDateType(tmpAPDULen + offset, 1, 1, *data_in)
        tmpAPDULen = tmpAPDULen + tmpLenLen

    if ChoiceWay == 2:  # 选择方法2
        sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
        tmpAPDULen = tmpAPDULen + 4

        tmpLenLen = HandleDateType(tmpAPDULen + offset, 1, 3, *data_in)
        tmpAPDULen = tmpAPDULen + tmpLenLen

    if ChoiceWay == 3:  # 选择方法3
        SumData = int(data_in[offset + tmpAPDULen], 16)
        output(data_in[offset + tmpAPDULen] + ' —— SEQUENCE OF Selector2，个数=' + str(SumData))
        tmpAPDULen = tmpAPDULen + 1
        for k in range(0, SumData):
            sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
            tmpAPDULen = tmpAPDULen + 4

            tmpLenLen = HandleDateType(tmpAPDULen + offset, 1, 3, *data_in)
            tmpAPDULen = tmpAPDULen + tmpLenLen

    if ChoiceWay == 4 or ChoiceWay == 5:  # 选择方法45
        stmpTime = ''
        for k in range(0, 7):
            stmpTime = stmpTime + data_in[offset + tmpAPDULen] + ' '
            tmpAPDULen = tmpAPDULen + 1

        if ChoiceWay == 4:
            output(stmpTime + '—— 采集启动时间')
        else:
            if ChoiceWay == 5:
                output(stmpTime + '—— 采集存储时间')

        tmpLenLen = HandleDateType(tmpAPDULen + offset, 0, 92, *data_in)
        tmpAPDULen = tmpAPDULen + tmpLenLen

    if ChoiceWay == 6 or ChoiceWay == 7 or ChoiceWay == 8:  # 选择方法678
        AtmpText = ';;'.split(';')
        AtmpText[0] = '启动'
        AtmpText[1] = '存储'
        AtmpText[2] = '成功'

        for i in range(0, 2):
            stmpTime = ''
            for k in range(0, 7):
                stmpTime = stmpTime + data_in[offset + tmpAPDULen] + ' '
                tmpAPDULen = tmpAPDULen + 1

            if i == 0:
                output(stmpTime + '—— 采集' + AtmpText[ChoiceWay - 6] + '时间起始值')
            else:
                output(stmpTime + '—— 采集' + AtmpText[ChoiceWay - 6] + '时间结束值')

        output(data_in[offset + tmpAPDULen] + ' ' + data_in[offset +
                                                            tmpAPDULen + 1] + ' ' + data_in[offset + tmpAPDULen + 2] + '—— 间隔')
        tmpAPDULen = tmpAPDULen + 3

        tmpLenLen = HandleDateType(tmpAPDULen + offset, 0, 92, *data_in)
        tmpAPDULen = tmpAPDULen + tmpLenLen

    if ChoiceWay == 9:  # 选择方法9
        SumData = int(data_in[offset + tmpAPDULen], 16)
        output(data_in[offset + tmpAPDULen] + ' —— 上第' + str(SumData) + '次记录')
        tmpAPDULen = tmpAPDULen + 1

    if ChoiceWay == 10:  # 选择方法10
        SumData = int(data_in[offset + tmpAPDULen], 16)
        output(data_in[offset + tmpAPDULen] + ' —— 上' + str(SumData) + '条记录')
        tmpAPDULen = tmpAPDULen + 1

        tmpLenLen = HandleDateType(tmpAPDULen + offset, 0, 92, *data_in)
        tmpAPDULen = tmpAPDULen + tmpLenLen

    # RCSD处理
    SumData = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— RCSD，SEQUENCE OF个数=' + str(SumData))
    tmpAPDULen = tmpAPDULen + 1

    for k in range(0, SumData):
        isOAD = int(data_in[offset + tmpAPDULen], 16)
        if isOAD == 0:
            output(data_in[offset + tmpAPDULen] + ' —— [0] OAD')
            tmpAPDULen = tmpAPDULen + 1
            sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
            tmpAPDULen = tmpAPDULen + 4
        else:
            if isOAD == 1:
                output(data_in[offset + tmpAPDULen] + ' —— [1] ROAD')
                tmpAPDULen = tmpAPDULen + 1
                SumData1 = int(data_in[offset + tmpAPDULen], 16)
                output(data_in[offset + tmpAPDULen] + ' —— ROAD，SEQUENCE OF个数=' + str(SumData1))
                tmpAPDULen = tmpAPDULen + 1
                for k in range(0, SumData1):
                    sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
                    tmpAPDULen = tmpAPDULen + 4
            else:
                output(data_in[offset + tmpAPDULen] + ' —— RCSD错误')

    return tmpAPDULen


def Pro0903(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    MaxTime = int(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1], 16)
    output(data_in[offset + tmpAPDULen] + ' ' + data_in[offset +
                                                        tmpAPDULen + 1] + ' —— 整个代理请求的超时时间=' + str(MaxTime) + 's')
    tmpAPDULen = tmpAPDULen + 2

    ProListSum = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— SEQUENCE OF个数=' + str(ProListSum))
    tmpAPDULen = tmpAPDULen + 1
    for i in range(0, ProListSum):
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

        # 超时
        SecSum = int(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1], 16)
        output(data_in[offset + tmpAPDULen] + ' ' + data_in[offset +
                                                            tmpAPDULen + 1] + ' —— 代理一个服务器的超时时间=' + str(SecSum) + 's')
        tmpAPDULen = tmpAPDULen + 2

        OADSum = int(data_in[offset + tmpAPDULen], 16)
        output(data_in[offset + tmpAPDULen] + ' —— OAD SEQUENCE OF个数=' + str(OADSum))
        tmpAPDULen = tmpAPDULen + 1
        for k in range(0, OADSum):
            sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
            tmpAPDULen = tmpAPDULen + 4

            tmpLenLen = HandleDateType(tmpAPDULen + offset, 1, 1, *data_in)
            tmpAPDULen = tmpAPDULen + tmpLenLen

    return tmpAPDULen


def Pro0904(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    MaxTime = int(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1], 16)
    output(data_in[offset + tmpAPDULen] + ' ' + data_in[offset +
                                                        tmpAPDULen + 1] + ' —— 整个代理请求的超时时间=' + str(MaxTime) + 's')
    tmpAPDULen = tmpAPDULen + 2

    ProListSum = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— SEQUENCE OF个数=' + str(ProListSum))
    tmpAPDULen = tmpAPDULen + 1
    for i in range(0, ProListSum):
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

        # 超时
        SecSum = int(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1], 16)
        output(data_in[offset + tmpAPDULen] + ' ' + data_in[offset +
                                                            tmpAPDULen + 1] + ' —— 代理一个服务器的超时时间=' + str(SecSum) + 's')
        tmpAPDULen = tmpAPDULen + 2

        OADSum = int(data_in[offset + tmpAPDULen], 16)
        output(data_in[offset + tmpAPDULen] + ' —— OAD SEQUENCE OF个数=' + str(OADSum))
        tmpAPDULen = tmpAPDULen + 1
        for k in range(0, OADSum):
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


def Pro0905(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    MaxTime = int(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1], 16)
    output(data_in[offset + tmpAPDULen] + ' ' + data_in[offset +
                                                        tmpAPDULen + 1] + ' —— 整个代理请求的超时时间=' + str(MaxTime) + 's')
    tmpAPDULen = tmpAPDULen + 2

    ProListSum = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— SEQUENCE OF个数=' + str(ProListSum))
    tmpAPDULen = tmpAPDULen + 1
    for i in range(0, ProListSum):
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

        # 超时
        SecSum = int(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1], 16)
        output(data_in[offset + tmpAPDULen] + ' ' + data_in[offset +
                                                            tmpAPDULen + 1] + ' —— 代理一个服务器的超时时间=' + str(SecSum) + 's')
        tmpAPDULen = tmpAPDULen + 2

        OADSum = int(data_in[offset + tmpAPDULen], 16)
        output(data_in[offset + tmpAPDULen] + ' —— OAD SEQUENCE OF个数=' + str(OADSum))
        tmpAPDULen = tmpAPDULen + 1
        for kk in range(0, OADSum):
            sFindDataID(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1])
            tmpAPDULen = tmpAPDULen + 2

            output(data_in[offset + tmpAPDULen] + ' —— 方法标识')
            tmpAPDULen = tmpAPDULen + 1

            output(data_in[offset + tmpAPDULen] + ' —— 操作模式')
            tmpAPDULen = tmpAPDULen + 1

            tmpLenLen = HandleDateType(tmpAPDULen + offset, 1, 1, *data_in)
            tmpAPDULen = tmpAPDULen + tmpLenLen

    return tmpAPDULen


def Pro0906(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    MaxTime = int(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1], 16)
    output(data_in[offset + tmpAPDULen] + ' ' + data_in[offset +
                                                        tmpAPDULen + 1] + ' —— 整个代理请求的超时时间=' + str(MaxTime) + 's')
    tmpAPDULen = tmpAPDULen + 2

    ProListSum = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— SEQUENCE OF个数=' + str(ProListSum))
    tmpAPDULen = tmpAPDULen + 1
    for i in range(0, ProListSum):
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

        # 超时
        SecSum = int(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1], 16)
        output(data_in[offset + tmpAPDULen] + ' ' + data_in[offset +
                                                            tmpAPDULen + 1] + ' —— 代理一个服务器的超时时间=' + str(SecSum) + 's')
        tmpAPDULen = tmpAPDULen + 2

        OADSum = int(data_in[offset + tmpAPDULen], 16)
        output(data_in[offset + tmpAPDULen] + ' —— OAD SEQUENCE OF个数=' + str(OADSum))
        tmpAPDULen = tmpAPDULen + 1
        for kk in range(0, OADSum):
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


def Pro0907(offset, *data_in):
    tmpAPDULen = 0
    output(data_in[offset + tmpAPDULen] + ' —— PIID')
    tmpAPDULen = tmpAPDULen + 1

    sFindDataID(data_in[offset + tmpAPDULen: offset + tmpAPDULen + 4])
    tmpAPDULen = tmpAPDULen + 4

    output(data_in[offset + tmpAPDULen] + ' ' + data_in[offset + tmpAPDULen + 1] + ' ' + data_in[offset + tmpAPDULen +
                                                                                                 2] + ' ' + data_in[offset + tmpAPDULen + 3] + ' ' + data_in[offset + tmpAPDULen + 4] + ' —— 端口通信控制块')
    tmpAPDULen = tmpAPDULen + 5

    SecSum = int(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1], 16)
    output(data_in[offset + tmpAPDULen] + ' ' + data_in[offset +
                                                        tmpAPDULen + 1] + ' —— 接收等待报文超时时间=' + str(SecSum) + 's')
    tmpAPDULen = tmpAPDULen + 2

    SecSum = int(data_in[offset + tmpAPDULen] + data_in[offset + tmpAPDULen + 1], 16)
    output(data_in[offset + tmpAPDULen] + ' ' + data_in[offset +
                                                        tmpAPDULen + 1] + ' —— 接收等待字节超时时间=' + str(SecSum) + 'ms')
    tmpAPDULen = tmpAPDULen + 2

    SumData = int(data_in[offset + tmpAPDULen], 16)
    output(data_in[offset + tmpAPDULen] + ' —— 透明转发命令长度=' + str(SumData))
    tmpAPDULen = tmpAPDULen + 1

    DataText = ''
    for k in range(0, SumData):
        DataText = DataText + data_in[offset + tmpAPDULen] + ' '
        tmpAPDULen = tmpAPDULen + 1
    output(DataText + ' —— 透明转发命令')

    return tmpAPDULen
