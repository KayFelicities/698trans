import config
from config import pathname
import os


# 文字输出
def output(text, newline=True):
    config.text_test += text
    if newline is True:
        config.text_test += '\n'
    return 0


# 输出原始报文
def show_data_source(data, len):
    source_text = ''
    for count in range(len):
        source_text += data[count] + ' '
    output(source_text, False)


def take_service_type(data):
    offset = 0
    file_path = os.path.join(pathname, '698APDUConfig.ini')
    file_handle = open(file_path, 'rb')
    file_lines = file_handle.readlines()
    file_handle.close()
    service_type = data[offset]
    service_explain = ' —— '
    for service_line in file_lines:
        if int(service_line.decode('utf-8').split('=')[0]) == int(service_type, 16):
            service_explain += service_line.decode('utf-8').split('=')[1].split('\n')[0].split('\r')[0]
            break
    if service_type not in ['01', '02', '03', '10', '81', '82', '83', '84', '90']:
        service_type += data[offset + 1]
        service_explain += ', ' + service_line.decode('utf-8').split('=')[int(data[offset + 1], 16) + 1].split('\n')[0].split('\r')[0]
        show_data_source(data[offset:], 2)
        offset += 2
    else:
        show_data_source(data[offset:], 1)
        offset += 1
    output(service_explain)
    return offset, service_type


def take_FollowReport(data, add_text=''):
    offset = 0
    follow_report_option = data[offset]
    offset += take_OPTIONAL(data[offset:], '跟随上报信息域')
    if follow_report_option == '01':
        follow_report_choice = data[offset]
        show_data_source(data[offset:], 1)
        if follow_report_choice == '01':
            result_normal_num = get_num_of_SEQUENCE(data[offset:], '对象属性及其数据')
            offset += 1
            for result_normal_count in range(result_normal_num):
                offset += take_A_ResultNormal(data[offset:])
        elif follow_report_choice == '02':
            result_record_num = get_num_of_SEQUENCE(data[offset:], '对象属性及其数据')
            offset += 1
            for result_record_count in range(result_record_num):
                offset += take_A_ResultRecord(data[offset:])
    return offset


def take_TimeTag(data, add_text=''):
    offset = 0
    timetag_option = data[offset]
    offset += take_OPTIONAL(data[offset:], '时间标签')
    if timetag_option == '01':
        offset += take_date_time_s(data[offset:], '发送时标')
        offset += take_TI(data[offset:], '允许传输延时时间')
    return offset


def take_PIID(data, add_text=''):
    offset = 0
    piid = int(data[offset], 16)
    service_priority = '一般的, ' if piid >> 7 == 0 else '高级的, '
    invoke_id = piid & 0x3f
    show_data_source(data[offset:], 1)
    output(' —— PIID(服务优先级:' + service_priority + '服务序号:' + str(invoke_id) + ')')
    offset += 1
    return offset


def take_PIID_ACD(data, add_text=''):
    offset = 0
    piid_acd = int(data[offset], 16)
    service_priority = '一般的, ' if piid_acd >> 7 == 0 else '高级的, '
    ACD = '不请求访问, ' if (piid_acd >> 6) & 0x01 == 0 else '请求访问, '
    invoke_id = piid_acd & 0x3f
    show_data_source(data[offset:], 1)
    output(' —— PIID-ACD(服务优先级:' + service_priority + ACD + '服务序号:' + str(invoke_id) + ')')
    offset += 1
    return offset


def take_OPTIONAL(data, add_text=''):
    offset = 0
    optional = '有(OPTIONAL)' if data[offset] == '01' else '无(OPTIONAL)'
    show_data_source(data[offset:], 1)
    output(' —— ' + add_text + ':' + optional)
    offset += 1
    return offset


def take_CHOICE(data, add_text='', choice_dict=None):
    offset = 0
    choice = data[offset]
    show_data_source(data[offset:], 1)
    if choice_dict is not None:
        choice_explain = choice_dict[choice]
        output(' —— ' + add_text + '(CHOICE' + choice + ':' + choice_explain + ')')
    output(' —— ' + add_text + '(CHOICE)')
    offset += 1
    return offset


