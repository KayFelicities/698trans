'''shared functions'''
import config
import data_translate


# 文字输出
def output(text, newline=True):
    config.output_text += text
    if newline is True:
        config.output_text += '\n'
    return 0


# 输出原始报文
def show_data_source(data, len, level=0, end_flag=0):
    if config.show_level is True:
        source_text = '   ' * (level - 1) + ('' if level == 0 else '|  ' if end_flag == 0 else '└ ')
    else:
        source_text = ''
    for count in range(len):
        source_text += data[count] + ' '
    output(source_text, False)


def take_service_type(data, end_flag=0):
    offset = 0
    service_type = data[offset]
    if service_type not in ['01', '02', '03', '10', '81', '82', '83', '84', '90']:
        service_type += data[offset + 1]
        show_data_source(data[offset:], 2)
        offset += 2
    else:
        show_data_source(data[offset:], 1)
        offset += 1
    try:
        explain = ' —— ' + data_translate.service_explain[service_type]
    except Exception:
        explain = ' —— ' + '未知服务'
    output(explain)
    return offset, service_type


def take_FollowReport(data, add_text='', end_flag=0):
    offset = 0
    follow_report_option = data[offset]
    offset += take_OPTIONAL(data[offset:], '跟随上报信息域')
    if follow_report_option == '01':
        follow_report_choice = data[offset]
        offset += take_CHOICE(data[offset:], '', choice_dict={'01': '对象属性及其数据', '02': '记录型对象属性及其数据'})
        if follow_report_choice == '01':
            result_normal_num = get_num_of_SEQUENCE(data[offset:], '对象属性及其数据')
            offset += 1
            config.line_level += 1
            for result_normal_count in range(result_normal_num):
                end_flag = 1 if result_normal_count == result_normal_num - 1 else 0
                offset += take_A_ResultNormal(data[offset:], end_flag=end_flag)
            config.line_level -= 1
        elif follow_report_choice == '02':
            result_record_num = get_num_of_SEQUENCE(data[offset:], '记录型对象属性及其数据')
            offset += 1
            config.line_level += 1
            for result_record_count in range(result_record_num):
                end_flag = 1 if result_record_count == result_record_num - 1 else 0
                offset += take_A_ResultRecord(data[offset:], end_flag=end_flag)
            config.line_level -= 1
    return offset


def take_TimeTag(data, add_text='', end_flag=0):
    offset = 0
    timetag_option = data[offset]
    offset += take_OPTIONAL(data[offset:], '时间标签')
    if timetag_option == '01':
        offset += take_date_time_s(data[offset:], '发送时标')
        offset += take_TI(data[offset:], '允许传输延时时间')
    return offset


def take_PIID(data, add_text='', end_flag=0):
    offset = 0
    piid = int(data[offset], 16)
    service_priority = '一般的, ' if piid >> 7 == 0 else '高级的, '
    invoke_id = piid & 0x3f
    show_data_source(data[offset:], 1)
    output(' —— PIID(服务优先级:' + service_priority + '服务序号:' + str(invoke_id) + ')')
    offset += 1
    return offset


def take_PIID_ACD(data, add_text='', end_flag=0):
    offset = 0
    piid_acd = int(data[offset], 16)
    service_priority = '一般的, ' if piid_acd >> 7 == 0 else '高级的, '
    ACD = '不请求访问, ' if (piid_acd >> 6) & 0x01 == 0 else '请求访问, '
    invoke_id = piid_acd & 0x3f
    show_data_source(data[offset:], 1)
    output(' —— PIID-ACD(服务优先级:' + service_priority + ACD + '服务序号:' + str(invoke_id) + ')')
    offset += 1
    return offset


def take_OPTIONAL(data, add_text='', end_flag=0):
    offset = 0
    optional = '有(OPTIONAL)' if data[offset] == '01' else '无(OPTIONAL)'
    show_data_source(data[offset:], 1, config.line_level)
    output(' —— ' + add_text + ':' + optional)
    offset += 1
    return offset


