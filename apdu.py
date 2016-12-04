from get_service import *  # NOQA
from set_service import *  # NOQA
from action_service import *  # NOQA
from report_service import *  # NOQA
from proxy_service import *  # NOQA
from connect_service import *  # NOQA
from security_service import *  # NOQA


def take_APDU(data, add_text=''):
    offset = 0
    output('=' * 60 + 'APDU')
    offset_temp, service_type = take_service_type(data[offset:])
    offset += offset_temp
    # try:
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
        '10': security_request,
        '90': security_response,
    }[service_type](data[offset:])
    # except Exception:
    #     output('报文格式错误')
    #     return offset
    if data[0] in ['82', '83', '84', '85', '86', '87', '88', '89']:
        offset += take_FollowReport(data[offset:])
        offset += take_TimeTag(data[offset:])
    elif data[0] in ['02', '03', '04', '05', '06', '07', '00', '09']:
        offset += take_TimeTag(data[offset:])
    output('^' * 60 + 'APDU')
    return offset
