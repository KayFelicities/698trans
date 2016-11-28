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
    offset += {
        '01': link_request, '02': connect_request, '03': release_request,
        '81': link_response, '82': connect_response, '83': release_response,
        '0501': get0501, '0502': get0502, '0503': get0503, '0504': get0504,
        '0505': get0505,
        '8501': get8501, '8502': get8502, '8503': get8503, '8504': get8504,
        '8505': get8505,
        '0601': set0601, '0602': set0602, '0603': set0603,
        '8601': set8601, '8602': set8602, '8603': set8603,
        '0701': act0701, '0702': act0702, '0703': act0703,
        '8701': act8701, '8702': act8702, '8703': act8703,
        '0801': rep0801, '0802': rep0802,
        '8801': rep8801, '8802': rep8802,
        '0901': pro0901, '0902': pro0902, '0903': pro0903, '0904': pro0904,
        '0905': pro0905, '0906': pro0906, '0907': pro0907,
        '8901': pro8901, '8902': pro8902, '8903': pro8903, '8904': pro8904,
        '8905': pro8905, '8906': pro8906, '8907': pro8907,
        '10': security_request, '90': security_response,
    }[service_type](data[offset:])
    if data[0] in ['82', '83', '84', '85', '86', '87', '88', '89']:
        offset += take_FollowReport(data[offset:])
        offset += take_TimeTag(data[offset:])
    elif data[0] in ['02', '03', '04', '05', '06', '07', '00', '09']:
        offset += take_TimeTag(data[offset:])
    output('^' * 60 + 'APDU')
    return offset
