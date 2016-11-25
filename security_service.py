from shared_functions import *  # NOQA


def security_request(data):
    offset = 0
    security_choice = data[offset]
    offset += 1
    offset += take_octect_string(data[offset:], '明文应用数据单元' if security_choice == 0 else '密文应用数据单元')
    security_choice = data[offset]
    offset += 1
    offset += {
        '00': take_SID_MAC,
        '01': take_RN,
        '02': take_RN_MAC,
        '03': take_SID,
    }[security_choice](data[offset:], '(数据验证信息)')
    return offset


def security_response(data):
    offset = 0
    security_choice = data[offset]
    offset += 1
    if security_choice == '00':
        offset += take_octect_string(data[offset:], '明文应用数据单元')
    elif security_choice == '01':
        offset += take_octect_string(data[offset:], '密文应用数据单元')
    elif security_choice == '02':
        dar = get_DAR(data[offset + 1])
        show_data_source(data[offset:], 2)
        output(' —— 异常错误:' + dar)
        offset += 2
    optional = data[offset]
    offset += take_OPTIONAL(data[offset:], '数据验证信息')
    if optional == '01':
        check_choice = data[offset]
        show_data_source(data[offset:], 1)
        output(' —— 数据验证方式:数据MAC')
        offset += 1
        if check_choice == '00':
            offset += take_MAC(data[offset:])
    return offset