def get_num_of_SEQUENCE(data, SEQUENCE_text=''):
    num = int(data[0], 16)
    show_data_source(data, 1)
    output(' —— ' + SEQUENCE_text + '*' + str(num))
    return num


def get_len_of_octect_string(data):
    offset = 0
    len_flag = int(data[offset], 16)
    offset += 1
    if len_flag >> 7 == 0:  # 单字节长度
        return len_flag, offset
    else:
        len_of_len = len_flag & 0x7f
        string_len = ''
        for count in range(len_of_len):
            string_len += data[offset + count]
        offset += len_of_len
        print('string_len:', string_len)
        return int(string_len, 16), offset


def take_DAR(data, add_text=''):
    offset = 0
    file_path = os.path.join(pathname, '698ErrIDConfig.ini')
    file_handle = open(file_path, 'rb')
    file_lines = file_handle.readlines()
    file_handle.close()
    dar_explain = ''
    for dar_line in file_lines:
        if dar_line.decode('utf-8')[0:2] == data[0]:
            dar_explain = dar_line.decode('utf-8')[3:].split('\n')[0]
            break
    show_data_source(data[offset:], 1)
    output(' —— ' + add_text + ':' + dar_explain)
    offset += 1
    return offset


def take_A_ResultNormal(data, add_text=''):
    offset = 0
    offset += take_OAD(data[offset:])
    offset += take_Get_Result(data[offset:])
    return offset


def take_Get_Result(data, add_text=''):
    offset = 0
    result = data[offset]
    if result == '00':  # 错误信息
        show_data_source(data[offset:], 1)
        offset += 1
        offset += take_DAR(data[offset:], 'DAR')
    elif result == '01':  # 数据
        show_data_source(data[offset:], 1)
        output(' —— 数据')
        offset += 1
        offset += take_Data(data[offset:])
    return offset


def take_A_ResultRecord(data, add_text=''):
    offset = 0
    offset += take_OAD(data[offset:])
    temp_offset, csd_num = take_RCSD(data[offset:])
    offset += temp_offset
    re_data_choice = data[offset]
    if re_data_choice == '00':
        show_data_source(data[offset:], 1)
        offset += 1
        offset += take_DAR(data[offset:], '错误信息')
    elif re_data_choice == '01':  # M条记录
        record_num = int(data[offset + 1], 16)
        show_data_source(data[offset:], 2)
        output(' —— ' + str(record_num) + '条记录')
        offset += 2
        for record_count in range(record_num):
            for csd_count in range(csd_num):
                offset += take_Data(data[offset:])
    return offset


def take_GetRecord(data, add_text=''):
    offset = 0
    offset += take_OAD(data[offset:])
    offset += take_RSD(data[offset:])  # RSD
    temp_offset, temp = take_RCSD(data[offset:])  # RCSD处理
    offset += temp_offset
    return offset


def take_ConnectMechanismInfo(data, add_text=''):
    offset = 0
    connect_choice = data[offset]
    show_data_source(data[offset:], 1)
    output(' —— ' + {
        '00': '公共连接',
        '01': '一般密码',
        '02': '对称加密',
        '03': '数字签名',
    }[connect_choice])
    offset += 1
    if connect_choice == '00':
        offset += take_NULL(data[offset:], 'NullSecurity:')
    elif connect_choice == '01':
        offset += take_visible_string(data[offset:], 'PasswordSecurity:')
    elif connect_choice == '02':
        offset += take_octect_string(data[offset:], '密文1')
        offset += take_octect_string(data[offset:], '客户机签名1')
    elif connect_choice == '03':
        offset += take_octect_string(data[offset:], '密文2')
        offset += take_octect_string(data[offset:], '客户机签名2')
    return offset


def take_ConnectResponseInfo(data, add_text=''):
    offset = 0
    connect_result = {
        '00': '允许建立应用连接',
        '01': '密码错误',
        '02': '对称解密错误',
        '03': '非对称解密错误',
        '04': '签名错误',
        '05': '协议版本不匹配',
        'FF': '其他错误'
    }[data[offset]]
    show_data_source(data[offset:], 1)
    output(' —— 认证结果:' + connect_result)
    offset += 1
    optional = data[offset]
    offset += take_OPTIONAL(data[offset:], '认证附加信息')
    if optional == '01':
        offset += take_RN(data[offset:], '服务器随机数:')
        offset += take_octect_string(data[offset:], '服务器签名信息')
    return offset


