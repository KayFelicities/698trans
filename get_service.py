from shared_functions import *  # NOQA


def get0501(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_OAD(data[offset:])
    return offset


def get8501(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    offset += take_A_ResultNormal(data[offset:])
    return offset


def get0502(data):
    offset = 0
    offset += take_PIID(data[offset:])
    oad_num = get_num_of_SEQUENCE(data[offset:], 'OAD')
    offset += 1
    for oad_count in range(oad_num):
        offset += take_OAD(data[offset:])
    return offset


def get8502(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    A_ResultNormal_num = get_num_of_SEQUENCE(data[offset:], 'A_ResultNormal')
    offset += 1
    for A_ResultNormal_count in range(A_ResultNormal_num):
        offset += take_A_ResultNormal(data[offset:])
    return offset


def get0503(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_GetRecord(data[offset:])
    return offset


def get8503(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    offset += take_A_ResultRecord(data[offset:])
    return offset


def get0504(data):
    offset = 0
    offset += take_PIID(data[offset:])
    get0503_num = get_num_of_SEQUENCE(data[offset:], 'getRecord')
    offset += 1
    for get0503_count in range(get0503_num):
        offset += take_GetRecord(data[offset:])
    return offset


def get8504(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    A_ResultRecord_num = get_num_of_SEQUENCE(data[offset:], 'A_ResultRecord')
    offset += 1
    for A_ResultRecord_count in range(A_ResultRecord_num):
        offset += take_A_ResultRecord(data[offset:])
    return offset


def get0505(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_long_unsigned(data[offset:], '最近一次数据块序号:')
    return offset


def get8505(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    offset += take_bool(data[offset:], '末帧标志:')
    offset += take_long_unsigned(data[offset:], '分帧序号:')

    re_data_choice = data[offset]
    if re_data_choice == '00':
        show_data_source(data[offset:], 2)
        offset += take_DAR(data[offset + 1:], '错误信息')
        offset += 2
    elif re_data_choice == '01':  # SEQUENCE OF A-ResultNormal
        show_data_source(data[offset:], 2)
        A_ResultNormal_num = get_num_of_SEQUENCE(data[offset + 1:], 'A_ResultNormal')
        output(' —— 对象属性*', str(A_ResultNormal_num))
        offset += 2
        for A_ResultNormal_count in range(A_ResultNormal_num):
            offset += take_A_ResultNormal(data[offset:])
    elif re_data_choice == '02':  # SEQUENCE OF A-ResultRecord
        show_data_source(data[offset:], 2)
        A_ResultRecord_num = get_num_of_SEQUENCE(data[offset + 1:], 'A_ResultRecord')
        output(' —— 记录型对象属性*', str(A_ResultRecord_num))
        offset += 2
        for A_ResultRecord_count in range(A_ResultRecord_num):
            offset += take_A_ResultRecord(data[offset:])
    return offset
