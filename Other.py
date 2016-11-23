from shared_functions import *
from shared_functions import take_date_time


def link_request(offset, *data_in):
    apdu_len = 2
    try:
        link_type = {
            '00': ' —— 登录',
            '01': ' —— 心跳',
            '02': ' —— 退出登录'
        }[data_in[offset + apdu_len]]
        output(data_in[offset + apdu_len] + link_type)
    except:
        output(data_in[offset + apdu_len] + ' —— 报文有误')

    apdu_len += 1
    cycle_time = str(int(data_in[offset + apdu_len] + data_in[offset + apdu_len + 1], 16))
    output(data_in[offset + apdu_len] + ' ' + data_in[offset +
                                                      apdu_len + 1] + ' —— 心跳周期:' + cycle_time + 's')
    apdu_len += 2
    apdu_len += take_date_time(data_in[offset + apdu_len: offset + apdu_len + 10], '(请求时间)')
    return apdu_len


def connect_request(offset, *data_in):
    apdu_len = 2
    output(data_in[offset + apdu_len] + ' ' + data_in[offset + apdu_len + 1] + ' —— 期望的应用层协议版本号')
    apdu_len += 2
    DataText = ''
    for k in range(0, 8):
        DataText = DataText + data_in[offset + apdu_len] + ' '
        apdu_len = apdu_len + 1
    output(DataText + ' —— 期望的协议一致性块')
    DataText = ''
    for k in range(0, 16):
        DataText = DataText + data_in[offset + apdu_len] + ' '
        apdu_len = apdu_len + 1
    output(DataText + ' —— 期望的功能一致性块')
    stXinTiao = str(int(data_in[offset + apdu_len] + data_in[offset + apdu_len + 1], 16))
    output(data_in[offset + apdu_len] + ' ' + data_in[offset +
                                                      apdu_len + 1] + ' —— 客户机发送帧最大尺寸:' + stXinTiao + '字节')
    apdu_len = apdu_len + 2
    stXinTiao = str(int(data_in[offset + apdu_len] + data_in[offset + apdu_len + 1], 16))
    output(data_in[offset + apdu_len] + ' ' + data_in[offset +
                                                      apdu_len + 1] + ' —— 客户机接收帧最大尺寸:' + stXinTiao + '字节')
    apdu_len = apdu_len + 2
    stXinTiao = str(int(data_in[offset + apdu_len], 16))
    output(data_in[offset + apdu_len] + ' —— 客户机接收帧最大窗口尺寸:' + stXinTiao + '个')
    apdu_len = apdu_len + 1
    stXinTiao = str(int(data_in[offset + apdu_len] + data_in[offset + apdu_len + 1], 16))
    output(data_in[offset + apdu_len] + ' ' + data_in[offset +
                                                      apdu_len + 1] + ' —— 客户机最大可处理APDU尺寸:' + stXinTiao)
    apdu_len = apdu_len + 2
    stXinTiao = str(int(data_in[offset + apdu_len] + data_in[offset + apdu_len + 1] +
                        data_in[offset + apdu_len + 2] + data_in[offset + apdu_len + 3], 16))
    output(data_in[offset + apdu_len] + ' ' + data_in[offset + apdu_len + 1] + ' ' + data_in[offset +
                                                                                             apdu_len + 2] + ' ' + data_in[offset + apdu_len + 3] + ' —— 期望的应用连接超时时间:' + stXinTiao + 's')
    apdu_len = apdu_len + 4
    if data_in[offset + apdu_len] == '00':
        output(data_in[offset + apdu_len] + ' —— 公共连接')
    elif data_in[offset + apdu_len] == '01':
        output(data_in[offset + apdu_len] + ' —— 一般密码')
        apdu_len = apdu_len + 1
        stXinTiao = int(data_in[offset + apdu_len], 16)
        output(data_in[offset + apdu_len] + ' —— 一般密码长度=' + str(stXinTiao))
        apdu_len = apdu_len + 1
        DataText = ''
        DataText1 = ''
        for k in range(0, stXinTiao):
            DataText = DataText + data_in[offset + apdu_len] + ' '
            DataText1 = DataText1 + chr(int(data_in[offset + apdu_len], 16))
            apdu_len = apdu_len + 1
        output(DataText + ' —— 一般密码=' + DataText1)
    elif data_in[offset + apdu_len] == '02':
        output(data_in[offset + apdu_len] + ' —— 对称加密')
        apdu_len = apdu_len + 1
        stXinTiao = int(data_in[offset + apdu_len], 16)
        output(data_in[offset + apdu_len] + ' —— 密文1 长度=' + str(stXinTiao))
        apdu_len = apdu_len + 1
        DataText = ''
        for k in range(0, stXinTiao):
            DataText = DataText + data_in[offset + apdu_len] + ' '
            apdu_len = apdu_len + 1
        output(DataText + ' —— 密文1')
        stXinTiao = int(data_in[offset + apdu_len], 16)
        output(data_in[offset + apdu_len] + ' —— 客户机签名1 长度=' + str(stXinTiao))
        apdu_len = apdu_len + 1
        DataText = ''
        for k in range(0, stXinTiao):
            DataText = DataText + data_in[offset + apdu_len] + ' '
            apdu_len = apdu_len + 1
        output(DataText + ' —— 客户机签名1')
    elif data_in[offset + apdu_len] == '03':
        output(data_in[offset + apdu_len] + ' —— 数字签名')
        apdu_len = apdu_len + 1
        stXinTiao = int(data_in[offset + apdu_len], 16)
        output(data_in[offset + apdu_len] + ' —— 密文2 长度=' + str(stXinTiao))
        apdu_len = apdu_len + 1
        DataText = ''
        for k in range(0, stXinTiao):
            DataText = DataText + data_in[offset + apdu_len] + ' '
            apdu_len = apdu_len + 1
        output(DataText + ' —— 密文2')
        stXinTiao = int(data_in[offset + apdu_len], 16)
        output(data_in[offset + apdu_len] + ' —— 客户机签名2 长度=' + str(stXinTiao))
        apdu_len = apdu_len + 1
        DataText = ''
        for k in range(0, stXinTiao):
            DataText = DataText + data_in[offset + apdu_len] + ' '
            apdu_len = apdu_len + 1
        output(DataText + ' —— 客户机签名2')
    else:
        output(data_in[offset + apdu_len] + ' —— 报文有误')
    apdu_len += 1
    return apdu_len


