'''get service'''
from shared_functions import *  # NOQA


def GetRequestNormal(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_OAD(data[offset:])
    return offset


def GetRequestNormalList(data):
    offset = 0
    offset += take_PIID(data[offset:])
    oad_num = get_num_of_SEQUENCE(data[offset:], 'OAD')
    offset += 1
    config.line_level += 1
    for oad_count in range(oad_num):
        end_flag = 1 if oad_count == oad_num - 1 else 0
        offset += take_OAD(data[offset:], end_flag=end_flag)
    config.line_level -= 1
    return offset


def GetRequestRecord(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_GetRecord(data[offset:])
    return offset


def GetRequestRecordList(data):
    offset = 0
    offset += take_PIID(data[offset:])
    GetRequestRecord_num = get_num_of_SEQUENCE(data[offset:], 'getRecord')
    offset += 1
    config.line_level += 1
    for GetRequestRecord_count in range(GetRequestRecord_num):
        end_flag = 1 if GetRequestRecord_count == GetRequestRecord_num - 1 else 0
        offset += take_GetRecord(data[offset:], end_flag=end_flag)
    config.line_level -= 1
    return offset


def GetRequestNext(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_long_unsigned(data[offset:], '最近一次数据块序号:')
    return offset


def GetResponseNormal(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    offset += take_A_ResultNormal(data[offset:])
    return offset


def GetResponseNormalList(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    A_ResultNormal_num = get_num_of_SEQUENCE(data[offset:], 'A_ResultNormal')
    offset += 1
    config.line_level += 1
    for A_ResultNormal_count in range(A_ResultNormal_num):
        end_flag = 1 if A_ResultNormal_count == A_ResultNormal_num - 1 else 0
        offset += take_A_ResultNormal(data[offset:], end_flag=end_flag)
    config.line_level -= 1
    return offset


def GetResponseRecord(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    offset += take_A_ResultRecord(data[offset:])
    return offset


def GetResponseRecordList(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    A_ResultRecord_num = get_num_of_SEQUENCE(data[offset:], 'A_ResultRecord')
    offset += 1
    config.line_level += 1
    for A_ResultRecord_count in range(A_ResultRecord_num):
        end_flag = 1 if A_ResultRecord_count == A_ResultRecord_num - 1 else 0
        offset += take_A_ResultRecord(data[offset:], end_flag=end_flag)
    config.line_level -= 1
    return offset


def GetResponseNext(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    offset += take_bool(data[offset:], '末帧标志:')
    offset += take_long_unsigned(data[offset:], '分帧序号:')

    re_data_choice = data[offset]
    if re_data_choice == '00':
        show_data_source(data[offset:], 1)
        output(' —— 错误信息')
        offset += take_DAR(data[offset + 1:], '错误信息')
        offset += 2
    elif re_data_choice == '01':  # SEQUENCE OF A-ResultNormal
        show_data_source(data[offset:], 1)
        output(' —— 对象属性')
        A_ResultNormal_num = get_num_of_SEQUENCE(data[offset + 1:], 'A_ResultNormal')
        offset += 2
        config.line_level += 1
        for A_ResultNormal_count in range(A_ResultNormal_num):
            end_flag = 1 if A_ResultNormal_count == A_ResultNormal_num - 1 else 0
            offset += take_A_ResultNormal(data[offset:], end_flag=end_flag)
        config.line_level -= 1
    elif re_data_choice == '02':  # SEQUENCE OF A-ResultRecord
        show_data_source(data[offset:], 1)
        output(' —— 记录型对象属性')
        A_ResultRecord_num = get_num_of_SEQUENCE(data[offset + 1:], 'A_ResultRecord')
        offset += 2
        config.line_level += 1
        for A_ResultRecord_count in range(A_ResultRecord_num):
            end_flag = 1 if A_ResultRecord_count == A_ResultRecord_num - 1 else 0
            offset += take_A_ResultRecord(data[offset:], end_flag=end_flag)
        config.line_level -= 1
    return offset