def take_FactoryVersion(data, add_text=''):
    offset = 0
    offset += take_visible_string(data[offset:], '厂商代码:', 4)
    offset += take_visible_string(data[offset:], '软件版本号:', 4)
    offset += take_visible_string(data[offset:], '软件版本日期:', 6)
    offset += take_visible_string(data[offset:], '硬件版本号:', 4)
    offset += take_visible_string(data[offset:], '硬件版本日期:', 6)
    offset += take_visible_string(data[offset:], '厂家扩展信息:', 8)
    return offset


# ############################ 数据类型处理 #############################
def take_Data(data, add_text=''):
    offset = 0
    if data[offset] == '00':    # 对null类型特殊处理
        offset += take_NULL(data[offset:])
        return offset
    show_data_source(data[offset:], 1)
    print(data[0])
    offset += 1
    offset += {
        '00': take_NULL,
        '01': take_array,
        '02': take_structure,
        '03': take_bool,
        '04': take_bit_string,
        '05': take_double_long,
        '06': take_double_long_unsigned,
        '09': take_octect_string,
        '0A': take_visible_string,
        '0C': take_UTF8_string,
        '0F': take_integer,
        '10': take_long,
        '11': take_unsigned,
        '12': take_long_unsigned,
        '14': take_long64,
        '15': take_long64_unsigned,
        '16': take_enum,
        '17': take_float32,
        '18': take_float64,
        '19': take_date_time,
        '1A': take_date,
        '1B': take_time,
        '1C': take_date_time_s,
        '50': take_OI,
        '51': take_OAD,
        '52': take_ROAD,
        '53': take_OMD,
        '54': take_TI,
        '55': take_TSA,
        '56': take_MAC,
        '57': take_RN,
        '58': take_Region,
        '59': take_Scaler_Unit,
        '5A': take_RSD,
        '5B': take_CSD,
        '5C': take_MS,
        '5D': take_SID,
        '5E': take_SID_MAC,
        '5F': take_COMDCB,
        '60': take_RCSD,
    }[data[offset - 1]](data[offset:])
    return offset


def take_NULL(data, add_text=''):
    offset = 0
    show_data_source(data, 1)
    offset += 1
    output(' —— ' + add_text + '(NULL)')
    return offset


def take_array(data, add_text=''):
    offset = 0
    structure_num = int(data[offset], 16)
    show_data_source(data[offset:], 1)
    output(' —— ' + add_text + 'array, 元素个数:' + str(structure_num))
    offset += 1
    for count in range(structure_num):
        offset += take_Data(data[offset:])
    return offset


def take_structure(data, add_text=''):
    offset = 0
    structure_num = int(data[offset], 16)
    show_data_source(data[offset:], 1)
    output(' —— ' + add_text + 'structure, 成员个数:' + str(structure_num))
    offset += 1
    for count in range(structure_num):
        offset += take_Data(data[offset:])
    return offset


def take_bool(data, add_text=''):
    offset = 0
    show_data_source(data, 1)
    bool_value = ':False' if data[offset] == 0 else ':True'
    output(' —— ' + add_text + bool_value + '(bool)')
    offset += 1
    return offset


def take_bit_string(data, add_text='', bit_len=None):
    offset = 0
    if bit_len is None:
        bit_len = int(data[offset], 16)
        show_data_source(data[offset:], 1)
        offset += 1
    byte_len = bit_len // 8 if bit_len % 8 == 0 else bit_len // 8 + 1
    show_data_source(data[offset:], byte_len)
    bit_string_text = ''
    for count in range(byte_len):
        bit_string_text += data[offset + count]
    output(' —— ' + add_text + str(bin(int(bit_string_text, 16))) + '(bit-string,长度' + str(bit_len) + ')')
    return offset


def take_double_long(data, add_text=''):
    offset = 0
    show_data_source(data, 4)
    if int(data[offset], 16) >> 7 == 1:  # 负数
        value = int(str(int(data[offset]) & 0x7f) + data[offset + 1] +
                    data[offset + 2] + data[offset + 3], 16) * (-1)
    else:
        value = int(data[offset] + data[offset + 1] + data[offset + 2] + data[offset + 3], 16)
    output(' —— ' + add_text + str(value) + '(double_long)')
    offset += 4
    return offset


