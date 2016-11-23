from HandleData import sFindDataID, HandleDateType
from shared_functions import *  # NOQA


def get0501(data):
    offset = 0
    output(data[offset] + ' —— PIID')
    offset += 1
    offset += take_OAD(data[offset:])
    return offset


def get8501(data):
    offset = 0
    output(data[offset] + ' —— PIID')
    offset += 1
    offset += take_A_ResultNormal(data[offset:])
    return offset


def get0502(data):
    offset = 0
    output(data[offset] + ' —— PIID')
    offset += 1
    oad_num = get_num_of_SEQUENCE(data[offset:], 'OAD')
    offset += 1
    for oad_count in range(oad_num):
        offset += take_OAD(data[offset:])
    return offset


def get8502(data):
    offset = 0
    output(data[offset] + ' —— PIID')
    offset += 1
    return offset


def get0503(data):
    offset = 0
    output(data[offset] + ' —— PIID')
    offset += 1
    offset += take_OAD(data[offset:])
    offset += take_RSD(data[offset:])  # RSD
    offset += take_RCSD(data[offset:])  # RCSD处理
    return offset


def get8503(data):
    offset = 0
    output(data[offset] + ' —— PIID')
    offset += 1
    return offset


def get0504(data):
    offset = 0
    output(data[offset] + ' —— PIID')
    offset += 1
    get0503_num = get_num_of_SEQUENCE(data[offset:], 'getRecord')
    offset += 1
    for get0503_count in range(get0503_num):
        get0503(data[offset:])
    return offset


def get8504(data):
    offset = 0
    output(data[offset] + ' —— PIID')
    offset += 1
    return offset


def get0505(data):
    offset = 0
    output(data[offset] + ' —— PIID')
    offset += 1
    offset += take_long_unsigned(data[offset:], '(最近一次数据块序号)')
    return offset


def get8505(data):
    offset = 0
    output(data[offset] + ' —— PIID')
    offset += 1
    return offset