def take_CHOICE(data, add_text='', choice_dict=None, end_flag=0):
    offset = 0
    choice = data[offset]
    show_data_source(data[offset:], 1)
    if choice_dict is not None:
        choice_explain = choice_dict[choice]
        output(' —— ' + add_text + '(CHOICE ' + choice + ':' + choice_explain + ')')
    else:
        output(' —— ' + add_text + '(CHOICE)')
    offset += 1
    return offset


def get_num_of_SEQUENCE(data, SEQUENCE_text='', end_flag=0):
    num = int(data[0], 16)
    show_data_source(data, 1)
    output(' —— ' + SEQUENCE_text + '*' + str(num))
    return num


def get_len_of_octect_string(data, end_flag=0):
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


def take_DAR(data, add_text='', level=0, end_flag=0):
    offset = 0
    show_data_source(data[offset:], 1, level=level)
    try:
        explain = data_translate.dar_explain[int(data[0], 16)]
    except Exception:
        explain = '未知DAR'
    output(' —— ' + add_text + ':' + explain)
    offset += 1
    return offset


def take_A_ResultNormal(data, add_text='', end_flag=0):
    offset = 0
    offset += take_OAD(data[offset:])
    offset += take_Get_Result(data[offset:])
    return offset


def take_Get_Result(data, add_text='', end_flag=0):
    offset = 0
    result = data[offset]
    if result == '00':  # 错误信息
        show_data_source(data[offset:], 1, level=config.line_level)
        offset += 1
        offset += take_DAR(data[offset:], 'DAR')
    elif result == '01':  # 数据
        show_data_source(data[offset:], 1, level=config.line_level)
        output(' —— 数据')
        offset += 1
        offset += take_Data(data[offset:])
    return offset


def take_A_ResultRecord(data, add_text='', end_flag=0):
    offset = 0
    offset += take_OAD(data[offset:])
    csd_num = int(data[offset], 16)
    offset += take_RCSD(data[offset:])
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


def take_GetRecord(data, add_text='', end_flag=0):
    offset = 0
    offset += take_OAD(data[offset:])
    offset += take_RSD(data[offset:])  # RSD
    offset += take_RCSD(data[offset:], end_flag=end_flag)  # RCSD处理
    return offset


def take_ConnectMechanismInfo(data, add_text='', end_flag=0):
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
        pass
    elif connect_choice == '01':
        offset += take_visible_string(data[offset:], 'PasswordSecurity:')
    elif connect_choice == '02':
        offset += take_octect_string(data[offset:], '密文1')
        offset += take_octect_string(data[offset:], '客户机签名1')
    elif connect_choice == '03':
        offset += take_octect_string(data[offset:], '密文2')
        offset += take_octect_string(data[offset:], '客户机签名2')
    return offset


def take_ConnectResponseInfo(data, add_text='', end_flag=0):
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


def take_FactoryVersion(data, add_text='', end_flag=0):
    offset = 0
    offset += take_visible_string(data[offset:], '厂商代码:', 4)
    offset += take_visible_string(data[offset:], '软件版本号:', 4)
    offset += take_visible_string(data[offset:], '软件版本日期:', 6)
    offset += take_visible_string(data[offset:], '硬件版本号:', 4)
    offset += take_visible_string(data[offset:], '硬件版本日期:', 6)
    offset += take_visible_string(data[offset:], '厂家扩展信息:', 8)
    return offset


# ############################ 数据类型处理 #############################
def take_Data(data, add_text='', end_flag=0):
    offset = 0
    if data[offset] == '00':    # 对null类型特殊处理
        offset += take_NULL(data[offset:], level_flag=1, end_flag=end_flag)
        return offset
    # if level != 0:
    #     config.line_level += level
    show_data_source(data[offset:], 1, config.line_level, end_flag)
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
    }[data[offset - 1]](data[offset:], add_text=add_text, level=0)
    return offset


def take_NULL(data, add_text='', level_flag=-1, end_flag=0):
    offset = 0
    show_data_source(data, 1, 0 if level_flag == -1 else config.line_level, end_flag)
    offset += 1
    output(' —— ' + add_text + '(NULL)')
    return offset


