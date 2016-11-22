import os

from shared_functions import *
from sFindIDFun import sFindDataID
from config import pathname

def sFindDataID1( sText ) :
    patternFile = os.path.join(pathname, '698DataIDConfig.ini')
    fileHandle = open(patternFile, 'rb')
    fileList = fileHandle.readlines()
    fileHandle.close()
    GFLen=len(fileList)

    OI=str(sText[0:4])

    #698对象OI找标识 20160921
    cc=0
    tt1=0
    tt2=GFLen-1

    for k in range (0,20) :

        if OI>fileList[tt1+int((tt2-tt1+1)/2)].decode('utf-8')[0:4] :
            tt1=tt1+int((tt2-tt1+1)/2)

        else :
            if OI==fileList[tt1+int((tt2-tt1+1)/2)].decode('utf-8')[0:4] :
                cc=tt1+int((tt2-tt1+1)/2)

                break
            else :
                tt2=tt1+int((tt2-tt1+1)/2)

        if (tt2-tt1)<=1 :
            if OI==fileList[tt1].decode('utf-8')[0:4] :
                cc=tt1

                break
            else :
                if OI==fileList[tt2].decode('utf-8')[0:4] :
                    cc=tt2

                    break
                else :
                    cc=9998
                    break

    if cc != 9998 :
        if fileList[cc].decode('utf-8')[5:7]=='01' :  #电量类
            tmpText=fileList[cc].decode('utf-8')[8:len(fileList[cc])-1]
        else :
            if fileList[cc].decode('utf-8')[5:7]=='02' :  #需量类
                tmpText=fileList[cc].decode('utf-8')[8:len(fileList[cc])-1]
            else :
                tmpText=fileList[cc].decode('utf-8')[8:len(fileList[cc])-1]

    else :
        tmpText=''

    if tmpText.find('=') != -1 :
        tmpText=tmpText.split('=')[0]

    return tmpText

def OADHandle( Num,*Text ):
    TempOI = Text[Num+1]+Text[Num+2]
    tmpText =sFindDataID1( TempOI )
    output(Text[Num+1]+' '+Text[Num+2]+' '+Text[Num+3]+' '+Text[Num+4]+' ——' +tmpText)
    return Num+4