def take_double_long_unsigned(data, add_text=''):
    offset = 0
    show_data_source(data, 4)
    output(' —— ' + add_text + str(int(data[offset] + data[offset + 1] + data[offset + 2] + data[offset + 3], 16)) + '(double_long_unsigned)')
    offset += 4
    return offset


def take_octect_string(data, add_text='', string_len=None):
    offset = 0
    if string_len is None:
        string_len, offset = get_len_of_octect_string(data[offset:])
        show_data_source(data[:offset], offset)
    show_data_source(data[offset:], string_len)
    output(' —— ' + add_text + '(octect_string,长度' + str(string_len) + ')')
    offset += string_len
    return offset


def take_visible_string(data, add_text='', string_len=None):
    offset = 0
    if string_len is None:
        string_len, offset = get_len_of_octect_string(data[offset:])
        show_data_source(data[:offset], offset)
    show_data_source(data[offset:], string_len)
    visible_string = ''
    for char in data[offset: offset + string_len]:
        visible_string += chr(int(char, 16))
    output(' —— ' + add_text + visible_string + '(visible_string,长度' + str(string_len) + ')')
    offset += string_len
    return offset


def take_UTF8_string(data, add_text=''):
    offset = 0
    print('未定义\n')
    return offset


def take_integer(data, add_text=''):
    offset = 0
    show_data_source(data, 1)
    if int(data[offset], 16) >> 7 == 1:  # 负数
        value = int(str(int(data[offset]) & 0x7f), 16) * (-1)
    else:
        value = int(data[offset], 16)
    output(' —— ' + add_text + str(value) + '(integer)')
    offset += 1
    return offset


def take_long(data, add_text=''):
    offset = 0
    show_data_source(data, 2)
    if int(data[offset], 16) >> 7 == 1:  # 负数
        value = int(str(int(data[offset]) & 0x7f) + data[offset + 1], 16) * (-1)
    else:
        value = int(data[offset] + data[offset + 1], 16)
    output(' —— ' + add_text + str(value) + '(long)')
    offset += 2
    return offset


def take_unsigned(data, add_text=''):
    offset = 0
    show_data_source(data, 1)
    output(' —— ' + add_text + str(int(data[offset], 16)) + '(unsigned)')
    offset += 1
    return offset


def take_long_unsigned(data, add_text=''):
    offset = 0
    show_data_source(data, 2)
    output(' —— ' + add_text + str(int(data[offset] + data[offset + 1], 16)) + '(long_unsigned)')
    offset += 2
    return offset


def take_long64(data, add_text=''):
    offset = 0
    show_data_source(data, 8)
    if int(data[offset], 16) >> 7 == 1:  # 负数
        value = int(str(int(data[offset]) & 0x7f) + data[offset + 1] +
                    data[offset + 2] + data[offset + 3] + data[offset + 4] + data[offset + 5] + data[offset + 6] + data[offset + 7], 16) * (-1)
    else:
        value = int(data[offset] + data[offset + 1] + data[offset + 2] + data[offset + 3] + data[offset + 4] + data[offset + 5] + data[offset + 6] + data[offset + 7], 16)
    output(' —— ' + add_text + str(value) + '(long64)')
    offset += 8
    return offset


def take_long64_unsigned(data, add_text=''):
    offset = 0
    show_data_source(data, 8)
    value = int(data[offset] + data[offset + 1] + data[offset + 2] + data[offset + 3] + data[offset + 4] + data[offset + 5] + data[offset + 6] + data[offset + 7], 16)
    output(' —— ' + add_text + str(value) + '(long64_unsigned)')
    offset += 8
    return offset


def take_enum(data, add_text=''):
    offset = 0
    show_data_source(data, 1)
    output(' —— ' + add_text + str(int(data[offset], 16)) + '(enum)')
    offset += 1
    return offset


