from shared_functions import *  # NOQA
from get_service import *  # NOQA
from set_service import *  # NOQA
from action_service import *  # NOQA
from report_service import *  # NOQA
from proxy_service import *  # NOQA
from connect_service import *  # NOQA


def security_request(data):
    offset = 0
    security_choice = data[offset]
    if security_choice == '00':  # 明文
        octect_string_len, len_offset = get_len_of_octect_string(data[offset + 1:])
        show_data_source(data[offset:], 1 + len_offset)
        output(' —— 明文应用数据单元, 长度' + str(octect_string_len))
        offset += 1 + len_offset
        offset += take_security_APDU(data[offset:])
    else:   # 密文
        show_data_source(data[offset:], 1)
        offset += take_octect_string(data[offset + 1:], '密文应用数据单元') + 1
    security_choice = data[offset]
    print('security_choice:', security_choice)
    offset += 1
    offset += {
        '00': take_SID_MAC,
        '01': take_RN,
        '02': take_RN_MAC,
        '03': take_SID,
    }[security_choice](data[offset:], '(数据验证信息)')
    return offset


def security_response(data):
    offset = 0
    security_choice = data[offset]
    if security_choice == '00':
        octect_string_len, len_offset = get_len_of_octect_string(data[offset + 1:])
        show_data_source(data[offset:], 1 + len_offset)
        output(' —— 明文应用数据单元, 长度' + str(octect_string_len))
        offset += 1 + len_offset
        offset += take_security_APDU(data[offset:])
    elif security_choice == '01':
        show_data_source(data[offset:], 1)
        offset += take_octect_string(data[offset + 1:], '密文应用数据单元') + 1
    elif security_choice == '02':
        show_data_source(data[offset:], 1)
        offset += 1
        offset += take_DAR(data[offset:], '异常错误')
    optional = data[offset]
    offset += take_OPTIONAL(data[offset:], '数据验证信息')
    if optional == '01':
        check_choice = data[offset]
        show_data_source(data[offset:], 1)
        output(' —— 数据验证方式:数据MAC')
        offset += 1
        if check_choice == '00':
            offset += take_MAC(data[offset:])
    return offset


def take_security_APDU(data, add_text=''):
    offset = 0
    output('*' * 50 + '安全传输APDU')
    offset_temp, service_type = take_service_type(data[offset:])
    offset += offset_temp
    offset += {
        '01': link_request,
        '02': connect_request,
        '03': release_request,
        '81': link_response,
        '82': connect_response,
        '83': release_response,
        '0501': GetRequestNormal,
        '0502': GetRequestNormalList,
        '0503': GetRequestRecord,
        '0504': GetRequestRecordList,
        '0505': GetRequestNext,
        '8501': GetResponseNormal,
        '8502': GetResponseNormalList,
        '8503': GetResponseRecord,
        '8504': GetResponseRecordList,
        '8505': GetResponseNext,
        '0601': SetRequestNormal,
        '0602': SetRequestNormalList,
        '0603': SetThenGetRequestNormalList,
        '8601': SetResponseNormal,
        '8602': SetResponseNormalList,
        '8603': SetThenGetResponseNormalList,
        '0701': ActionRequest,
        '0702': ActionRequestList,
        '0703': ActionThenGetRequestNormalList,
        '8701': ActionResponseNormal,
        '8702': ActionResponseNormalList,
        '8703': ActionThenGetResponseNormalList,
        '0801': ReportResponseList,
        '0802': ReportResponseRecordList,
        '8801': ReportNotificationList,
        '8802': ReportNotificationRecordList,
        '0901': ProxyGetRequestList,
        '0902': ProxyGetRequestRecord,
        '0903': ProxySetRequestList,
        '0904': ProxySetThenGetRequestList,
        '0905': ProxyActionRequestList,
        '0906': ProxyActionThenGetRequestList,
        '0907': ProxyTransCommandRequest,
        '8901': ProxyGetResponseList,
        '8902': ProxyGetResponseRecord,
        '8903': ProxySetResponseList,
        '8904': ProxySetThenGetResponseList,
        '8905': ProxyActionResponseList,
        '8906': ProxyActionThenGetResponseList,
        '8907': ProxyTransCommandResponse,
    }[service_type](data[offset:])
    if data[0] in ['82', '83', '84', '85', '86', '87', '88', '89']:
        offset += take_FollowReport(data[offset:])
        offset += take_TimeTag(data[offset:])
    elif data[0] in ['02', '03', '04', '05', '06', '07', '00', '09']:
        offset += take_TimeTag(data[offset:])
    output('*' * 50 + '安全传输APDU')
    return offset
