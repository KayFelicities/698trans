from shared_functions import *  # NOQA


def act0701(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_OMD(data[offset:])
    offset += take_Data(data[offset:])
    return offset


def act8701(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    offset += take_OMD(data[offset:])
    offset += take_DAR(data[offset:], '操作执行结果')
    optional = data[offset]
    offset += take_OPTIONAL(data[offset:], '操作返回数据')
    if optional == '01':
        offset += take_Data(data[offset:])
    return offset


def act0702(data):
    offset = 0
    offset += take_PIID(data[offset:])
    object_num = get_num_of_SEQUENCE(data[offset:], '对象方法')
    offset += 1
    for object_count in range(object_num):
        offset += take_OMD(data[offset:])
        offset += take_Data(data[offset:])
    return offset


def act8702(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    action_result_num = get_num_of_SEQUENCE(data[offset:], '对象方法操作结果')
    for action_result_count in range(action_result_num):
        offset += take_OMD(data[offset:])
        offset += take_DAR(data[offset:], '设置执行结果')
        optional = data[offset]
        offset += take_OPTIONAL(data[offset:], '操作返回数据')
        if optional == '01':
            offset += take_Data(data[offset:])
    return offset


def act0703(data):
    offset = 0
    offset += take_PIID(data[offset:])
    object_num = get_num_of_SEQUENCE(data[offset:], '设置后读取对象属性')
    offset += 1
    for object_count in range(object_num):
        offset += take_OMD(data[offset:], '设置的对象方法:')
        offset += take_Data(data[offset:], '方法参数:')
        offset += take_OMD(data[offset:], '读取的对象属性:')
        offset += take_Data(data[offset:], '读取延时:')
    return offset


def act8703(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    action_result_num = get_num_of_SEQUENCE(data[offset:], '对象方法操作结果')
    for action_result_count in range(action_result_num):
        offset += take_OMD(data[offset:])
        offset += take_DAR(data[offset:], '设置执行结果')
        optional = data[offset]
        offset += take_OPTIONAL(data[offset:], '操作返回数据')
        if optional == '01':
            offset += take_Data(data[offset:])
        offset += take_OAD(data[offset:])
        offset += take_Get_Result(data[offset:])
    return offset
