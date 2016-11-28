from shared_functions import *  # NOQA


def ProxyGetRequestList(data):
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


def ProxyGetRequestRecord(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_long_unsigned(data[offset:], '代理请求的超时时间:')
    offset += take_TSA(data[offset:], '目标服务器地址:')
    offset += take_OAD(data[offset:])
    offset += take_RSD(data[offset:])
    offset += take_RCSD(data[offset:])
    return offset


def ProxySetRequestList(data):
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


def ProxySetThenGetRequestList(data):
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


def ProxyActionRequestList(data):
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


def ProxyActionThenGetRequestList(data):
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


def ProxyTransCommandRequest(data):
    offset = 0
    offset += take_PIID(data[offset:])
    offset += take_OAD(data[offset:])
    offset += take_COMDCB(data[offset:], '端口通信控制块:')
    offset += take_long_unsigned(data[offset:], '接收等待报文超时时间（秒）:')
    offset += take_long_unsigned(data[offset:], '接收等待字节超时时间（毫秒）:')
    offset += take_octect_string(data[offset:], '透明转发命令')
    return offset


def ProxyGetResponseList(data):
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


def ProxyGetResponseRecord(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    offset += take_TSA(data[offset:])
    offset += take_A_ResultRecord(data[offset:])
    return offset


def ProxySetResponseList(data):
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
            offset += take_DAR(data[offset:], '设置结果')
    return offset


def ProxySetThenGetResponseList(data):
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
            offset += take_DAR(data[offset:], '设置结果')
            offset += take_OAD(data[offset:])
            offset += take_Get_Result(data[offset:])
    return offset


def ProxyActionResponseList(data):
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
            offset += take_DAR(data[offset:], '操作结果')
            optional = data[offset]
            offset += take_OPTIONAL(data[offset:], '操作返回数据')
            if optional == '01':
                offset += take_Data(data[offset:])
    return offset


def ProxyActionThenGetResponseList(data):
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
            offset += take_DAR(data[offset:], '操作结果')
            optional = data[offset]
            offset += take_OPTIONAL(data[offset:], '操作返回数据')
            if optional == '01':
                offset += take_Data(data[offset:])
            offset += take_OAD(data[offset:])
            offset += take_Get_Result(data[offset:])
    return offset


def ProxyTransCommandResponse(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    offset += take_OAD(data[offset:])
    trans_result_choice = data[offset]
    if trans_result_choice == '00':
        show_data_source(data[offset:], 2)
        offset += take_DAR(data[offset + 1:], '错误信息') + 1
    elif trans_result_choice == '01':
        show_data_source(data[offset:], 1)
        output(' —— 返回数据')
        offset += 1
        offset += take_octect_string(data[offset:])
    return offset