def take_array(data, add_text='', level=-1):
    offset = 0
    member_num = int(data[offset], 16)
    show_data_source(data[offset:], 1)
    output(' —— ' + add_text + 'array, 成员个数:' + str(member_num))
    offset += 1
    config.line_level += 1
    for count in range(member_num):
        end_flag = 1 if count == member_num - 1 else 0
        offset += take_Data(data[offset:], end_flag=end_flag)
    config.line_level -= 1
    return offset


def take_structure(data, add_text='', level=-1):
    offset = 0
    member_num = int(data[offset], 16)
    show_data_source(data[offset:], 1)
    output(' —— ' + add_text + 'structure, 成员个数:' + str(member_num))
    offset += 1
    config.line_level += 1
    for count in range(member_num):
        end_flag = 1 if count == member_num - 1 else 0
        offset += take_Data(data[offset:], end_flag=end_flag)
    config.line_level -= 1
    return offset


def take_bool(data, add_text='', level=-1):
    offset = 0
    show_data_source(data, 1)
    bool_value = ':False' if data[offset] == '00' else ':True'
    output(' —— ' + add_text + bool_value + '(bool)')
    offset += 1
    return offset


def take_bit_string(data, add_text='', bit_len=None, level=-1):
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
    output(' —— ' + add_text + str(bin(int(bit_string_text, 16))).split('b')[1].rjust(bit_len, '0')
           + '(bit-string,长度' + str(bit_len) + ')')
    offset += byte_len
    return offset


def take_double_long(data, add_text='', level=-1):
    offset = 0
    show_data_source(data, 4)
    if int(data[offset], 16) >> 7 == 1:  # 负数
        value = -(0x100000000 - int(''.join(data[offset : offset + 4]), 16))
    else:
        value = int(''.join(data[offset: offset + 4]), 16)
    output(' —— ' + add_text + str(value) + '(double_long)')
    offset += 4
    return offset


def take_double_long_unsigned(data, add_text='', level=-1):
    offset = 0
    show_data_source(data, 4)
    output(' —— ' + add_text +
           str(int(data[offset] + data[offset + 1] + data[offset + 2] + data[offset + 3], 16))
           + '(double_long_unsigned)')
    offset += 4
    return offset


def take_octect_string(data, add_text='', string_len=None, level=-1):
    offset = 0
    if string_len is None:
        string_len, offset = get_len_of_octect_string(data[offset:])
        show_data_source(data[:offset], offset)
    show_data_source(data[offset:], string_len)
    output(' —— ' + add_text + '(octect_string,长度' + str(string_len) + ')')
    offset += string_len
    return offset


def take_visible_string(data, add_text='', string_len=None, level=-1):
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


def take_UTF8_string(data, add_text='', level=-1):
    offset = 0
    print('未定义\n')
    return offset


def take_integer(data, add_text='', level=-1):
    offset = 0
    show_data_source(data, 1)
    if int(data[offset], 16) >> 7 == 1:  # 负数
        value = -(0x100 - int(data[offset], 16))
    else:
        value = int(data[offset], 16)
    output(' —— ' + add_text + str(value) + '(integer)')
    offset += 1
    return offset


def take_long(data, add_text='', level=-1):
    offset = 0
    show_data_source(data, 2)
    if int(data[offset], 16) >> 7 == 1:  # 负数
        value = -(0x10000 - int(data[offset] + data[offset + 1], 16))
    else:
        value = int(data[offset] + data[offset + 1], 16)
    output(' —— ' + add_text + str(value) + '(long)')
    offset += 2
    return offset


def take_unsigned(data, add_text='', level=-1):
    offset = 0
    show_data_source(data, 1)
    output(' —— ' + add_text + str(int(data[offset], 16)) + '(unsigned)')
    offset += 1
    return offset