def HandleDate( Num,Sign,Id,*Text ) :
    patternFile = os.path.join(pathname, '698DataTypeConfig.ini')
    fd = open(patternFile, 'rb')
    Dlist =fd.readlines()
    fd.close()

    tt1 =len(Dlist)-1
    OI =str(int(Text[Num],16))

    if len(OI)<2 :
        OI='0'+OI
    if Sign  !=  0:
        for k in range(0,tt1) :
            if (OI == (Dlist[k].decode('utf-8').split('=')[0])) :
                output(Text[Num]+' ——['+Dlist[k].decode('utf-8').split('=')[0]+'] '+Dlist[k].decode('utf-8').split('=')[1]) #show data type
                break
    else :
        OI = Id
        Num -= 1

    OI =int(OI)

    if OI == 0 :
        return Num+1

    elif 1 <= OI <= 2 :
        if OI == 1 :#array
            output(Text[Num+1]+' ——'+str(int(Text[Num+1],16))+"个元素")
        if OI == 2 :   #structure
            output(Text[Num+1]+' ——'+str(int(Text[Num+1],16))+"个成员")
        tNum = Num + 2
        for k in range(0,int(Text[Num+1],16)) :
            tNum=HandleDate( tNum,Sign,Id,*Text )
        return tNum

    elif 3 <= OI <= 28 :
        if OI == 3 :#bool
            output(Text[Num+1]+' ——'+str(int(Text[Num+1],16))+" bool")
            return Num+2

        if OI == 4 :#bit-string
            bit_len = int(Text[Num+1], 16)
            output(Text[Num+1]+' ——bit-string长度:'+str(bit_len)+" bit")
            byte_len = bit_len // 8 if bit_len % 8 == 0 else bit_len // 8 + 1
            bit_string_text = ''
            for k in range(0, byte_len):
                bit_string_text += Text[Num + 2 + k] + ' '
            output(bit_string_text + ' ——bit-stringn内容:' + str(bin(int(bit_string_text.replace(' ', ''), 16))))
            return Num + 2 + byte_len

        if OI == 5 or OI == 6 :#double-long double-long-unsigned
            TempStr = ''
            for k in range(0,4) :
                TempStr = TempStr + Text[Num+1]+ ' '
                Num += 1

            output(TempStr+' ——数据('+str(int(TempStr[9:11],16)+int(TempStr[6:8],16)*256+int(TempStr[3:5],16)*65536+int(TempStr[0:2],16)*16777216)+')')
            return Num + 1

        if OI == 9 : #octet-string
            output(Text[Num+1]+' ——size('+str(int(Text[Num+1],16))+')')
            TempStr = ''
            for k in range(0,int(Text[Num+1],16)) :
                TempStr = TempStr + Text[Num+2]+ ' '
                Num += 1
            output(TempStr+' ——数据')
            return Num + 2

        if OI == 10 : #visible-string
            output(Text[Num+1]+' ——size('+str(int(Text[Num+1],16))+')')
            TempStr = ''
            Tstr = ''
            for k in range(0,int(Text[Num+1],16)) :
                Tstr = Tstr + str(chr(int(Text[Num+2])))+ ' '
                TempStr = TempStr + Text[Num+2]+ ' '
                Num += 1
            output(TempStr+' ——数据(ASCII):'+Tstr)
            return Num + 2

        if OI == 12 : #UTF8-string
            output(Text[Num+1]+" —— 数据")
            return Num+2

        if OI == 15 or OI == 17 :#integer unsigned
            output(Text[Num+1]+" —— 数据("+str(int(Text[Num+1],16))+')')
            return Num+2

        if OI == 16 or OI == 18 :#unsigned long-unsigned
            TempStr = ''
            for k in range(0,2) :
                TempStr = TempStr + Text[Num+1]+ ' '
                Num += 1
            output(TempStr+' ——数据('+str(int(TempStr[3:5],16)+int(TempStr[0:2],16)*256)+')')
            return Num + 1

        if OI == 20 or OI == 21 :#long64 long64-unsigned
            TempStr = ''
            for k in range(0,8) :
                TempStr = TempStr + Text[Num+1]+ ' '
                Num += 1
            output(TempStr+' ——数据('+str(int(TempStr[0:2],16)*16777216*256*256*256*256+int(TempStr[3:5],16)*16777216*256*256*256+int(TempStr[6:8],16)*16777216*256*256+int(TempStr[9:11],16)*16777216*256+int(TempStr[12:14],16)*16777216+int(TempStr[15:17],16)*65536+int(TempStr[18:20],16)*256+int(TempStr[21:23],16))+')')
            return Num + 1

        if OI == 22 :#enum
            TempStr = ''
            for k in range(0,1) :
                TempStr = TempStr + Text[Num+1]+ ' '
                Num += 1
            output(TempStr+' ——数据:('+str(int(TempStr[0:2],16))+')')
            return Num + 1

        if OI == 23 :#float32
            TempStr = ''
            for k in range(0,4) :
                TempStr = TempStr + Text[Num+1]+ ' '
                Num += 1
            output(TempStr+' ——数据('+str(int(TempStr[9:11],16)+int(TempStr[6:8],16)*256+int(TempStr[3:5],16)*65536+int(TempStr[0:2],16)*16777216)+')')
            return Num + 1

        if OI == 24 :#float64
            TempStr = ''
            for k in range(0,8) :
                TempStr = TempStr + Text[Num+1]+ ' '
                Num += 1
            output(TempStr+' ——数据('+str(int(TempStr[0:2],16)*16777216*256*256*256*256+int(TempStr[3:5],16)*16777216*256*256*256+int(TempStr[6:8],16)*16777216*256*256+int(TempStr[9:11],16)*16777216*256+int(TempStr[12:14],16)*16777216+int(TempStr[15:17],16)*65536+int(TempStr[18:20],16)*256+int(TempStr[21:23],16))+')')
            return Num + 1

        if OI == 25 :#date_time
            TempStr = ''
            for k in range(0,10) :
                TempStr = TempStr + Text[Num+1]+ ' '
                Num += 1
            year = str(int(TempStr[0:2])*256 + int(TempStr[3:5],16))
            month = str(int(TempStr[6:8],16))
            day = str(int(TempStr[9:11],16))
            hour = str(int(TempStr[12:14],16))
            fen = str(int(TempStr[15:17],16))
            sec = str(int(TempStr[18:20],16))
            minsec = str(int(TempStr[21:23])*256 + int(TempStr[25:27],16))
            if len(fen) != 2 :
                fen = '0'+fen
            if len(sec) != 2 :
                sec = '0'+sec
            output(TempStr+' ——'+year+'年'+month+'月'+day+'日'+hour+':'+fen+':'+sec+':'+minsec)

            return Num+1

        if OI == 26 :#date
            TempStr = ''
            for k in range(0,5) :
                TempStr = TempStr + Text[Num+1]+ ' '
                Num += 1
            year = str(int(TempStr[0:2])*256 + int(TempStr[3:5],16))
            month = str(int(TempStr[6:8],16))
            day = str(int(TempStr[9:11],16))
            output(TempStr+' ——'+year+'年'+month+'月'+day+'日')
            return Num+1

        if OI == 27 :#time
            TempStr = ''
            for k in range(0,3) :
                TempStr = TempStr + Text[Num+1]+ ' '
                Num += 1
            hour = str(int(TempStr[0:2],16))
            fen = str(int(TempStr[3:5],16))
            sec = str(int(TempStr[6:8],16))
            if len(fen) != 2 :
                fen = '0'+fen
            if len(sec) != 2 :
                sec = '0'+sec
            output(TempStr+' ——'+hour+':'+fen+':'+sec)
            return Num+1

        if OI == 28 :#date_time_s
            TempStr = ''
            for k in range(0,7) :
                TempStr = TempStr + Text[Num+1]+ ' '
                Num += 1

            year = str(int(TempStr[0:2])*256 + int(TempStr[3:5],16))
            month = str(int(TempStr[6:8],16))
            day = str(int(TempStr[9:11],16))
            hour = str(int(TempStr[12:14],16))
            fen = str(int(TempStr[15:17],16))
            sec = str(int(TempStr[18:20],16))
            if len(fen) != 2 :
                fen = '0'+fen
            if len(sec) != 2 :
                sec = '0'+sec
            output(TempStr+' ——'+year+'年'+month+'月'+day+'日'+hour+':'+fen+':'+sec)
            return Num+1

        if OI == 7 or OI == 8 or OI == 13 or OI == 14 or OI == 19 :#remain
            output('错误')
            return -1


    elif 80 <= OI <=96 :
        if OI == 80 :#OI
            TempOI = Text[Num+1]+Text[Num+2]
            tmpText =sFindDataID( TempOI )
            output(TempOI+' ——' +tmpText)
            return Num+5

        if OI == 81 :#OAD
            OADHandle( Num,*Text )
            return Num+5

        if OI == 82 :#ROAD
            OADHandle( Num,*Text )
            Ndata =int(Text[Num+5],16)
            output(Text[Num+5]+' —— 关联对象属性描述符   SEQUENCE OF个数='+str(Ndata))
            Tnum = Num + 5
            for k in range(0,Ndata) :
                OADHandle( Tnum,*Text )
                Tnum += 4
            return Tnum+1

        if OI == 83 :#OMD
            output(Text[Num+1]+' '+Text[Num+2]+' '+Text[Num+3]+' '+Text[Num+4]+' ——OMD')
            return Num+5

        if OI == 84 :#TI
            if Text[Num+1] == '00' :
                output(Text[Num+2]+' ——秒')
            if Text[Num+1] == '01' :
                output(Text[Num+2]+' ——分')
            if Text[Num+1] == '02' :
                output(Text[Num+2]+' ——时')
            if Text[Num+1] == '03' :
                output(Text[Num+2]+' ——日')
            if Text[Num+1] == '04' :
                output(Text[Num+2]+' ——月')
            if Text[Num+1] == '05' :
                output(Text[Num+2]+' ——年')
            output(Text[Num+2]+' '+Text[Num+3]+' ——间隔值')
            return Num+4

        if OI == 85 :#TSA
            Tdata = int(Text[Num+1],16)%16
            output(str(Text[Num+1]) + ' ' + str(Text[Num+2]) + '——TSA长度 ' + str(int(Text[Num+2],16) + 1))
            tsa_data = ''
            for k in range(3, Tdata+2):
                tsa_data  += str(Text[Num + k])+' '
            output(tsa_data + '——TSA内容')
            return Num+Tdata+2

        if OI == 86 :#MAC
            output(Text[Num+1]+' ——MAC的长度')
            Tnum = int(Text[Num+1],16)
            output(str(Text[Num+2:Num+2+Tnum])+' ——MAC')
            return Num+1+Tnum

        if OI == 87 :#RN
            Tnum = int(Text[Num+1],16)
            output(str(Text[Num+1:Num+2+Tnum])+' ——RN数据')
            return Num+Tnum+2

        if OI == 88 :#Region
            if Text[Num+1] == '00' :
                output('('+Text[Num+2]+','+Text[Num+3]+')')
            elif Text[Num+1] == '01' :
                output('['+Text[Num+2]+','+Text[Num+3]+')')
            elif Text[Num+1] == '02' :
                output('('+Text[Num+2]+','+Text[Num+3]+']')
            elif Text[Num+1] == '03' :
                output('['+Text[Num+2]+','+Text[Num+3]+']')
            return Num+4

        if OI == 89 :#Scaler_Unit

            return -1

        if OI == 91 :#CSD
            if Text[Num+1] == '00' :
                output(Text[Num+1]+' ——OAD')
                OADHandle( Num+1,*Text )
                return Num+6
            else :
                output(Text[Num+1]+' ——ROAD')
                OADHandle( Num+1,*Text )
                Ndata =int(Text[Num+6],16)
                output(Text[Num+6]+' —— 关联对象属性描述符   SEQUENCE OF个数='+str(Ndata))
                Tnum = Num + 6
                for k in range(0,Ndata) :
                    OADHandle( Tnum,*Text )
                    Tnum += 4
                return Tnum+1

        if OI == 90 :#RSD
            if Text[Num+1] == '00' :
                output(Text[Num+1]+' ——NULL（不选择）')
                return Num+2

            if Text[Num+1] == '01' :
                output(Text[Num+1]+' ——方法一')
                Tnum = OADHandle(Num+1,*Text)
                Tnum = HandleDate(Tnum,1,1,*Text)
                return Tnum

            if Text[Num+1] == '02' :
                output(Text[Num+1]+' ——方法二')
                Tnum = OADHandle(Num+1,*Text)
                Tnum = HandleDate(Tnum,1,1,*Text)
                Tnum = HandleDate(Tnum,1,1,*Text)
                Tnum = HandleDate(Tnum,1,1,*Text)
                return Tnum

            if Text[Num+1] == '03' :
                output(Text[Num+1]+' ——方法三')

                Tlen = int(Text[Num+2],16)
                output(Text[Num+2]+'SEQUENCE OF 方法二的个数 ='+str(Tlen))
                Tnum = Num+2
                for k in range(0,Tlen):
                    Tnum = OADHandle(Tnum,*Text)
                    Tnum = HandleDate(Tnum,1,1,*Text)
                    Tnum = HandleDate(Tnum,1,1,*Text)
                    Tnum = HandleDate(Tnum,1,1,*Text)
                    Tnum -= 1
                return Tnum+Tlen-1

            if Text[Num+1] == '04' :
                output(Text[Num+1]+' ——方法四')
                Tnum = Num + 2
                Tnum = HandleDate(Tnum,0,28,*Text)
                Tnum = HandleDate(Tnum,0,92,*Text)
                return Tnum

            if Text[Num+1] == '05' :
                output(Text[Num+1]+' ——方法五')
                Tnum = Num + 2
                Tnum = HandleDate(Tnum,0,28,*Text)
                Tnum = HandleDate(Tnum,0,92,*Text)
                return Tnum

            if Text[Num+1] == '06' :
                output(Text[Num+1]+' ——方法六')
                Tnum = Num + 2
                Tnum = HandleDate(Tnum,0,28,*Text)#data_times
                Tnum = HandleDate(Tnum,0,28,*Text)
                Tnum = HandleDate(Tnum,0,84,*Text)#TI
                Tnum = HandleDate(Tnum,0,92,*Text)#MS
                return Tnum

            if Text[Num+1] == '07' :
                output(Text[Num+1]+' ——方法七')
                Tnum = Num + 2
                Tnum = HandleDate(Tnum,0,28,*Text)#data_times
                Tnum = HandleDate(Tnum,0,28,*Text)
                Tnum = HandleDate(Tnum,0,84,*Text)#TI
                Tnum = HandleDate(Tnum,0,92,*Text)#MS
                return Tnum

            if Text[Num+1] == '08' :
                output(Text[Num+1]+' ——方法八')
                Tnum = Num + 2
                Tnum = HandleDate(Tnum,0,28,*Text)#data_times
                Tnum = HandleDate(Tnum,0,28,*Text)
                Tnum = HandleDate(Tnum,0,84,*Text)#TI
                Tnum = HandleDate(Tnum,0,92,*Text)#MS
                return Tnum

            if Text[Num+1] == '09' :
                output(Text[Num+1]+' ——方法九')
                Tnum = Num + 2
                Tnum = HandleDate(Tnum,0,16,*Text)
                return Tnum

            if Text[Num+1] == '0A' :
                output(Text[Num+1]+' ——方法十')
                Tnum = Num + 2
                Tnum = HandleDate(Tnum,0,16,*Text)
                Tnum = HandleDate(Tnum,0,92,*Text)#MS
                return Tnum

        if OI == 92 :#MS
            if Text[Num+1] == '00' :
                output(Text[Num+1]+' —— 无电能表')
                return Num+2

            if Text[Num+1] == '01' :
                output(Text[Num+1]+' —— 全部用户地址')
                return Num+2

            if Text[Num+1] == '02' :#unsigned
                tNum = int(Text[Num+2],16)
                output(Text[Num+1]+' —— 一组用户类型')
                output(Text[Num+2]+' —— SEQUENCE OF unsigned的个数 = '+str(int(Text[Num+2],16)))
                Tnum = Num + 3
                for k in range(0,tNum) :
                    output(Text[Tnum]+' —— 一组用户类型'+str(k+1))
                    Tnum += 1
                return Tnum

            if Text[Num+1] == '03' :#TSA
                tNum = int(Text[Num+2],16)
                output(Text[Num+1]+' ——TSA')
                output(Text[Num+2]+' —— SEQUENCE OF TSA的个数 = '+str(tNum))
                Tnum = Num + 3
                for k in range(0,tNum) :
                    Tdata = int(Text[Tnum],16)%16
                    output(str(Text[Tnum:Tnum+Tdata+1])+' —— TSA'+str(k+1))
                    Tnum = Tnum+Tdata+1
                return Tnum

            if Text[Num+1] == '04' :#long-unsigned
                tNum = int(Text[Num+2],16)
                output(Text[Num+1]+' ——一组配置序号')
                output(Text[Num+2]+' —— SEQUENCE OF long-unsigned的个数 = '+str(int(Text[Num+2],16)))
                Tnum = Num + 3
                for k in range(0,tNum) :
                    output(Text[Tnum]+' '+ Text[Tnum+1]+'—— 一组配置序号'+str(k+1))
                    Tnum += 2
                return Tnum

            if Text[Num+1] == '05' :#Region
                tNum = int(Text[Num+2],16)
                output(Text[Num+1]+' ——一组用户类型区间')
                output(Text[Num+2]+' —— SEQUENCE OF Region的个数 = '+str(int(Text[Num+2],16)))
                Tnum = Num + 3
                for k in range(0,tNum) :
                    if Text[Tnum+1] == '0B' and Text[Tnum+3] == '0B' :#unsigned
                        Str1 = str(int(Text[Tnum+2],16))
                        Str2 = str(int(Text[Tnum+4],16))
                        Tstr = Text[Tnum+2]+' '+Text[Tnum+4]
                        if Text[Tnum] == '00' :
                            output(Text[Tnum]+' ——( )')
                            Str =( Tstr+' ——('+Str1+','+Str2+')')
                        elif Text[Tnum] == '01' :
                            output(Text[Tnum]+' ——[ )')
                            Str = (Tstr+'——['+Str1+','+Str2+')')
                        elif Text[Tnum] == '02' :
                            output(Text[Tnum]+' ——( ]')
                            Str = (Tstr+'——('+Str1+','+Str2+']')
                        elif Text[Tnum] == '03' :
                            output(Text[Tnum]+' ——[ ]')
                            Str = (Tstr+'——['+Str1+','+Str2+']')
                        output(Text[Tnum+1]+' ——[11]unsigned')
                        Tnum += 5
                        output(Str+' —— 一组用户类型区间'+str(k+1))
                return Tnum

            if Text[Num+1] == '06' :#Region
                tNum = int(Text[Num+2],16)
                output(Text[Num+1]+' ——一组用户地址区间')
                output(Text[Num+2]+' —— SEQUENCE OF Region的个数 = '+str(int(Text[Num+2],16)))
                Tnum = Num + 3
                for k in range(0,tNum) :
                    order = Tnum
                    if Text[Tnum+1] == '55' :#TSA
                        TempNum = int(Text[Tnum+2],16)
                        Str1 = Text[Tnum+2]
                        for j in range(0,TempNum) :
                            Str1 =  Str1+ ' ' + Text[Tnum+3]
                            Tnum += 1
                        Tnum = Tnum + 3
                    if Text[Tnum] == '55' :#TSA
                        TempNum = int(Text[Tnum+1],16)
                        Str2 = Text[Tnum+1]
                        for j in range(0,TempNum) :
                            Str2 =  Str2 + ' '+ Text[Tnum+2]
                            Tnum += 1
                        Tnum = Tnum + 2

                        if Text[order] == '00' :
                            output(Text[order]+' ——( )')
                            Str = (Str1+' '+Str2+' ——('+Str1+','+Str2+')')
                        elif Text[order] == '01' :
                            Str = (Str1+' '+Str2+' ——['+Str1+','+Str2+')')
                            output(Text[order]+' ——[ )')
                        elif Text[order] == '02' :
                            Str = (Str1+' '+Str2+' ——('+Str1+','+Str2+']')
                            output(Text[order]+' ——( ]')
                        elif Text[order] == '03' :
                            Str = (Str1+' '+Str2+' ——['+Str1+','+Str2+']')
                            output(Text[order]+' ——[ ]')
                    output(Text[order+1]+' ——[85]TSA')
                    output(Str+' —— TSA'+str(k+1))
                return Tnum

            if Text[Num+1] == '07' :#Region
                tNum = int(Text[Num+2],16)
                output(Text[Num+1]+' ——一组配置序号区间')
                output(Text[Num+2]+' —— SEQUENCE OF Region的个数 = '+str(int(Text[Num+2],16)))
                Tnum = Num + 3
                for k in range(0,tNum) :
                    if Text[Tnum+1] == '0C' and Text[Tnum+4] == '0C' :#long_unsigned
                        Str1 = str(int((Text[Tnum+2]+Text[Tnum+3]),16))
                        Str2 = str(int((Text[Tnum+5]+Text[Tnum+6]),16))
                        Tstr =Text[Tnum+2]+' '+Text[Tnum+3]+' '+Text[Tnum+5]+' '+Text[Tnum+6]
                        if Text[Tnum] == '00' :
                            output(Text[Tnum]+' ——( )')
                            Str =( Tstr+' ——('+Str1+','+Str2+')')
                        elif Text[Tnum] == '01' :
                            output(Text[Tnum]+' ——[ )')
                            Str = (Tstr+' ——['+Str1+','+Str2+')')
                        elif Text[Tnum] == '02' :
                            output(Text[Tnum]+' ——( ]')
                            Str = (Tstr+' ——('+Str1+','+Str2+']')
                        elif Text[Tnum] == '03' :
                            output(Text[Tnum]+' ——[ ]')
                            Str = (Tstr+' ——['+Str1+','+Str2+']')
                        output(Text[Tnum+1]+' ——[12]long——unsigned')
                        Tnum += 7
                        output(Str+' —— 一组配置序号区间'+str(k+1))
                return Tnum


        if OI == 93 :#SID

            return -1

        if OI == 94 :#SID_MAC

            return -1

        if OI == 95 :#COMDCB

            return -1

        if OI == 96 :
            output('60 ——[96]RCSD')
            output(Text[Num+1]+' ——  SEQUENCE OF CSD个数='+str(int(Text[Num+1],16)))
            tNum = Num+2
            for k in range(0,int(Text[Num+1],16)) :
                if Text[tNum] == '00' :
                    output(Text[tNum]+' ——OAD')
                    OADHandle( tNum,*Text )
                    tNum += 4
                else :
                    output(Text[tNum]+' ——ROAD')
                    OADHandle( tNum,*Text )
                    tNum = tNum + 5
                    Ndata =int(Text[tNum],16)
                    output(Text[tNum]+' —— 关联对象属性描述符   SEQUENCE OF个数='+str(Ndata))
                    for k in range(0,Ndata) :
                        OADHandle( tNum,*Text )
                        tNum += 4
                tNum += 1
            return tNum



def HandleDateType( Num,Line,Column,*Text ) :
    Tempnum = Num
    if Line == 0 :
        Tempnum = HandleDate( Tempnum,Line,Column,*Text )
    else :
        output(' ')
        for k in range(0,Line):
            for j in range(0,Column):
                Tempnum = HandleDate( Tempnum,Line,Column,*Text )
            output(' ')
    return Tempnum-Num