def take_float32(data, add_text=''):
    offset = 0
    show_data_source(data, 4)
    if int(data[offset], 16) >> 7 == 1:  # 负数
        value = int(str(int(data[offset]) & 0x7f) + data[offset + 1] +
                    data[offset + 2] + data[offset + 3], 16) * (-1)
    else:
        value = int(data[offset] + data[offset + 1] + data[offset + 2] + data[offset + 3], 16)
    output(' —— ' + add_text + str(value) + '(float32)')
    offset += 4
    return offset


def take_float64(data, add_text=''):
    offset = 0
    show_data_source(data, 8)
    if int(data[offset], 16) >> 7 == 1:  # 负数
        value = int(str(int(data[offset]) & 0x7f) + data[offset + 1] +
                    data[offset + 2] + data[offset + 3] + data[offset + 4] + data[offset + 5] + data[offset + 6] + data[offset + 7], 16) * (-1)
    else:
        value = int(data[offset] + data[offset + 1] + data[offset + 2] + data[offset + 3] + data[offset + 4] + data[offset + 5] + data[offset + 6] + data[offset + 7], 16)
    output(' —— ' + add_text + str(value) + '(float64)')
    offset += 8
    return offset


def take_date_time(data, add_text=''):
    offset = 0
    year = int(data[0] + data[1], 16)
    month = int(data[2], 16)
    day = int(data[3], 16)
    hour = int(data[5], 16)
    minute = int(data[6], 16)
    second = int(data[7], 16)
    milliseconds = int(data[8] + data[9], 16)
    show_data_source(data, 10)
    output(' —— ' + add_text + '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}:{6:03d}'
           .format(year, month, day, hour, minute, second, milliseconds) + '(date_time)')
    offset += 10
    return offset


def take_date(data, add_text=''):
    offset = 0
    year = int(data[0] + data[1], 16)
    month = int(data[2], 16)
    day = int(data[3], 16)
    # week = int(data[4], 16)
    show_data_source(data, 5)
    output(' —— ' + add_text + '{0:04d}-{1:02d}-{2:02d}'.format(year, month, day) + '(date)')
    offset += 5
    return offset


def take_time(data, add_text=''):
    offset = 0
    hour = int(data[0], 16)
    minute = int(data[1], 16)
    second = int(data[2], 16)
    show_data_source(data, 3)
    output(' —— ' + add_text + '{0:02d}:{1:02d}:{2:02d}'.format(hour, minute, second) + '(time)')
    offset += 3
    return offset


def take_date_time_s(data, add_text=''):
    offset = 0
    year = int(data[0] + data[1], 16)
    month = int(data[2], 16)
    day = int(data[3], 16)
    hour = int(data[4], 16)
    minute = int(data[5], 16)
    second = int(data[6], 16)
    show_data_source(data, 7)
    output(' —— ' + add_text + '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'
           .format(year, month, day, hour, minute, second) + '(date_time_s)')
    offset += 7
    return offset


def take_OI(data, add_text=''):
    offset = 0
    file_path = os.path.join(pathname, '698DataIDConfig.ini')
    file_handle = open(file_path, 'rb')
    file_lines = file_handle.readlines()
    file_handle.close()
    OI = data[offset] + data[offset + 1]
    OI_explain = ''
    for OI_line in file_lines:
        if OI_line.decode('utf-8')[0:4] == OI:
            OI_explain = OI_line.decode('utf-8')[8:].split('=')[0].split('\r\n')[0]
            break
    # print('OI_explain:', OI_explain, 'over')
    show_data_source(data, 2)
    output(' —— ' + add_text + OI_explain + '(OI)')
    offset += 2
    return offset


def take_OAD(data, add_text=''):
    offset = 0
    file_path = os.path.join(pathname, '698DataIDConfig.ini')
    file_handle = open(file_path, 'rb')
    file_lines = file_handle.readlines()
    file_handle.close()
    OI = data[offset] + data[offset + 1]
    OI_explain = ''
    for OI_line in file_lines:
        if OI_line.decode('utf-8')[0:4] == OI:
            OI_explain = OI_line.decode('utf-8')[8:].split('=')[0].split('\r\n')[0]
            break
    # print('OI_explain:', OI_explain, 'over')
    show_data_source(data[offset:], 2)
    offset += 2
    attr = int(data[offset], 16)
    index = int(data[offset + 1], 16)
    show_data_source(data[offset:], 2)
    output(' —— ' + add_text + OI_explain + ', 属性' + str(attr) + ', 索引' + str(index) + '(OAD)')
    offset += 2
    return offset