def take_long_unsigned(data, add_text='', level=-1):
    offset = 0
    show_data_source(data, 2)
    output(' —— ' + add_text + str(int(data[offset] + data[offset + 1], 16)) + '(long_unsigned)')
    offset += 2
    return offset


def take_long64(data, add_text='', level=-1):
    offset = 0
    show_data_source(data, 8)
    if int(data[offset], 16) >> 7 == 1:  # 负数
        value = -(0x10000000000000000 - int(''.join(data[offset : offset + 8]), 16))
    else:
        value = int(''.join(data[offset : offset + 8]), 16)
    output(' —— ' + add_text + str(value) + '(long64)')
    offset += 8
    return offset


def take_long64_unsigned(data, add_text='', level=-1):
    offset = 0
    show_data_source(data, 8)
    value = int(data[offset] + data[offset + 1] + data[offset + 2] + data[offset + 3] +
                data[offset + 4] + data[offset + 5] + data[offset + 6] + data[offset + 7], 16)
    output(' —— ' + add_text + str(value) + '(long64_unsigned)')
    offset += 8
    return offset


def take_enum(data, add_text='', level=-1, enum_dict=None):
    offset = 0
    enum_explain = ''
    if enum_dict is not None:
        try:
            enum_explain = enum_dict[data[offset]]
        except Exception:
            print(Exception)
    show_data_source(data, 1)
    output(' —— ' + add_text + enum_explain + '(enum)')
    offset += 1
    return offset


def take_float32(data, add_text='', level=-1):
    offset = 0
    show_data_source(data, 4)
    if int(data[offset], 16) >> 7 == 1:  # 负数
        value = -(0x100000000 - int(''.join(data[offset : offset + 4]), 16))
    else:
        value = int(''.join(data[offset : offset + 4]), 16)
    output(' —— ' + add_text + str(value) + '(float32)')
    offset += 4
    return offset


def take_float64(data, add_text='', level=-1):
    offset = 0
    show_data_source(data, 8)
    if int(data[offset], 16) >> 7 == 1:  # 负数
        value = -(0x10000000000000000 - int(''.join(data[offset : offset + 8]), 16))
    else:
        value = int(''.join(data[offset : offset + 8]), 16)
    output(' —— ' + add_text + str(value) + '(float64)')
    offset += 8
    return offset


def take_date_time(data, add_text='', level=-1):
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


def take_date(data, add_text='', level=-1):
    offset = 0
    year = int(data[0] + data[1], 16)
    month = int(data[2], 16)
    day = int(data[3], 16)
    # week = int(data[4], 16)
    show_data_source(data, 5)
    output(' —— ' + add_text + '{0:04d}-{1:02d}-{2:02d}'.format(year, month, day) + '(date)')
    offset += 5
    return offset


def take_time(data, add_text='', level=-1):
    offset = 0
    hour = int(data[0], 16)
    minute = int(data[1], 16)
    second = int(data[2], 16)
    show_data_source(data, 3)
    output(' —— ' + add_text + '{0:02d}:{1:02d}:{2:02d}'.format(hour, minute, second) + '(time)')
    offset += 3
    return offset


def take_date_time_s(data, add_text='', level=-1):
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


def take_OI(data, add_text='', level=-1):
    offset = 0
    OI_explain = data_translate.oad_explain[data[offset] + data[offset + 1] + '01'].split('，')[0]
    # print('OI_explain:', OI_explain, 'over')
    show_data_source(data, 2)
    output(' —— ' + add_text + OI_explain + '(OI)')
    offset += 2
    return offset


def take_OAD(data, add_text='', level=-1, end_flag=0):
    offset = 0
    attr = int(data[offset + 2], 16)
    try:
        explain = data_translate.oad_explain[data[offset] + data[offset + 1] + data[offset + 2]]
    except Exception:
        try:
            explain = data_translate.oad_explain[data[offset] + data[offset + 1] + '01'].split('，')[0]
            explain += '，属性' + str(attr)
        except Exception:
            explain = '未知OAD，属性' + str(attr)
    index = int(data[offset + 3], 16)
    if level == -1:
        show_data_source(data[offset:], 4, level=config.line_level, end_flag=end_flag)
    else:
        show_data_source(data[offset:], 4, level=level, end_flag=end_flag)
    offset += 4
    output(' —— ' + add_text + explain + '，索引' + str(index) + '(OAD)')
    return offset


