from shared_functions import *  # NOQA


def SetRequestNormal(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_OAD(data[offset:])
    offset += take_Data(data[offset:])
    return offset


def SetRequestNormalList(data):
    offset = 0
    offset += take_PIID(data[offset:])
    object_num = get_num_of_SEQUENCE(data[offset:], '对象属性')
    offset += 1
    config.line_level += 1
    for object_count in range(object_num):
        end_flag = 1 if object_count == object_num - 1 else 0
        offset += take_OAD(data[offset:])
        offset += take_Data(data[offset:], end_flag=end_flag)
    config.line_level -= 1
    return offset


def SetThenGetRequestNormalList(data):
    offset = 0
    offset += take_PIID(data[offset:])
    object_num = get_num_of_SEQUENCE(data[offset:], '设置后读取对象属性')
    offset += 1
    config.line_level += 1
    for object_count in range(object_num):
        end_flag = 1 if object_count == object_num - 1 else 0
        offset += take_OAD(data[offset:], '设置的对象属性:')
        offset += take_Data(data[offset:], '数据:')
        offset += take_OAD(data[offset:], '读取的对象属性:')
        offset += take_Data(data[offset:], '延时读取时间:', end_flag=end_flag)
    config.line_level -= 1
    return offset


def SetResponseNormal(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    offset += take_OAD(data[offset:])
    offset += take_DAR(data[offset:], '设置执行结果')
    return offset


def SetResponseNormalList(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    set_result_num = get_num_of_SEQUENCE(data[offset:], '对象属性设置结果')
    offset += 1
    config.line_level += 1
    for set_result_count in range(set_result_num):
        end_flag = 1 if set_result_count == set_result_num - 1 else 0
        offset += take_OAD(data[offset:])
        offset += take_DAR(data[offset:], '设置执行结果', end_flag=end_flag)
    config.line_level -= 1
    return offset


def SetThenGetResponseNormalList(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    set_result_num = get_num_of_SEQUENCE(data[offset:], '对象属性设置后读取结果')
    offset += 1
    config.line_level += 1
    for set_result_count in range(set_result_num):
        end_flag = 1 if set_result_count == set_result_num - 1 else 0
        offset += take_OAD(data[offset:])
        offset += take_DAR(data[offset:], '设置执行结果', level=config.line_level)
        offset += take_OAD(data[offset:])
        offset += take_Get_Result(data[offset:], end_flag=end_flag)
    config.line_level -= 1
    return offset
