'''action service'''
from shared_functions import *  # NOQA


def ActionRequest(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_OMD(data[offset:])
    offset += take_Data(data[offset:])
    return offset


def ActionRequestList(data):
    offset = 0
    offset += take_PIID(data[offset:])
    object_num = get_num_of_SEQUENCE(data[offset:], '对象方法')
    offset += 1
    config.line_level += 1
    for object_count in range(object_num):
        end_flag = 1 if object_count == object_num - 1 else 0
        offset += take_OMD(data[offset:])
        offset += take_Data(data[offset:], end_flag=end_flag)
    config.line_level -= 1
    return offset


def ActionThenGetRequestNormalList(data):
    offset = 0
    offset += take_PIID(data[offset:])
    object_num = get_num_of_SEQUENCE(data[offset:], '设置后读取对象属性')
    offset += 1
    config.line_level += 1
    for object_count in range(object_num):
        end_flag = 1 if object_count == object_num - 1 else 0
        offset += take_OMD(data[offset:], '设置的对象方法:')
        offset += take_Data(data[offset:], '方法参数:')
        offset += take_OMD(data[offset:], '读取的对象属性:')
        offset += take_Data(data[offset:], '读取延时:', end_flag=end_flag)
    config.line_level -= 1
    return offset


def ActionResponseNormal(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    offset += take_OMD(data[offset:])
    offset += take_DAR(data[offset:], '操作执行结果')
    optional = data[offset]
    offset += take_OPTIONAL(data[offset:], '操作返回数据')
    if optional == '01':
        offset += take_Data(data[offset:])
    return offset


def ActionResponseNormalList(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    action_result_num = get_num_of_SEQUENCE(data[offset:], '对象方法操作结果')
    offset += 1
    config.line_level += 1
    for action_result_count in range(action_result_num):
        end_flag = 1 if action_result_count == action_result_num - 1 else 0
        offset += take_OMD(data[offset:])
        offset += take_DAR(data[offset:], '设置执行结果')
        optional = data[offset]
        offset += take_OPTIONAL(data[offset:], '操作返回数据')
        if optional == '01':
            offset += take_Data(data[offset:], end_flag=end_flag)
    config.line_level -= 1
    return offset


def ActionThenGetResponseNormalList(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    action_result_num = get_num_of_SEQUENCE(data[offset:], '对象方法操作结果')
    offset += 1
    config.line_level += 1
    for action_result_count in range(action_result_num):
        end_flag = 1 if action_result_count == action_result_num - 1 else 0
        offset += take_OMD(data[offset:])
        offset += take_DAR(data[offset:], '设置执行结果', level=config.line_level)
        optional = data[offset]
        offset += take_OPTIONAL(data[offset:], '操作返回数据')
        if optional == '01':
            offset += take_Data(data[offset:])
        offset += take_OAD(data[offset:])
        offset += take_Get_Result(data[offset:], end_flag=end_flag)
    config.line_level -= 1
    return offset