def take_ROAD(data, add_text='', level=-1, end_flag=0):
    offset = 0
    config.line_level += 1
    offset += take_OAD(data[offset:], level=0)
    oad_num = int(data[offset], 16)
    show_data_source(data[offset:], 1, level=config.line_level, end_flag=end_flag)
    output(' —— 关联OAD*' + str(oad_num))
    offset += 1
    config.line_level += 1
    for oad_count in range(oad_num):
        end_flag = 1 if oad_count == oad_num - 1 else 0
        offset += take_OAD(data[offset:], end_flag=end_flag)
    config.line_level -= 1
    config.line_level -= 1
    return offset


def take_OMD(data, add_text='', level=-1, end_flag=0):
    offset = 0
    method = int(data[offset + 2], 16)
    try:
        explain = data_translate.omd_explain[data[offset] + data[offset + 1] + data[offset + 2]]
    except Exception:
        try:
            explain = data_translate.omd_explain[data[offset] + data[offset + 1] + '01'].split('，')[0]
            explain += '，方法' + str(method)
        except Exception:
            explain = '未知OMD，方法' + str(method)
    mode = int(data[offset + 3], 16)
    show_data_source(data[offset:], 4, level=config.line_level, end_flag=end_flag)
    offset += 4
    output(' —— ' + add_text + explain + '，操作模式' + str(mode) + '(OMD)')
    return offset


def take_TI(data, add_text='', level=-1):
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


def take_TSA(data, add_text='', level=-1):
    # print('Kay, take_TSA data:', data)
    offset = 0
    TSA_len = int(data[offset], 16)
    addr_text = ''
    if TSA_len != 0:
        addr_len = int(data[offset + 1], 16) + 1
        for tsa_count in range(addr_len):
            addr_text += data[offset + 2 + tsa_count]
    else:
        addr_len = 0
    show_data_source(data[offset:], 1 + TSA_len)
    output(' —— ' + add_text + addr_text + '(TSA,长度' + str(addr_len) + ')')
    offset += 1 + TSA_len
    return offset


def take_MAC(data, add_text='', level=-1):
    offset = 0
    offset += take_octect_string(data[offset:], 'MAC')
    return offset


def take_RN(data, add_text='', level=-1):
    offset = 0
    offset += take_octect_string(data[offset:], 'RN')
    return offset


def take_RN_MAC(data, add_text='', level=-1):
    offset = 0
    offset += take_octect_string(data[offset:], 'RN')
    offset += take_octect_string(data[offset:], 'MAC')
    return offset


def take_Region(data, add_text='', level=-1):
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


def take_Scaler_Unit(data, add_text='', level=-1):
    offset = 0
    offset += take_integer(data[offset:], '换算:')
    offset += take_enum(data[offset:], '单位:')
    return offset


def take_RSD(data, add_text='', level=-1):
    offset = 0
    # print(data[:])
    show_data_source(data[offset:], 1, level=config.line_level)
    selector = data[offset]
    if selector == '00':
        output(' —— Selector0, 不选择')
    else:
        output(' —— Selector' + selector)
    offset += 1
    if selector == '00':
        pass
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


def take_CSD(data, add_text='', level=-1, end_flag=0):
    offset = 0
    csd_choice = data[offset]
    show_data_source(data[offset:], 1, level=config.line_level, end_flag=end_flag)
    output(' —— OAD' if csd_choice == '00' else ' —— ROAD')
    offset += 1
    if csd_choice == '00':
        offset += take_OAD(data[offset:], end_flag=end_flag)
    elif csd_choice == '01':
        offset += take_ROAD(data[offset:], end_flag=end_flag)
    return offset


