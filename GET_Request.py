from HandleData import sFindDataID, HandleDateType
from shared_functions import *


def Get0501(offset,*data_in):
    apdu_len=0
    output(data_in[offset + apdu_len] + ' —— PIID')
    apdu_len += 1
    apdu_len += take_OAD(data_in[offset + apdu_len:])
    return apdu_len


def Get0502(offset,*data_in):
    apdu_len = 0
    output(data_in[offset + apdu_len] + ' —— PIID')
    apdu_len += 1
    oad_count = int(data_in[offset + apdu_len], 16)
    output(data_in[offset + apdu_len] + ' —— OAD*' + str(oad_count))
    apdu_len += 1
    for k in range(0, oad_count):
        apdu_len += take_OAD(data_in[offset + apdu_len:])
    return apdu_len


def Get0503(offset,*data_in):
    apdu_len=0
    output(data_in[offset + apdu_len] + ' —— PIID')
    apdu_len += 1
    sFindDataID(data_in[offset + apdu_len : offset + apdu_len + 4])
    apdu_len += 4
    # RSD
    apdu_len += take_RSD(data_in[offset + apdu_len:])
    
    #RCSD处理
    SumData=int(data_in[offset + apdu_len],16)
    output(data_in[offset + apdu_len] + ' —— RCSD，SEQUENCE OF个数=' + str(SumData))
    apdu_len=apdu_len + 1
    for k in range(0,SumData) :
        isOAD=int(data_in[offset + apdu_len],16)
        if isOAD==0 :
            output(data_in[offset + apdu_len] + ' —— [0] OAD')
            apdu_len=apdu_len + 1
            sFindDataID(data_in[offset + apdu_len : offset + apdu_len + 4])
            apdu_len=apdu_len + 4
        else :
            if isOAD==1 :
                output(data_in[offset + apdu_len] + ' —— [1] ROAD')
                apdu_len=apdu_len + 1

                sFindDataID(data_in[offset + apdu_len : offset + apdu_len + 4])
                apdu_len=apdu_len + 4

                SumData1=int(data_in[offset + apdu_len],16)
                output(data_in[offset + apdu_len] + ' —— ROAD，SEQUENCE OF个数=' + str(SumData1))
                apdu_len=apdu_len + 1
                for k in range(0,SumData1) :
                    sFindDataID(data_in[offset + apdu_len : offset + apdu_len + 4])
                    apdu_len=apdu_len + 4
            else :
                output(data_in[offset + apdu_len] + ' —— RCSD错误')
    return apdu_len



