from shared_functions import *  # NOQA


def calc_len(input_text):
    input_text = input_text.replace(' ', '').replace('\n', '').upper()  # 处理空格和换行
    data_len = int(len(input_text) / 2)
    len_message = str(data_len) + '字节(' + str(hex(data_len)) + ')'
    # data = []
    # for k in range(0, data_len):
    #     data.append(input_text[k * 2:(k + 1) * 2])
    # fcs_calc = get_fcs(data[:], data_len)
    # fcs_calc = ((fcs_calc << 8) | (fcs_calc >> 8)) & 0xffff  # 低位在前
    return len_message


def data_format(input_text):
    input_text = input_text.replace(' ', '').replace('\n', '').upper()  # 处理空格和换行
    # 处理FE前缀
    k = 0
    while input_text[k * 2:(k + 1) * 2] == 'FE':
        k += 1
    input_text = input_text[k * 2:]
    print('原始报文： ' + input_text + '\n')
    # 写入list
    data = []
    for k in range(0, int(len(input_text) / 2)):
        data.append(input_text[k * 2:(k + 1) * 2])
    return data


def check_data(data_in):  # True合法
    if data_in[0] != '68' or data_in[len(data_in) - 1] != '16':
        # output('报文格式错误')
        return 'format_error'
    elif int(data_in[2] + data_in[1], 16) != len(data_in) - 2:
        output('报文长度(0x' + data_in[2] + data_in[1] + ')错误！正确值0x{0:04X}'.format(len(data_in) - 2))
        return 'len_error'
    else:
        return 'ok'


def take_link_layer_1(data):
    offset = 0
    # 起始符
    output('68 —— 帧起始符')
    offset += 1
    # 长度
    show_data_source(data[offset:], 2)
    output(' —— 长度L:' + str(int(data[offset + 1] + data[offset], 16)) + '字节')
    offset += 2
    # 控制域
    ctrol = int(data[offset], 16)
    dir_prm_flag = ctrol >> 6
    frame_separation_flag = (ctrol >> 5) & 0x01
    function_flag = ctrol & 0x03
    frame_type = {
        0: '完整报文',
        1: '分帧报文'
    }[frame_separation_flag]
    function_type = ''
    if function_flag == 1:
        try:
            function_type = {
                0: '主站确认登录心跳',
                2: '终端登录心跳'
            }[dir_prm_flag]
        except:
            function_type = '错误'
    elif function_flag == 3:
        function_type = {
            0: '主站确认主动上报',
            1: '主站向终端下发命令',
            2: '终端主动上报',
            3: '终端响应主站命令'
        }[dir_prm_flag]
    else:
        function_type = '错误'
    show_data_source(data[offset:], 1)
    output(' —— 控制域C: ' + frame_type + ' ' + function_type)
    offset += 1
    # 地址域
    server_addr_type = {
        0: ' 单地址',
        1: ' 通配地址',
        2: ' 组地址',
        3: ' 广播地址'
    }[int(data[offset], 16) >> 6]
    server_logic_addr = (int(data[offset], 16) >> 4) & 0x03
    server_addr_len = (int(data[offset], 16) & 0x0f) + 1
    server_addr_reverse = data[offset + server_addr_len: offset: -1]
    server_addr = ''
    for k in range(0, server_addr_len):
        server_addr += server_addr_reverse[k]
    show_data_source(data[offset:], server_addr_len + 1)
    output(' —— 服务器地址: 逻辑地址' + str(server_logic_addr) + server_addr_type + server_addr)
    offset += server_addr_len + 1
    show_data_source(data[offset:], 1)
    output(' —— 客户机地址: ' + data[offset])
    offset += 1
    # 帧头校验
    fcs_calc = get_fcs(data[1:offset], offset - 1)
    fcs_calc = ((fcs_calc << 8) | (fcs_calc >> 8)) & 0xffff  # 低位在前
    # print('fcs test:', data[1:offset], 'cs:', hex(fcs_calc))
    fcs_now = int(data[offset] + data[offset + 1], 16)
    hcs_check = '(正确)' if fcs_now == fcs_calc else '(错误，正确值{0:04X})'.format(fcs_calc)

    show_data_source(data[offset:], 2)
    output(' —— 帧头校验:{0:04X}'.format(fcs_now) + hcs_check)
    offset += 2
    # 分帧
    if frame_separation_flag == 1:
        frame_separation = int(data[offset] + data[offset + 1], 16)
        print('frame_separation', frame_separation)
        frame_separation_seq = frame_separation & 0x3f
        try:
            frame_separation_type = {
                0: '(起始帧)',
                1: '(最后帧)',
                2: '(确认帧)',
                3: '(中间帧)',
            }[frame_separation >> 14]
        except:
            frame_separation_type = '错误'
        show_data_source(data[offset:], 2)
        output(' —— 分帧序号:' + str(frame_separation_seq) + frame_separation_type)
        offset += 2
    return offset