def take_MS(data, add_text='', level=-1):
    offset = 0
    MS_choice = data[0]
    if MS_choice == '00':  # 无电能表
        offset += take_NULL(data[offset:], 'MS:无电能表')
    elif MS_choice == '01':  # 全部用户地址
        offset += take_NULL(data[offset:], 'MS:全部用户地址')
    elif MS_choice == '02':  # 一组用户类型
        num = int(data[1], 16)
        show_data_source(data[offset:], 2)
        offset += 2
        output(' —— MS:用户类型*' + str(num))
        for count in range(num):
            offset += take_unsigned(data[offset:], '用户类型:')
    elif MS_choice == '03':  # 一组用户地址
        num = int(data[1], 16)
        show_data_source(data, 2)
        offset += 2
        output(' —— MS:用户地址*' + str(num))
        for count in range(num):
            offset += take_TSA(data[offset:])
    elif MS_choice == '04':  # 一组配置序号
        num = int(data[1], 16)
        show_data_source(data, 2)
        offset += 2
        output(' —— MS:配置序号*' + str(num))
        for count in range(num):
            offset += take_long_unsigned(data[offset:], '配置序号:')
    elif MS_choice == '05':  # 一组用户类型区间
        offset = 0
        num = int(data[1], 16)
        show_data_source(data, 2)
        offset += 2
        output(' —— MS:用户类型区间*' + str(num))
        for count in range(num):
            offset += take_Region(data[offset:], '用户类型区间:')
    elif MS_choice == '06':  # 一组用户地址区间
        offset = 0
        num = int(data[1], 16)
        show_data_source(data, 2)
        offset += 2
        output(' —— MS:用户地址区间*' + str(num))
        for count in range(num):
            offset += take_Region(data[offset:], '用户地址区间:')
    elif MS_choice == '07':  # 一组配置序号区间
        offset = 0
        num = int(data[1], 16)
        show_data_source(data, 2)
        offset += 2
        output(' —— MS:配置序号区间*' + str(num))
        for count in range(num):
            offset += take_Region(data[offset:], '配置序号区间:')
    return offset


def take_SID(data, add_text='', level=-1):
    offset = 0
    offset += take_double_long_unsigned(data[offset:], '标识:')
    print(data[offset:])
    offset += take_octect_string(data[offset:], '附加数据')
    return offset


def take_SID_MAC(data, add_text='', level=-1):
    offset = 0
    offset += take_SID(data[offset:])
    offset += take_MAC(data[offset:])
    return offset


def take_COMDCB(data, add_text='', level=-1):
    offset = 0
    rate_dict = {
        '00': '300bps',
        '01': '600bps',
        '02': '1200bps',
        '03': '2400bps',
        '04': '4800bps',
        '05': '7200bps',
        '06': '9600bps',
        '07': '19200bps',
        '08': '38400bps',
        '09': '57600bps',
        '0A': '15200bps',
        'FF': '自适应',
    }
    offset += take_enum(data[offset:], add_text='波特率：', enum_dict=rate_dict)
    offset += take_enum(data[offset:], add_text='校验位：', enum_dict={'00': '无校验', '01': '奇校验', '02': '偶校验'})
    offset += take_enum(data[offset:], add_text='数据位：', enum_dict={'05': '5', '06': '6', '07': '7', '08': '8'})
    offset += take_enum(data[offset:], add_text='停止位：', enum_dict={'01': '1', '02': '2'})
    offset += take_enum(data[offset:], add_text='流控：', enum_dict={'00': '无', '01': '硬件', '02': '软件'})
    return offset


def take_RCSD(data, add_text='', level=-1, end_flag=0):
    offset = 0
    csd_num = int(data[offset], 16)
    show_data_source(data[offset:], 1, level=config.line_level, end_flag=end_flag)
    output(' —— CSD*' + str(csd_num))
    offset += 1
    config.line_level += 1
    for csd_count in range(csd_num):
        end_flag = 1 if csd_count == csd_num - 1 else 0
        offset += take_CSD(data[offset:], end_flag=end_flag)
    config.line_level -= 1
    return offset
