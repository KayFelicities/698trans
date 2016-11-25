from shared_functions import *  # NOQA


def pro0901(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_long_unsigned(data[offset:], '整个代理请求的超时时间:')
    proxy_num = get_num_of_SEQUENCE(data[offset:], '代理服务器')
    offset += 1
    for proxy_count in range(proxy_num):
        offset += take_TSA(data[offset:], '目标服务器地址:')
        offset += take_long_unsigned(data[offset:], '代理一个服务器的超时时间:')
        oad_num = get_num_of_SEQUENCE(data[offset:], 'OAD')
        offset += 1
        for oad_count in range(oad_num):
            offset += take_OAD(data[offset:])
    return offset


def pro0902(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_long_unsigned(data[offset:], '代理请求的超时时间:')
    offset += take_TSA(data[offset:], '目标服务器地址:')
    offset += take_OAD(data[offset:])
    offset += take_RSD(data[offset:])
    offset += take_RCSD(data[offset:])
    return offset


def pro0903(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_long_unsigned(data[offset:], '整个代理请求的超时时间:')
    proxy_num = get_num_of_SEQUENCE(data[offset:], '代理服务器')
    offset += 1
    for proxy_count in range(proxy_num):
        offset += take_TSA(data[offset:], '目标服务器地址:')
        offset += take_long_unsigned(data[offset:], '代理一个服务器的超时时间:')
        oad_num = get_num_of_SEQUENCE(data[offset:], 'OAD及其数据')
        offset += 1
        for oad_count in range(oad_num):
            offset += take_OAD(data[offset:])
            offset += take_Data(data[offset:])
    return offset


def pro0904(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_long_unsigned(data[offset:], '整个代理请求的超时时间:')
    proxy_num = get_num_of_SEQUENCE(data[offset:], '代理服务器')
    offset += 1
    for proxy_count in range(proxy_num):
        offset += take_TSA(data[offset:], '目标服务器地址:')
        offset += take_long_unsigned(data[offset:], '代理一个服务器的超时时间:')
        oad_num = get_num_of_SEQUENCE(data[offset:], '对象属性的设置后读取')
        offset += 1
        for oad_count in range(oad_num):
            offset += take_OAD(data[offset:])
            offset += take_Data(data[offset:])
            offset += take_OAD(data[offset:])
            offset += take_unsigned(data[offset:], '延时读取时间:')
    return offset


def pro0905(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_long_unsigned(data[offset:], '整个代理请求的超时时间:')
    proxy_num = get_num_of_SEQUENCE(data[offset:], '代理服务器')
    offset += 1
    for proxy_count in range(proxy_num):
        offset += take_TSA(data[offset:], '目标服务器地址:')
        offset += take_long_unsigned(data[offset:], '代理一个服务器的超时时间:')
        oad_num = get_num_of_SEQUENCE(data[offset:], 'OAD及其参数')
        offset += 1
        for oad_count in range(oad_num):
            offset += take_OMD(data[offset:])
            offset += take_Data(data[offset:])
    return offset


def pro0906(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_long_unsigned(data[offset:], '整个代理请求的超时时间:')
    proxy_num = get_num_of_SEQUENCE(data[offset:], '代理服务器')
    offset += 1
    for proxy_count in range(proxy_num):
        offset += take_TSA(data[offset:], '目标服务器地址:')
        offset += take_long_unsigned(data[offset:], '代理一个服务器的超时时间:')
        oad_num = get_num_of_SEQUENCE(data[offset:], '对象方法及属性的操作后读取')
        offset += 1
        for oad_count in range(oad_num):
            offset += take_OMD(data[offset:])
            offset += take_Data(data[offset:])
            offset += take_OAD(data[offset:])
            offset += take_unsigned(data[offset:], '延时读取时间:')
    return offset


def pro0907(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_OAD(data[offset:])
    offset += take_COMDCB(data[offset:], '端口通信控制块:')
    offset += take_long_unsigned(data[offset:], '接收等待报文超时时间（秒）:')
    offset += take_long_unsigned(data[offset:], '接收等待字节超时时间（毫秒）:')
    offset += take_octect_string(data[offset:], '透明转发命令')
    return offset


def pro8901(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    proxy_num = get_num_of_SEQUENCE(data[offset:], '代理服务器的读取结果')
    offset += 1
    for proxy_count in range(proxy_num):
        offset += take_TSA(data[offset:])
        oad_num = get_num_of_SEQUENCE(data[offset:], 'OAD及其结果')
        offset += 1
        for oad_count in range(oad_num):
            offset += take_OAD(data[offset:])
            offset += take_Get_Result(data[offset:])
    return offset


def pro8902(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    offset += take_TSA(data[offset:])
    offset += take_A_ResultRecord(data[offset:])
    return offset


def pro8903(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    proxy_num = get_num_of_SEQUENCE(data[offset:], '代理服务器的读取结果')
    offset += 1
    for proxy_count in range(proxy_num):
        offset += take_TSA(data[offset:])
        set_result_num = get_num_of_SEQUENCE(data[offset:], '对象属性设置结果')
        offset += 1
        for set_result_count in range(set_result_num):
            offset += take_OAD(data[offset:])
            dar = get_DAR(data[offset])
            output(' —— 设置结果:' + dar)
            offset += 1
    return offset


def pro8904(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    proxy_num = get_num_of_SEQUENCE(data[offset:], '代理服务器的读取结果')
    offset += 1
    for proxy_count in range(proxy_num):
        offset += take_TSA(data[offset:])
        set_result_num = get_num_of_SEQUENCE(data[offset:], '对象属性设置后读取结果')
        offset += 1
        for set_result_count in range(set_result_num):
            offset += take_OAD(data[offset:])
            dar = get_DAR(data[offset])
            output(' —— 设置结果:' + dar)
            offset += 1
            offset += take_OAD(data[offset:])
            offset += take_Get_Result(data[offset:])
    return offset


def pro8905(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    proxy_num = get_num_of_SEQUENCE(data[offset:], '代理服务器的读取结果')
    offset += 1
    for proxy_count in range(proxy_num):
        offset += take_TSA(data[offset:])
        set_result_num = get_num_of_SEQUENCE(data[offset:], '对象属性设置后读取结果')
        offset += 1
        for set_result_count in range(set_result_num):
            offset += take_OMD(data[offset:])
            dar = get_DAR(data[offset])
            output(' —— 操作结果:' + dar)
            offset += 1
            optional = data[offset]
            offset += take_OPTIONAL(data[offset:], '操作返回数据')
            if optional == '01':
                offset += take_Data(data[offset:])
    return offset


def pro8906(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    proxy_num = get_num_of_SEQUENCE(data[offset:], '代理服务器的读取结果')
    offset += 1
    for proxy_count in range(proxy_num):
        offset += take_TSA(data[offset:])
        set_result_num = get_num_of_SEQUENCE(data[offset:], '对象属性设置后读取结果')
        offset += 1
        for set_result_count in range(set_result_num):
            offset += take_OMD(data[offset:])
            dar = get_DAR(data[offset])
            output(' —— 操作结果:' + dar)
            offset += 1
            optional = data[offset]
            offset += take_OPTIONAL(data[offset:], '操作返回数据')
            if optional == '01':
                offset += take_Data(data[offset:])
            offset += take_OAD(data[offset:])
            offset += take_Get_Result(data[offset:])
    return offset


def pro8907(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    offset += take_OAD(data[offset:])
    trans_result_choice = data[offset]
    if trans_result_choice == '00':
        show_data_source(data[offset:], 2)
        dar = get_DAR(data[offset + 1])
        output(' —— 错误信息:' + dar)
        offset += 2
    elif trans_result_choice == '01':
        show_data_source(data[offset:], 1)
        output(' —— 返回数据')
        offset += 1
        offset += take_octect_string(data[offset:])
    return offset