def take_ROAD(data, add_text=''):
    offset = 0
    offset += take_OAD(data[offset:],)
    oad_num = int(data[offset], 16)
    show_data_source(data[offset:], 1)
    output(' —— 关联OAD*' + str(oad_num))
    offset += 1
    for oad_count in range(oad_num):
        offset += take_OAD(data[offset:],)
    return offset


def take_OMD(data, add_text=''):
    offset = 0
    file_path = os.path.join(pathname, '698DataIDConfig.ini')
    file_handle = open(file_path, 'rb')
    file_lines = file_handle.readlines()
    file_handle.close()
    OI = data[offset] + data[offset + 1]
    OI_explain = ''
    for OI_line in file_lines:
        if OI_line.decode('utf-8')[0:4] == OI:
            OI_explain = OI_line.decode('utf-8')[8:].split('=')[0].split('\r\n')[0]
            break
    # print('OI_explain:', OI_explain, 'over')
    show_data_source(data[offset:], 2)
    offset += 2
    attr = int(data[offset], 16)
    index = int(data[offset + 1], 16)
    show_data_source(data[offset:], 2)
    output(' —— ' + add_text + OI_explain + ', 方法' + str(attr) + ', 操作模式' + str(index) + '(OMD)')
    offset += 2
    return offset


def take_TI(data, add_text=''):
    offset = 0
    TI_uint = {
        '00': '秒',
        '01': '分',
        '02': '时',
        '03': '日',
        '04': '月',
        '05': '年',
    }[data[offset]]
    TI_value = int(data[offset + 1] + data[offset + 2], 16)
    show_data_source(data[offset:], 3)
    output(' —— ' + add_text + str(TI_value) + TI_uint + '(TI)')
    offset = 3
    return offset


def take_TSA(data, add_text=''):
    # print('Kay, take_TSA data:', data)
    offset = 0
    TSA_len = int(data[offset], 16)
    addr_len = int(data[offset + 1], 16)
    show_data_source(data[offset:], 1 + TSA_len)
    addr_text = ''
    for tsa_count in range(addr_len + 1):
        addr_text += data[offset + 2 + tsa_count]
    output(' —— ' + add_text + addr_text + '(TSA)')
    offset += 1 + TSA_len
    return offset


def take_MAC(data, add_text=''):
    offset = 0
    offset += take_octect_string(data[offset:], 'MAC')
    return offset


def take_RN(data, add_text=''):
    offset = 0
    offset += take_octect_string(data[offset:], 'RN')
    return offset


def take_RN_MAC(data, add_text=''):
    offset = 0
    offset += take_octect_string(data[offset:], 'RN')
    offset += take_octect_string(data[offset:], 'MAC')
    return offset


def take_Region(data, add_text=''):
    offset = 0
    uint = {
        '00': '前闭后开',
        '01': '前开后闭',
        '02': '前闭后闭',
        '03': '前开后开',
    }[data[offset]]
    show_data_source(data[offset:], 1)
    output(' —— ' + uint)
    offset += 1
    offset += take_Data(data, add_text='起始值')
    offset += take_Data(data, add_text='结束值')
    return offset


def take_Scaler_Unit(data, add_text=''):
    offset = 0
    offset += take_integer(data[offset:], '换算:')
    offset += take_enum(data[offset:], '单位:')
    return offset


