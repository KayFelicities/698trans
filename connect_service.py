from shared_functions import *  # NOQA


def link_request(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    try:
        link_type = {
            '00': ' —— 登录',
            '01': ' —— 心跳',
            '02': ' —— 退出登录'
        }[data[offset]]
        output(data[offset] + link_type)
    except:
        output(data[offset] + ' —— 报文有误')
    offset += 1
    offset += take_long_unsigned(data[offset:], '(心跳周期s)')
    offset += take_date_time(data[offset:], '(请求时间)')
    return offset


def link_response(data):
    offset = 0
    offset += take_PIID(data[offset:])
    time_credible_flag = int(data[offset], 16) >> 7
    if time_credible_flag == 1:
        output(data[offset] + ' —— 结果Result：可信')
    else:
        output(data[offset] + ' —— 结果Result：不可信')
    offset += 1
    offset += take_date_time(data[offset:], '(请求时间)')
    offset += take_date_time(data[offset:], '(收到时间)')
    offset += take_date_time(data[offset:], '(响应时间)')
    return offset


def connect_request(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_long_unsigned(data[offset:], '(期望的应用层协议版本号)')
    DataText = ''
    for k in range(0, 8):
        DataText = DataText + data[offset] + ' '
        offset = offset + 1
    output(DataText + ' —— 期望的协议一致性块')
    DataText = ''
    for k in range(0, 16):
        DataText = DataText + data[offset] + ' '
        offset = offset + 1
    output(DataText + ' —— 期望的功能一致性块')
    stXinTiao = str(int(data[offset] + data[offset + 1], 16))
    output(data[offset] + ' ' + data[offset + 1] + ' —— 客户机发送帧最大尺寸:' + stXinTiao + '字节')
    offset += 2
    stXinTiao = str(int(data[offset] + data[offset + 1], 16))
    output(data[offset] + ' ' + data[offset + 1] + ' —— 客户机接收帧最大尺寸:' + stXinTiao + '字节')
    offset = offset + 2
    stXinTiao = str(int(data[offset], 16))
    output(data[offset] + ' —— 客户机接收帧最大窗口尺寸:' + stXinTiao + '个')
    offset = offset + 1
    stXinTiao = str(int(data[offset] + data[offset + 1], 16))
    output(data[offset] + ' ' + data[offset + 1] + ' —— 客户机最大可处理APDU尺寸:' + stXinTiao)
    offset = offset + 2
    stXinTiao = str(int(data[offset] + data[offset + 1] + data[offset + 2] + data[offset + 3], 16))
    output(data[offset] + ' ' + data[offset + 1] + ' ' + data[offset + 2] + ' ' + data[offset + 3] + ' —— 期望的应用连接超时时间:' + stXinTiao + 's')
    offset = offset + 4
    if data[offset] == '00':
        output(data[offset] + ' —— 公共连接')
    elif data[offset] == '01':
        output(data[offset] + ' —— 一般密码')
        offset = offset + 1
        stXinTiao = int(data[offset], 16)
        output(data[offset] + ' —— 一般密码长度=' + str(stXinTiao))
        offset = offset + 1
        DataText = ''
        DataText1 = ''
        for k in range(0, stXinTiao):
            DataText = DataText + data[offset] + ' '
            DataText1 = DataText1 + chr(int(data[offset], 16))
            offset = offset + 1
        output(DataText + ' —— 一般密码=' + DataText1)
    elif data[offset] == '02':
        output(data[offset] + ' —— 对称加密')
        offset = offset + 1
        stXinTiao = int(data[offset], 16)
        output(data[offset] + ' —— 密文1 长度=' + str(stXinTiao))
        offset = offset + 1
        DataText = ''
        for k in range(0, stXinTiao):
            DataText = DataText + data[offset] + ' '
            offset = offset + 1
        output(DataText + ' —— 密文1')
        stXinTiao = int(data[offset], 16)
        output(data[offset] + ' —— 客户机签名1 长度=' + str(stXinTiao))
        offset = offset + 1
        DataText = ''
        for k in range(0, stXinTiao):
            DataText = DataText + data[offset] + ' '
            offset = offset + 1
        output(DataText + ' —— 客户机签名1')
    elif data[offset] == '03':
        output(data[offset] + ' —— 数字签名')
        offset = offset + 1
        stXinTiao = int(data[offset], 16)
        output(data[offset] + ' —— 密文2 长度=' + str(stXinTiao))
        offset = offset + 1
        DataText = ''
        for k in range(0, stXinTiao):
            DataText = DataText + data[offset] + ' '
            offset = offset + 1
        output(DataText + ' —— 密文2')
        stXinTiao = int(data[offset], 16)
        output(data[offset] + ' —— 客户机签名2 长度=' + str(stXinTiao))
        offset = offset + 1
        DataText = ''
        for k in range(0, stXinTiao):
            DataText = DataText + data[offset] + ' '
            offset = offset + 1
        output(DataText + ' —— 客户机签名2')
    else:
        output(data[offset] + ' —— 报文有误')
    offset += 1
    return offset


def connect_response(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    DataText = ''
    for k in range(0, 4):
        DataText = DataText + data[offset] + ' '
        offset = offset + 1
    output(DataText + ' —— 厂商代码')
    DataText = ''
    for k in range(0, 4):
        DataText = DataText + data[offset] + ' '
        offset = offset + 1
    output(DataText + ' —— 软件版本号')
    DataText = ''
    for k in range(0, 6):
        DataText = DataText + data[offset] + ' '
        offset = offset + 1
    output(DataText + ' —— 软件版本日期')
    DataText = ''
    for k in range(0, 4):
        DataText = DataText + data[offset] + ' '
        offset = offset + 1
    output(DataText + ' —— 硬件版本号')
    DataText = ''
    for k in range(0, 6):
        DataText = DataText + data[offset] + ' '
        offset = offset + 1
    output(DataText + ' —— 硬件版本日期')
    DataText = ''
    for k in range(0, 8):
        DataText = DataText + data[offset] + ' '
        offset = offset + 1
    output(DataText + ' —— 厂家扩展信息')
    output(data[offset] + ' ' + data[offset + 1] + ' —— 商定的应用层协议版本号')
    offset = offset + 2
    DataText = ''
    for k in range(0, 8):
        DataText = DataText + data[offset] + ' '
        offset = offset + 1
    output(DataText + ' —— 商定的协议一致性块')
    DataText = ''
    for k in range(0, 16):
        DataText = DataText + data[offset] + ' '
        offset = offset + 1
    output(DataText + ' —— 商定的功能一致性块')
    stXinTiao = str(int(data[offset] + data[offset + 1], 16))
    output(data[offset] + ' ' + data[offset + 1] + ' —— 服务器发送帧最大尺寸:' + stXinTiao + '字节')
    offset = offset + 2
    stXinTiao = str(int(data[offset] + data[offset + 1], 16))
    output(data[offset] + ' ' + data[offset + 1] + ' —— 服务器接收帧最大尺寸:' + stXinTiao + '字节')
    offset = offset + 2
    stXinTiao = str(int(data[offset], 16))
    output(data[offset] + ' —— 服务器接收帧最大窗口尺寸:' + stXinTiao + '个')
    offset = offset + 1
    stXinTiao = str(int(data[offset] + data[offset + 1], 16))
    output(data[offset] + ' ' + data[offset + 1] + ' —— 服务器最大可处理APDU尺寸:' + stXinTiao)
    offset = offset + 2
    stXinTiao = str(int(data[offset] + data[offset + 1] +
                        data[offset + 2] + data[offset + 3], 16))
    output(data[offset] + ' ' + data[offset + 1] + ' ' + data[offset + 2] + ' ' + data[offset + 3] + ' —— 商定的应用连接超时时间:' + stXinTiao + 's')
    offset = offset + 4
    connect_result = {
        '00': ' —— 允许建立应用连接',
        '01': ' —— 密码错误',
        '02': ' —— 对称解密错误',
        '03': ' —— 非对称解密错误',
        '04': ' —— 签名错误',
        '05': ' —— 协议版本不匹配',
        'FF': ' —— 其他错误'
    }[data[offset]]
    output(data[offset] + connect_result)
    offset += 1
    optional_message = data[offset]
    output(optional_message + ' —— 认证附加信息')
    offset += 1
    if optional_message == 0:
        return offset
    RN_len = data[offset]
    output(RN_len + ' —— 服务器随机数长度:' + str(int(RN_len, 16)))
    offset += 1
    RN_text = ''
    for k in range(0, int(RN_len, 16)):
        RN_text += data[offset + k] + ' '
    output(RN_text + ' —— 服务器随机数')
    offset += int(RN_len, 16)
    signature_info_len = data[offset]
    output(signature_info_len + ' —— 服务器签名信息长度:' + str(int(signature_info_len, 16)))
    offset += 1
    signature_info_text = ''
    for k in range(0, int(signature_info_len, 16)):
        signature_info_text += data[offset + k] + ' '
    output(signature_info_text + ' —— 服务器签名信息')
    offset += int(signature_info_len, 16)
    return offset


def release_request(data):
    offset = 0
    offset += take_PIID(data[offset:])
    return offset


def release_response(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    if data[offset] == '00':
        output(data[offset] + ' —— 成功')
    else:
        output(data[offset] + ' —— 不成功')
    offset += 1
    return offset
