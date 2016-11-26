from shared_functions import *  # NOQA


def set0601(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_OAD(data[offset:])
    offset += take_Data(data[offset:])
    return offset


def set8601(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    dar = get_DAR(data[offset])
    output(' —— 设置执行结果:' + dar)
    offset += 1
    return offset


def set0602(data):
    offset = 0
    offset += take_PIID(data[offset:])
    object_num = get_num_of_SEQUENCE(data[offset:], '对象属性')
    offset += 1
    for object_count in range(object_num):
        offset += take_OAD(data[offset:])
        offset += take_Data(data[offset:])
    return offset


def set8602(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    set_result_num = get_num_of_SEQUENCE(data[offset:], '对象属性设置结果')
    offset += 1
    for set_result_count in range(set_result_num):
        offset += take_OAD(data[offset:])
        dar = get_DAR(data[offset])
        output(' —— 设置执行结果:' + dar)
        offset += 1
    return offset


def set0603(data):
    offset = 0
    offset += take_PIID(data[offset:])
    object_num = get_num_of_SEQUENCE(data[offset:], '设置后读取对象属性')
    offset += 1
    for object_count in range(object_num):
        offset += take_OAD(data[offset:], '设置的对象属性:')
        offset += take_Data(data[offset:], '数据:')
        offset += take_OAD(data[offset:], '读取的对象属性:')
        offset += take_Data(data[offset:], '延时读取时间:')
    return offset


def set8603(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    set_result_num = get_num_of_SEQUENCE(data[offset:], '对象属性设置后读取结果')
    offset += 1
    for set_result_count in range(set_result_num):
        offset += take_OAD(data[offset:])
        dar = get_DAR(data[offset])
        output(' —— 设置执行结果:' + dar)
        offset += 1
        offset += take_OAD(data[offset:])
        offset += take_Get_Result(data[offset:])
    return offset
