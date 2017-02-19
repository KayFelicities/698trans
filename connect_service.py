'''connect service'''
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
    except Exception:
        output(data[offset] + ' —— 报文有误')
    offset += 1
    offset += take_long_unsigned(data[offset:], '心跳周期s:')
    offset += take_date_time(data[offset:], '请求时间:')
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
    offset += take_date_time(data[offset:], '请求时间:')
    offset += take_date_time(data[offset:], '收到时间:')
    offset += take_date_time(data[offset:], '响应时间:')
    return offset


def connect_request(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_long_unsigned(data[offset:], '期望的应用层协议版本号:')
    show_data_source(data[offset:], 8)
    output(' —— 期望的协议一致性块')
    offset += 8
    show_data_source(data[offset:], 16)
    offset += 16
    output(' —— 期望的功能一致性块')
    offset += take_long_unsigned(data[offset:], '客户机发送帧最大尺寸:')
    offset += take_long_unsigned(data[offset:], '客户机接收帧最大尺寸:')
    offset += take_unsigned(data[offset:], '客户机接收帧最大窗口尺寸:')
    offset += take_long_unsigned(data[offset:], '客户机最大可处理APDU尺寸:')
    offset += take_double_long_unsigned(data[offset:], '期望的应用连接超时时间:')
    offset += take_ConnectMechanismInfo(data[offset:], '认证请求对象:')
    return offset


def connect_response(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    offset += take_FactoryVersion(data[offset:])
    offset += take_long_unsigned(data[offset:], '商定的应用层协议版本号:')
    show_data_source(data[offset:], 8)
    output(' —— 期望的协议一致性块')
    offset += 8
    show_data_source(data[offset:], 16)
    offset += 16
    output(' —— 期望的功能一致性块')
    offset += take_long_unsigned(data[offset:], '服务器发送帧最大尺寸:')
    offset += take_long_unsigned(data[offset:], '服务器发送帧最大尺寸:')
    offset += take_unsigned(data[offset:], '服务器发送帧最大窗口尺寸:')
    offset += take_long_unsigned(data[offset:], '服务器最大可处理APDU尺寸:')
    offset += take_double_long_unsigned(data[offset:], '商定的应用连接超时时间:')
    offset += take_ConnectResponseInfo(data[offset:], '连接响应对象:')
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
