from sFindIDFun import sFindErrID
from shared_functions import *


def security_response(offset,*data_in) :
    apdu_len = 0
    try:
        encryption_type = {
            '00' : ' —— 明文应用数据单元',
            '01' : ' —— 密文应用数据单元'
        }[int(data_in[offset + apdu_len], 16)]
        output(data_in[offset + apdu_len] + encryption_type)
    except:
        print('encryption_type', data_in[offset+apdu_len])
        sFindErrID(data_in[offset + apdu_len])
    apdu_len += 1

    apdu_content_len = int(data_in[offset+apdu_len], 16)
    output(data_in[offset+apdu_len]+' —— 应用数据长度:'+str(apdu_content_len))
    apdu_len += 1
    apdu_content_text = ''
    for k in range(0,apdu_content_len) :
        apdu_content_text += data_in[offset + apdu_len + k] + ' '
    apdu_len += apdu_content_len
    output(apdu_content_text + '—— 应用数据单元')

    optional_message = data_in[offset + apdu_len]
    if optional_message == 0:
        output(data_in[offset + apdu_len]+' —— 不含数据验证信息')
        apdu_len += 1
        return apdu_len

    output(data_in[offset + apdu_len]+' —— 含数据验证信息')
    apdu_len += 1
    mac_len = int(data_in[offset + apdu_len + 1], 16)
    print('mac_len', mac_len)
    output(data_in[offset + apdu_len] + ' ' + data_in[offset + apdu_len + 1] + ' —— 数据MAC, 长度' + str(mac_len))
    apdu_len += 2
    mac_text = ''
    for k in range(0, mac_len) :
        mac_text += data_in[offset + apdu_len + k] + ' '
    apdu_len += mac_len
    output(mac_text + '—— MAC数据')
    return apdu_len



def security_request(offset,*data_in) :
    apdu_len=0
    PDUnit=int(data_in[offset+apdu_len],16)
    if PDUnit==0 :
        output(data_in[offset+apdu_len]+' —— 明文应用数据单元   [0]')
    else :
        if PDUnit==1 :
            output(data_in[offset+apdu_len]+' —— 密文应用数据单元   [1]')
    apdu_len=apdu_len+1
    SumData1=int(data_in[offset+apdu_len],16)
    output(data_in[offset+apdu_len]+' —— 字串个数='+str(SumData1))
    apdu_len=apdu_len+1
    txtData=''
    for k in range(0,SumData1) :
        txtData=txtData+data_in[offset+apdu_len]+' '
        apdu_len=apdu_len+1
    output(txtData+'—— 应用数据单元数据')
    PDUnit=int(data_in[offset+apdu_len],16)
    if PDUnit==0 :
        output(data_in[offset+apdu_len]+' —— 数据验证码 SID_MAC  [0]')
        apdu_len=apdu_len+1
        output(data_in[offset+apdu_len]+' '+data_in[offset+apdu_len+1]+' '+data_in[offset+apdu_len+2]+' '+data_in[offset+apdu_len+3]+' —— SID标识')
        apdu_len=apdu_len+4
        SumData1=int(data_in[offset+apdu_len],16)
        output(data_in[offset+apdu_len]+' —— 附加数据长度='+str(SumData1))
        apdu_len=apdu_len+1
        txtData=''
        for k in range(0,SumData1) :
            txtData=txtData+data_in[offset+apdu_len]+' '
            apdu_len=apdu_len+1
        output(txtData+'—— 附加数据')
        SumData1=int(data_in[offset+apdu_len],16)
        output(data_in[offset+apdu_len]+' —— MAC长度='+str(SumData1))
        apdu_len=apdu_len+1
        txtData=''
        for k in range(0,SumData1) :
            txtData=txtData+data_in[offset+apdu_len]+' '
            apdu_len=apdu_len+1
        output(txtData+'—— MAC数据')
    else :
        if PDUnit==1 :
            output(data_in[offset+apdu_len]+' —— 随机数RN          [1]')
            apdu_len=apdu_len+1
            SumData1=int(data_in[offset+apdu_len],16)
            output(data_in[offset+apdu_len]+' —— 随机数长度='+str(SumData1))
            apdu_len=apdu_len+1
            txtData=''
            for k in range(0,SumData1) :
                txtData=txtData+data_in[offset+apdu_len]+' '
                apdu_len=apdu_len+1
            output(txtData+'—— 随机数')
        else :
            if PDUnit==2 :
                output(data_in[offset+apdu_len]+' —— 随机数+数据MAC  [2]')
                apdu_len=apdu_len+1
                SumData1=int(data_in[offset+apdu_len],16)
                output(data_in[offset+apdu_len]+' —— 随机数长度='+str(SumData1))
                apdu_len=apdu_len+1
                txtData=''
                for k in range(0,SumData1) :
                    txtData=txtData+data_in[offset+apdu_len]+' '
                    apdu_len=apdu_len+1
                output(txtData+'—— 随机数')
                SumData1=int(data_in[offset+apdu_len],16)
                output(data_in[offset+apdu_len]+' —— MAC长度='+str(SumData1))
                apdu_len=apdu_len+1
                txtData=''
                for k in range(0,SumData1) :
                    txtData=txtData+data_in[offset+apdu_len]+' '
                    apdu_len=apdu_len+1
                output(txtData+'—— MAC数据')
            else :
                if PDUnit==3 :
                    output(data_in[offset+apdu_len]+' —— 安全标识 SID       [3]')
                    apdu_len=apdu_len+1
                    output(data_in[offset+apdu_len]+' '+data_in[offset+apdu_len+1]+' '+data_in[offset+apdu_len+2]+' '+data_in[offset+apdu_len+3]+' —— SID标识')
                    apdu_len=apdu_len+4
                    SumData1=int(data_in[offset+apdu_len],16)
                    output(data_in[offset+apdu_len]+' —— 附加数据长度='+str(SumData1))
                    apdu_len=apdu_len+1
                    txtData=''
                    for k in range(0,SumData1) :
                        txtData=txtData+data_in[offset+apdu_len]+' '
                        apdu_len=apdu_len+1
                    output(txtData+'—— 附加数据')
    apdu_len=apdu_len+1
    return apdu_len