def Get0504(offset,*data_in) :
    apdu_len=0
    output(data_in[offset + apdu_len] + ' —— PIID')
    apdu_len=apdu_len + 1

    SumRecord=int(data_in[offset + apdu_len],16)
    output(data_in[offset + apdu_len] + ' —— 记录型对象个数=' + str(SumRecord))
    apdu_len=apdu_len + 1
    for j in range(0,SumRecord) :
        sFindDataID(data_in[offset + apdu_len : offset + apdu_len + 4])
        apdu_len=apdu_len + 4
        selector=int(data_in[offset + apdu_len],16)
        output(data_in[offset + apdu_len] + ' —— RSD， 选择方法' + str(selector))
        apdu_len=apdu_len + 1
        #RSD处理
        if selector==1 :          #选择方法1
            sFindDataID(data_in[offset + apdu_len : offset + apdu_len + 4])
            apdu_len=apdu_len + 4

            tmpLenLen=HandleDateType(apdu_len + offset,1,1,*data_in)
            apdu_len=apdu_len + tmpLenLen
        if selector==2 :          #选择方法2
            sFindDataID(data_in[offset + apdu_len : offset + apdu_len + 4])
            apdu_len=apdu_len + 4

            tmpLenLen=HandleDateType(apdu_len + offset,1,3,*data_in)
            apdu_len=apdu_len + tmpLenLen
        if selector==3 :          #选择方法3
            SumData=int(data_in[offset + apdu_len],16)
            output(data_in[offset + apdu_len] + ' —— SEQUENCE OF Selector2，个数=' + str(SumData))
            apdu_len=apdu_len + 1
            for k in range(0,SumData) :
                sFindDataID(data_in[offset + apdu_len : offset + apdu_len + 4])
                apdu_len=apdu_len + 4
                tmpLenLen=HandleDateType(apdu_len + offset,1,3,*data_in)
                apdu_len=apdu_len + tmpLenLen
        if selector==4 or selector==5 :          #选择方法45
            stmpTime=''
            for k in range(0,7) :
                stmpTime=stmpTime + data_in[offset + apdu_len] + ' '
                apdu_len=apdu_len + 1
            if selector==4 :
                output(stmpTime + '—— 采集启动时间')
            else :
                if selector==5 :
                    output(stmpTime + '—— 采集存储时间')
            tmpLenLen=HandleDateType(apdu_len + offset,0,92,*data_in)
            apdu_len=apdu_len + tmpLenLen
        if selector==6 or selector==7 or selector==8 :          #选择方法678
            AtmpText=';;'.split(';')
            AtmpText[0]='启动'
            AtmpText[1]='存储'
            AtmpText[2]='成功'
            for i in range(0,2) :
                stmpTime=''
                for k in range(0,7) :
                    stmpTime=stmpTime + data_in[offset + apdu_len] + ' '
                    apdu_len=apdu_len + 1
                if i==0 :
                    output(stmpTime + '—— 采集' + AtmpText[selector-6] + '时间起始值')
                else :
                    output(stmpTime + '—— 采集' + AtmpText[selector-6] + '时间结束值')
            output(data_in[offset + apdu_len] + ' ' + data_in[offset + apdu_len + 1] + ' ' + data_in[offset + apdu_len + 2] + '—— 间隔')
            apdu_len=apdu_len + 3
            tmpLenLen=HandleDateType(apdu_len + offset,0,92,*data_in)
            apdu_len=apdu_len + tmpLenLen
        if selector==9 :          #选择方法9
            SumData=int(data_in[offset + apdu_len],16)
            output(data_in[offset + apdu_len] + ' —— 上第' + str(SumData) + '次记录')
            apdu_len=apdu_len + 1
        if selector==10 :          #选择方法10
            SumData=int(data_in[offset + apdu_len],16)
            output(data_in[offset + apdu_len] + ' —— 上' + str(SumData) + '条记录')
            apdu_len=apdu_len + 1
            tmpLenLen=HandleDateType(apdu_len + offset,0,92,*data_in)
            apdu_len=apdu_len + tmpLenLen
        #RCSD处理
        SumData=int(data_in[offset + apdu_len],16)
        output(data_in[offset + apdu_len] + ' —— RCSD，SEQUENCE OF个数=' + str(SumData))
        apdu_len=apdu_len + 1
        for k in range(0,SumData) :
            isOAD=int(data_in[offset + apdu_len],16)
            if isOAD==0 :
                output(data_in[offset + apdu_len] + ' —— [0] OAD')
                apdu_len=apdu_len + 1
                sFindDataID(data_in[offset + apdu_len : offset + apdu_len + 4])
                apdu_len=apdu_len + 4
            else :
                if isOAD==1 :
                    output(data_in[offset + apdu_len] + ' —— [1] ROAD')
                    apdu_len=apdu_len + 1
                    SumData1=int(data_in[offset + apdu_len],16)
                    output(data_in[offset + apdu_len] + ' —— ROAD，SEQUENCE OF个数=' + str(SumData1))
                    apdu_len=apdu_len + 1
                    for k in range(0,SumData1) :
                        sFindDataID(data_in[offset + apdu_len : offset + apdu_len + 4])
                        apdu_len=apdu_len + 4
                else :
                    output(data_in[offset + apdu_len] + ' —— RCSD错误')
    return apdu_len



def Get0505(offset,*data_in) :
    apdu_len=0
    output(data_in[offset + apdu_len] + ' —— PIID')
    apdu_len=apdu_len + 1
    DataNo=int(data_in[offset + apdu_len] + data_in[offset + apdu_len + 1],16)
    output(data_in[offset + apdu_len] + ' ' + data_in[offset + apdu_len + 1] + ' —— 最近一次数据块序号=' + str(DataNo))
    apdu_len=apdu_len + 2

    return apdu_len
