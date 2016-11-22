import os
from shared_functions import *
from config import pathname


def sFindAPDU( sText ) :
    patternFile = os.path.join(pathname, '698APDUConfig.ini')
    fileHandle = open(patternFile, 'rb')
    file_line_list = fileHandle.readlines()
    fileHandle.close()
    GFLen=len(file_line_list)

    apdu_1 = int(sText,16)
    # print('apdu_1', apdu_1)
    for file_line in file_line_list:
        if int(file_line.decode('utf-8').split('=')[0]) == apdu_1:
            return file_line
    return ''


def sFindDataID(oad):
    patternFile = os.path.join(pathname, '698DataIDConfig.ini')
    fileHandle = open(patternFile, 'rb')
    fileList = fileHandle.readlines()
    fileHandle.close()
    GFLen=len(fileList)

    oad_string = ''
    for temp_byte in oad:
        oad_string += temp_byte
    print('oad_string:', oad_string)

    oad_explain = ''
    for oad_line in fileList:
        if oad_line.decode('utf-8')[0:4] == oad_string[0:4]:
            oad_explain = oad_line.decode('utf-8')[8:].split('=')[0].split('\n')[0]
            break;
    output(oad[0] + ' ' + oad[1] + ' ' + oad[2] + ' ' + oad[3] + ' —— OAD:'+ oad_explain)
    return 0


def sFindErrID( sText ) :
    patternFile = os.path.join(pathname, '698ErrIDConfig.ini')
    fileHandle = open(patternFile, 'rb')
    fileList = fileHandle.readlines()
    fileHandle.close()
    GFLen=len(fileList)
    OI=int(sText,16)
    if OI==255 :
        output(sText+' —— 其它错误')
        return 0
    else :
        #698 err 找标识 20160921
        cc=0
        tt1=0
        tt2=GFLen-1
        for k in range (0,20) :
            if OI>int(fileList[tt1+int((tt2-tt1+1)/2)].decode('utf-8')[0:2]) :
                tt1=tt1+int((tt2-tt1+1)/2)
            else :
                if OI==int(fileList[tt1+int((tt2-tt1+1)/2)].decode('utf-8')[0:2]) :
                    cc=tt1+int((tt2-tt1+1)/2)
                    break
                else :
                    tt2=tt1+int((tt2-tt1+1)/2)
            if (tt2-tt1)<=1 :
                if OI==int(fileList[tt1].decode('utf-8')[0:2]) :
                    cc=tt1
                    break
                else :
                    if OI==int(fileList[tt2].decode('utf-8')[0:2]) :
                        cc=tt2
                        break
                    else :
                        cc=9998
                        break
        if cc != 9998 :
            tmpText=fileList[cc].decode('utf-8')[3:]
            tmpText=tmpText[0:len(tmpText)-1]
            output(sText+' —— '+tmpText)
        return 0


def sFindDataType( sText ) :
    patternFile = os.path.join(pathname, '698DataTypeConfig.ini')
    fileHandle = open(patternFile, 'rb')
    fileList = fileHandle.readlines()
    fileHandle.close()
    GFLen=len(fileList)


    OI=str(int(sText,16))
    if len(OI)<2 :
        OI='0'+OI
    cc=0
    tt1=0
    tt2=GFLen-1
    for k in range (0,20) :
        if OI>fileList[tt1+int((tt2-tt1+1)/2)].decode('utf-8')[0:2] :
            tt1=tt1+int((tt2-tt1+1)/2)
        else :
            if OI==fileList[tt1+int((tt2-tt1+1)/2)].decode('utf-8')[0:2] :
                cc=tt1+int((tt2-tt1+1)/2)
                break
            else :
                tt2=tt1+int((tt2-tt1+1)/2)

        if (tt2-tt1)<=1 :
            if OI==fileList[tt1].decode('utf-8')[0:2] :
                cc=tt1

                break
            else :
                if OI==fileList[tt2].decode('utf-8')[0:2] :
                    cc=tt2

                    break
                else :
                    cc=9998
                    break

    if cc != 9998 :
        tmpText=fileList[cc].decode('utf-8').split('=')[2]
        ltmpText=int(tmpText[0:len(tmpText)-1])
        output(sText+' —— ['+str(int(sText,16))+'] '+fileList[cc].decode('utf-8').split('=')[1])
    else :
        output(sText+' —— ['+str(int(sText,16))+'] 数据类型错误')
        ltmpText=-1

    return ltmpText


def sShowNData(sDataType,sData ) :
    tmpText=''
    if sDataType=='date_time' :
        tmpText=str(int(sData[0:4],16))+'-'+sData[4:6]+'-'+sData[6:8]+' 星期'+sData[8:10]+' '+sData[10:12]+':'+sData[12:14]+':'+sData[14:16]+':'+str(int(sData[16:20],16))

    if sDataType=='date' :
        tmpText=str(int(sData[0:4],16))+'-'+sData[4:6]+'-'+sData[6:8]+' 星期'+sData[8:10]

    if sDataType=='time' :
        tmpText=sData[0:2]+':'+sData[2:4]+':'+sData[4:6]

    if sDataType=='date_time_s' :
        tmpText=str(int(sData[0:4],16))+'-'+sData[4:6]+'-'+sData[6:8]+' '+sData[8:10]+':'+sData[10:12]+':'+sData[12:14]

    return tmpText
