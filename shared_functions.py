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
        len_of_len = len_flag | 0x7f
        string_len = ''
        for count in range(len_of_len):
            string_len += data[offset + count]
        offset += len_of_len
        return int(string_len, 16), offset


def get_DAR(DAR):
    file_path = os.path.join(pathname, '698ErrIDConfig.ini')
    file_handle = open(file_path, 'rb')
    file_lines = file_handle.readlines()
    file_handle.close()
    dar_explain = ''
    for dar_line in file_lines:
        if dar_line.decode('utf-8')[0:2] == DAR:
            dar_explain = dar_line.decode('utf-8')[3:].split('\n')[0]
            break
    return dar_explain


def take_A_ResultNormal(data, add_text=''):
    offset = 0
    offset += take_OAD(data[offset:])
    offset += take_Get_Result(data[offset:])
    return offset


def take_Get_Result(data, add_text=''):
    offset = 0
    result = data[offset]
    if result == '00':  # 错误信息
        show_data_source(data[offset:], 2)
        dar = get_DAR(data[offset + 1])
        output(' —— 错误信息:' + dar)
        offset += 2
    if result == '01':  # 数据
        show_data_source(data[offset:], 1)
        output(' —— 数据')
        offset += 1
        offset += take_Data(data[offset:])
    return offset


# ############################ 数据类型处理 #############################
def take_Data(data, add_text=''):
    offset = 0
    show_data_source(data[offset:], 1)
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
    output(' —— NULL' + add_text)
    return offset


def take_array(data, add_text=''):
    offset = 0
    return offset


def take_structure(data, add_text=''):
    offset = 0
    return offset


def take_bool(data, add_text=''):
    offset = 0
    return offset


def take_bit_string(data, add_text=''):
    offset = 0
    return offset


def take_double_long(data, add_text=''):
    offset = 0
    return offset


def take_double_long_unsigned(data, add_text=''):
    offset = 0
    return offset


def take_octect_string(data, add_text=''):
    offset = 0
    string_len = 0
    string_len, offset = get_len_of_octect_string(data[offset:])
    show_data_source(data[:offset], offset)
    output(' —— octect_string,长度:' + str(string_len))
    show_data_source(data[offset:], string_len)
    output(' —— octect_string' + add_text)
    offset += string_len
    return offset


def take_visible_string(data, add_text=''):
    offset = 0
    return offset


def take_UTF8_string(data, add_text=''):
    offset = 0
    return offset


def take_integer(data, add_text=''):
    offset = 0
    return offset


def take_long(data, add_text=''):
    offset = 0
    return offset


def take_unsigned(data, add_text=''):
    offset = 0
    show_data_source(data, 1)
    output(' —— unsigned:' + str(int(data[offset], 16)) + add_text)
    offset += 1
    return offset


def take_long_unsigned(data, add_text=''):
    offset = 0
    show_data_source(data, 2)
    output(' —— long_unsigned:' + str(int(data[offset] + data[offset + 1], 16)) + add_text)
    offset += 2
    return offset


def take_long64(data, add_text=''):
    offset = 0
    show_data_source(data, 4)
    if int(data[offset], 16) >> 7 == 1:  # 负数
        value = int(str(int(data[offset]) & 0x7f) + data[offset + 1] +
                    data[offset + 2] + data[offset + 3], 16) * (-1)
    else:
        value = int(data[offset] + data[offset + 1] + data[offset + 2] + data[offset + 3], 16)
    output(' —— long64:' + str(value) + add_text)
    offset += 4
    return offset


def take_long64_unsigned(data, add_text=''):
    offset = 0
    show_data_source(data, 4)
    value = int(data[offset] + data[offset + 1] + data[offset + 2] + data[offset + 3], 16)
    output(' —— long64:' + str(value) + add_text)
    offset += 4
    return offset


def take_enum(data, add_text=''):
    offset = 0
    show_data_source(data, 1)
    output(' —— enum:' + str(int(data[offset], 16)) + add_text)
    offset += 1
    return offset


def take_float32(data, add_text=''):
    offset = 0
    return offset


def take_float64(data, add_text=''):
    offset = 0
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
    output(' —— data_time:{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}:{6:03d}'
           .format(year, month, day, hour, minute, second, milliseconds) + add_text)
    offset += 10
    return offset


def take_date(data, add_text=''):
    offset = 0
    return offset


def take_time(data, add_text=''):
    offset = 0
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
    output(' —— data_time:{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'
           .format(year, month, day, hour, minute, second) + add_text)
    offset += 7
    return offset


def take_OI(data, add_text=''):
    offset = 0
    return offset


def take_OAD(data, add_text=''):
    offset = 0
    file_path = os.path.join(pathname, '698DataIDConfig.ini')
    file_handle = open(file_path, 'rb')
    file_lines = file_handle.readlines()
    file_handle.close()

    OI = data[offset] + data[offset + 1]
    oad_explain = ''
    for OI_line in file_lines:
        if OI_line.decode('utf-8')[0:4] == OI:
            oad_explain = OI_line.decode('utf-8')[8:].split('=')[0].split('\n')[0]
            break
    show_data_source(data, 4)
    output(' —— OAD:' + oad_explain)
    offset += 4
    return offset