def release_request(offset, *data_in):
    apdu_len = 2
    return apdu_len


def link_response(offset, *data_in):
    apdu_len = 2
    time_credible_flag = int(data_in[offset + apdu_len], 16) >> 7
    if time_credible_flag == 1:
        output(data_in[offset + apdu_len] + ' —— 结果Result：可信')
    else:
        output(data_in[offset + apdu_len] + ' —— 结果Result：不可信')
    apdu_len += 1
    apdu_len += take_date_time(data_in[offset + apdu_len: offset + apdu_len + 10], '(请求时间)')
    apdu_len += take_date_time(data_in[offset + apdu_len: offset + apdu_len + 10], '(收到时间)')
    apdu_len += take_date_time(data_in[offset + apdu_len: offset + apdu_len + 10], '(响应时间)')
    return apdu_len


def connect_response(offset, *data_in):
    apdu_len = 2
    DataText = ''
    for k in range(0, 4):
        DataText = DataText + data_in[offset + apdu_len] + ' '
        apdu_len = apdu_len + 1
    output(DataText + ' —— 厂商代码')
    DataText = ''
    for k in range(0, 4):
        DataText = DataText + data_in[offset + apdu_len] + ' '
        apdu_len = apdu_len + 1
    output(DataText + ' —— 软件版本号')
    DataText = ''
    for k in range(0, 6):
        DataText = DataText + data_in[offset + apdu_len] + ' '
        apdu_len = apdu_len + 1
    output(DataText + ' —— 软件版本日期')
    DataText = ''
    for k in range(0, 4):
        DataText = DataText + data_in[offset + apdu_len] + ' '
        apdu_len = apdu_len + 1
    output(DataText + ' —— 硬件版本号')
    DataText = ''
    for k in range(0, 6):
        DataText = DataText + data_in[offset + apdu_len] + ' '
        apdu_len = apdu_len + 1
    output(DataText + ' —— 硬件版本日期')
    DataText = ''
    for k in range(0, 8):
        DataText = DataText + data_in[offset + apdu_len] + ' '
        apdu_len = apdu_len + 1
    output(DataText + ' —— 厂家扩展信息')
    output(data_in[offset + apdu_len] + ' ' + data_in[offset + apdu_len + 1] + ' —— 商定的应用层协议版本号')
    apdu_len = apdu_len + 2
    DataText = ''
    for k in range(0, 8):
        DataText = DataText + data_in[offset + apdu_len] + ' '
        apdu_len = apdu_len + 1
    output(DataText + ' —— 商定的协议一致性块')
    DataText = ''
    for k in range(0, 16):
        DataText = DataText + data_in[offset + apdu_len] + ' '
        apdu_len = apdu_len + 1
    output(DataText + ' —— 商定的功能一致性块')
    stXinTiao = str(int(data_in[offset + apdu_len] + data_in[offset + apdu_len + 1], 16))
    output(data_in[offset + apdu_len] + ' ' + data_in[offset +
                                                      apdu_len + 1] + ' —— 服务器发送帧最大尺寸:' + stXinTiao + '字节')
    apdu_len = apdu_len + 2
    stXinTiao = str(int(data_in[offset + apdu_len] + data_in[offset + apdu_len + 1], 16))
    output(data_in[offset + apdu_len] + ' ' + data_in[offset +
                                                      apdu_len + 1] + ' —— 服务器接收帧最大尺寸:' + stXinTiao + '字节')
    apdu_len = apdu_len + 2
    stXinTiao = str(int(data_in[offset + apdu_len], 16))
    output(data_in[offset + apdu_len] + ' —— 服务器接收帧最大窗口尺寸:' + stXinTiao + '个')
    apdu_len = apdu_len + 1
    stXinTiao = str(int(data_in[offset + apdu_len] + data_in[offset + apdu_len + 1], 16))
    output(data_in[offset + apdu_len] + ' ' + data_in[offset +
                                                      apdu_len + 1] + ' —— 服务器最大可处理APDU尺寸:' + stXinTiao)
    apdu_len = apdu_len + 2
    stXinTiao = str(int(data_in[offset + apdu_len] + data_in[offset + apdu_len + 1] +
                        data_in[offset + apdu_len + 2] + data_in[offset + apdu_len + 3], 16))
    output(data_in[offset + apdu_len] + ' ' + data_in[offset + apdu_len + 1] + ' ' + data_in[offset +
                                                                                             apdu_len + 2] + ' ' + data_in[offset + apdu_len + 3] + ' —— 商定的应用连接超时时间:' + stXinTiao + 's')
    apdu_len = apdu_len + 4
    connect_result = {
        '00': ' —— 允许建立应用连接',
        '01': ' —— 密码错误',
        '02': ' —— 对称解密错误',
        '03': ' —— 非对称解密错误',
        '04': ' —— 签名错误',
        '05': ' —— 协议版本不匹配',
        'FF': ' —— 其他错误'
    }[data_in[offset + apdu_len]]
    output(data_in[offset + apdu_len] + connect_result)
    apdu_len += 1
    optional_message = data_in[offset + apdu_len]
    output(optional_message + ' —— 认证附加信息')
    apdu_len += 1
    if optional_message == 0:
        return apdu_len

    RN_len = data_in[offset + apdu_len]
    output(RN_len + ' —— 服务器随机数长度:' + str(int(RN_len, 16)))
    apdu_len += 1
    RN_text = ''
    for k in range(0, int(RN_len, 16)):
        RN_text += data_in[offset + apdu_len + k] + ' '
    output(RN_text + ' —— 服务器随机数')
    apdu_len += int(RN_len, 16)

    signature_info_len = data_in[offset + apdu_len]
    output(signature_info_len + ' —— 服务器签名信息长度:' + str(int(signature_info_len, 16)))
    apdu_len += 1
    signature_info_text = ''
    for k in range(0, int(signature_info_len, 16)):
        signature_info_text += data_in[offset + apdu_len + k] + ' '
    output(signature_info_text + ' —— 服务器签名信息')
    apdu_len += int(signature_info_len, 16)

    return apdu_len


def release_response(offset, *data_in):
    apdu_len = 2
    if data_in[offset + apdu_len] == '00':
        output(data_in[offset + apdu_len] + ' —— 成功')
    else:
        output(data_in[offset + apdu_len] + ' —— 不成功')
    apdu_len += 1
    return apdu_len


def connect_service(offset, *data_in):
    output(data_in[offset + 1] + ' —— PIID')
    apdu_len = {
        '01': link_request,
        '02': connect_request,
        '03': release_request,
        '81': link_response,
        '82': connect_response,
        '83': release_response
    }[data_in[offset]](offset, *data_in)
    return apdu_len