def take_RSD(data, add_text=''):
    offset = 0
    # print(data[:])
    show_data_source(data[offset:], 1)
    selector = data[offset]
    output(' —— Selector' + selector)
    offset += 1
    if selector == '00':
        offset += take_NULL(data[offset:], '不选择')
    elif selector == '01':
        offset += take_OAD(data[offset:])
        offset += take_Data(data[offset:], '数值')
    elif selector == '02':
        offset += take_OAD(data[offset:])
        offset += take_Data(data[offset:], '起始值')
        offset += take_Data(data[offset:], '结束值')
        offset += take_Data(data[offset:], '数据间隔')
    elif selector == '03':
        selector2_count = int(data[offset], 16)
        offset += 1
        for count in range(selector2_count):
            offset += take_OAD(data[offset:])
            offset += take_Data(data[offset:], '起始值:')
            offset += take_Data(data[offset:], '结束值:')
            offset += take_Data(data[offset:], '数据间隔:')
    elif selector in ['04', '05']:
        offset += take_date_time_s(data[offset:], '采集启动时间:' if selector == '04' else '采集存储时间:')
        offset += take_MS(data[offset:], '数值:')
    elif selector in ['06', '07', '08']:
        type_text = {
            '06': '采集启动时间',
            '07': '采集存储时间',
            '08': '采集成功时间',
        }[selector]
        offset += take_date_time_s(data[offset:], type_text + '起始值:')
        offset += take_date_time_s(data[offset:], type_text + '结束值:')
        offset += take_TI(data[offset:])
        offset += take_MS(data[offset:])
    elif selector == '09':
        offset += take_unsigned(data[offset:], '上第n次记录:')
    elif selector == '0A':
        offset += take_unsigned(data[offset:], '上n条记录:')
        offset += take_MS(data[offset:])
    return offset


def take_CSD(data, add_text=''):
    offset = 0
    csd_choice = data[offset]
    show_data_source(data[offset:], 1)
    output(' —— OAD' if csd_choice == '00' else ' —— ROAD')
    offset += 1
    if csd_choice == '00':
        offset += take_OAD(data[offset:])
    elif csd_choice == '01':
        offset += take_ROAD(data[offset:])
    return offset


def take_MS(data, add_text=''):
    offset = 0
    MS_choice = data[0]
    if MS_choice == '00':  # 无电能表
        offset += take_NULL(data[offset:], '无电能表')
    elif MS_choice == '01':  # 全部用户地址
        offset += take_NULL(data[offset:], '全部用户地址')
    elif MS_choice == '02':  # 一组用户类型
        num = int(data[1], 16)
        show_data_source(data[offset:], 2)
        offset += 2
        output(' —— 用户类型*' + str(num))
        for count in range(num):
            offset += take_unsigned(data[offset:], '用户类型:')
    elif MS_choice == '03':  # 一组用户地址
        num = int(data[1], 16)
        show_data_source(data, 2)
        offset += 2
        output(' —— 用户地址*' + str(num))
        for count in range(num):
            offset += take_TSA(data[offset:])
    elif MS_choice == '04':  # 一组配置序号
        num = int(data[1], 16)
        show_data_source(data, 2)
        offset += 2
        output(' —— 配置序号*' + str(num))
        for count in range(num):
            offset += take_long_unsigned(data[offset:], '配置序号:')
    elif MS_choice == '05':  # 一组用户类型区间
        offset = 0
        num = int(data[1], 16)
        show_data_source(data, 2)
        offset += 2
        output(' —— 用户类型区间*' + str(num))
        for count in range(num):
            offset += take_Region(data[offset:], '用户类型区间:')
    elif MS_choice == '06':  # 一组用户地址区间
        offset = 0
        num = int(data[1], 16)
        show_data_source(data, 2)
        offset += 2
        output(' —— 用户地址区间*' + str(num))
        for count in range(num):
            offset += take_Region(data[offset:], '用户地址区间:')
    elif MS_choice == '07':  # 一组配置序号区间
        offset = 0
        num = int(data[1], 16)
        show_data_source(data, 2)
        offset += 2
        output(' —— 配置序号区间*' + str(num))
        for count in range(num):
            offset += take_Region(data[offset:], '配置序号区间:')
    return offset


def take_SID(data, add_text=''):
    offset = 0
    offset += take_double_long_unsigned(data[offset:], '标识:')
    print(data[offset:])
    offset += take_octect_string(data[offset:], '附加数据')
    return offset


def take_SID_MAC(data, add_text=''):
    offset = 0
    offset += take_SID(data[offset:])
    offset += take_MAC(data[offset:])
    return offset


def take_COMDCB(data, add_text=''):
    offset = 0
    print('未定义\n')
    return offset


def take_RCSD(data, add_text=''):
    offset = 0
    csd_num = int(data[offset], 16)
    show_data_source(data[offset:], 1)
    output(' —— CSD*' + str(csd_num))
    offset += 1
    for csd_count in range(csd_num):
        offset += take_CSD(data[offset:])
    return offset, csd_num