def take_ROAD(data, add_text=''):
    offset = 0
    offset += take_OAD(data[offset:], '对象属性描述符')
    oad_num = int(data[offset], 16)
    show_data_source(data[offset:], 1)
    output(' —— 关联OAD*' + str(oad_num))
    offset += 1
    for oad_count in range(oad_num):
        offset += take_OAD(data[offset:], '(关联OAD)')
    return offset


def take_OMD(data, add_text=''):
    offset = 0
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
    output(' —— 间隔时间:' + str(TI_value) + TI_uint)
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
    output(' —— TSA' + ':' + addr_text)
    offset += 1 + TSA_len
    return offset


def take_MAC(data, add_text=''):
    offset = 0
    return offset


def take_RN(data, add_text=''):
    offset = 0
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
    offset += take_Data(data, add_text='(起始值)')
    offset += take_Data(data, add_text='(结束值)')
    return offset


def take_Scaler_Unit(data, add_text=''):
    offset = 0
    return offset


def take_RSD(data, add_text=''):
    offset = 0
    show_data_source(data[offset:], 1)
    selector = data[offset]
    output(' —— Selector' + selector)
    offset += 1
    if selector == '00':
        offset += take_NULL(data[offset:], '(不选择)')
    elif selector == '01':
        offset += take_OAD(data[offset:])
        offset += take_Data(data[offset:], '(数值)')
    elif selector == '02':
        offset += take_OAD(data[offset:])
        offset += take_Data(data[offset:], '(起始值)')
        offset += take_Data(data[offset:], '(结束值)')
        offset += take_Data(data[offset:], '(数据间隔)')
    elif selector == '03':
        selector2_count = int(data[offset], 16)
        offset += 1
        for count in range(selector2_count):
            offset += take_OAD(data[offset:])
            offset += take_Data(data[offset:], '(起始值)')
            offset += take_Data(data[offset:], '(结束值)')
            offset += take_Data(data[offset:], '(数据间隔)')
    elif selector in ['04', '05']:
        offset += take_date_time_s(data[offset:], '(采集启动时间)' if selector == '04' else '(采集存储时间)')
        offset += take_MS(data[offset:], '(数值)')
    elif selector in ['06', '07', '08']:
        type_text = {
            '06': '(采集启动时间',
            '07': '(采集存储时间',
            '08': '(采集成功时间',
        }[selector]
        offset += take_date_time_s(data[offset:], type_text + '起始值)')
        offset += take_date_time_s(data[offset:], type_text + '结束值)')
        offset += take_TI(data[offset:])
        offset += take_MS(data[offset:])
    elif selector == '09':
        offset += take_unsigned(data[offset:], '(上第n次记录)')
    elif selector == '0A':
        offset += take_unsigned(data[offset:], '(上n条记录)')
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
        offset += take_NULL(data[offset:], '(无电能表)')
    elif MS_choice == '01':  # 全部用户地址
        offset += take_NULL(data[offset:], '(全部用户地址)')
    elif MS_choice == '02':  # 一组用户类型
        num = int(data[1], 16)
        show_data_source(data[offset:], 2)
        offset += 2
        output(' —— 用户类型*' + str(num))
        for count in range(num):
            offset += take_unsigned(data[offset:], '(用户类型)')
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
            offset += take_long_unsigned(data[offset:], '(配置序号)')
    elif MS_choice == '05':  # 一组用户类型区间
        offset = 0
        num = int(data[1], 16)
        show_data_source(data, 2)
        offset += 2
        output(' —— 用户类型区间*' + str(num))
        for count in range(num):
            offset += take_Region(data[offset:], '(用户类型区间)')
    elif MS_choice == '06':  # 一组用户地址区间
        offset = 0
        num = int(data[1], 16)
        show_data_source(data, 2)
        offset += 2
        output(' —— 用户地址区间*' + str(num))
        for count in range(num):
            offset += take_Region(data[offset:], '(用户地址区间)')
    elif MS_choice == '07':  # 一组配置序号区间
        offset = 0
        num = int(data[1], 16)
        show_data_source(data, 2)
        offset += 2
        output(' —— 配置序号区间*' + str(num))
        for count in range(num):
            offset += take_Region(data[offset:], '(配置序号区间)')
    return offset


def take_SID(data, add_text=''):
    offset = 0
    return offset


def take_SID_MAC(data, add_text=''):
    offset = 0
    return offset


def take_COMDCB(data, add_text=''):
    offset = 0
    return offset


def take_RCSD(data, add_text=''):
    offset = 0
    csd_num = int(data[offset], 16)
    show_data_source(data[offset:], 1)
    output(' —— CSD*' + str(csd_num))
    offset += 1
    for csd_count in range(csd_num):
        offset += take_CSD(data[offset:])
    return offset