def take_link_layer_2(data, offset):
    offset_temp = offset
    fcs_calc = get_fcs(data[1:offset], offset - 1)
    fcs_calc = ((fcs_calc << 8) | (fcs_calc >> 8)) & 0xffff  # 低位在前
    # print('fcs test:', data[1:offset], 'cs:', hex(fcs_calc))
    fcs_now = int(data[offset] + data[offset + 1], 16)
    hcs_check = '(正确)' if fcs_now == fcs_calc else '(错误，正确值{0:04X})'.format(fcs_calc)
    show_data_source(data[offset:], 2)
    output(' —— 帧校验:{0:04X}'.format(fcs_now) + hcs_check)
    offset += 2
    show_data_source(data[offset:], 1)
    output(' —— 结束符')
    offset += 1
    return offset - offset_temp


def get_fcs(cp, tlen):
    fcs = 0xffff
    for count in range(tlen):
        fcs = (fcs >> 8) ^ fcstab[(fcs ^ int(cp[count], 16)) & 0xff]
    fcs ^= 0xffff
    return fcs


fcstab = (0x0000, 0x1189, 0x2312, 0x329b, 0x4624, 0x57ad, 0x6536, 0x74bf,
          0x8c48, 0x9dc1, 0xaf5a, 0xbed3, 0xca6c, 0xdbe5, 0xe97e, 0xf8f7,
          0x1081, 0x0108, 0x3393, 0x221a, 0x56a5, 0x472c, 0x75b7, 0x643e,
          0x9cc9, 0x8d40, 0xbfdb, 0xae52, 0xdaed, 0xcb64, 0xf9ff, 0xe876,
          0x2102, 0x308b, 0x0210, 0x1399, 0x6726, 0x76af, 0x4434, 0x55bd,
          0xad4a, 0xbcc3, 0x8e58, 0x9fd1, 0xeb6e, 0xfae7, 0xc87c, 0xd9f5,
          0x3183, 0x200a, 0x1291, 0x0318, 0x77a7, 0x662e, 0x54b5, 0x453c,
          0xbdcb, 0xac42, 0x9ed9, 0x8f50, 0xfbef, 0xea66, 0xd8fd, 0xc974,
          0x4204, 0x538d, 0x6116, 0x709f, 0x0420, 0x15a9, 0x2732, 0x36bb,
          0xce4c, 0xdfc5, 0xed5e, 0xfcd7, 0x8868, 0x99e1, 0xab7a, 0xbaf3,
          0x5285, 0x430c, 0x7197, 0x601e, 0x14a1, 0x0528, 0x37b3, 0x263a,
          0xdecd, 0xcf44, 0xfddf, 0xec56, 0x98e9, 0x8960, 0xbbfb, 0xaa72,
          0x6306, 0x728f, 0x4014, 0x519d, 0x2522, 0x34ab, 0x0630, 0x17b9,
          0xef4e, 0xfec7, 0xcc5c, 0xddd5, 0xa96a, 0xb8e3, 0x8a78, 0x9bf1,
          0x7387, 0x620e, 0x5095, 0x411c, 0x35a3, 0x242a, 0x16b1, 0x0738,
          0xffcf, 0xee46, 0xdcdd, 0xcd54, 0xb9eb, 0xa862, 0x9af9, 0x8b70,
          0x8408, 0x9581, 0xa71a, 0xb693, 0xc22c, 0xd3a5, 0xe13e, 0xf0b7,
          0x0840, 0x19c9, 0x2b52, 0x3adb, 0x4e64, 0x5fed, 0x6d76, 0x7cff,
          0x9489, 0x8500, 0xb79b, 0xa612, 0xd2ad, 0xc324, 0xf1bf, 0xe036,
          0x18c1, 0x0948, 0x3bd3, 0x2a5a, 0x5ee5, 0x4f6c, 0x7df7, 0x6c7e,
          0xa50a, 0xb483, 0x8618, 0x9791, 0xe32e, 0xf2a7, 0xc03c, 0xd1b5,
          0x2942, 0x38cb, 0x0a50, 0x1bd9, 0x6f66, 0x7eef, 0x4c74, 0x5dfd,
          0xb58b, 0xa402, 0x9699, 0x8710, 0xf3af, 0xe226, 0xd0bd, 0xc134,
          0x39c3, 0x284a, 0x1ad1, 0x0b58, 0x7fe7, 0x6e6e, 0x5cf5, 0x4d7c,
          0xc60c, 0xd785, 0xe51e, 0xf497, 0x8028, 0x91a1, 0xa33a, 0xb2b3,
          0x4a44, 0x5bcd, 0x6956, 0x78df, 0x0c60, 0x1de9, 0x2f72, 0x3efb,
          0xd68d, 0xc704, 0xf59f, 0xe416, 0x90a9, 0x8120, 0xb3bb, 0xa232,
          0x5ac5, 0x4b4c, 0x79d7, 0x685e, 0x1ce1, 0x0d68, 0x3ff3, 0x2e7a,
          0xe70e, 0xf687, 0xc41c, 0xd595, 0xa12a, 0xb0a3, 0x8238, 0x93b1,
          0x6b46, 0x7acf, 0x4854, 0x59dd, 0x2d62, 0x3ceb, 0x0e70, 0x1ff9,
          0xf78f, 0xe606, 0xd49d, 0xc514, 0xb1ab, 0xa022, 0x92b9, 0x8330,
          0x7bc7, 0x6a4e, 0x58d5, 0x495c, 0x3de3, 0x2c6a, 0x1ef1, 0x0f78)
