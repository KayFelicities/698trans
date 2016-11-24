from shared_functions import *  # NOQA


def data_format(input_text):
    input_text = input_text.replace(' ', '').replace('\n', '').upper()  # 处理空格和换行
    data_len = int(len(input_text) / 2)
    output('报文总长：' + str(data_len) + '字节(' + str(hex(data_len)) + ')\n')
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
        output('报文格式错误')
        return False
    elif int(data_in[2] + data_in[1], 16) != len(data_in) - 2:
        output('报文长度(0x' + data_in[2] + data_in[1] + ')错误！正确值0x{0:04X}'.format(len(data_in) - 2))
        return False
    else:
        return True


def take_link_layer_1(data):
    offset = 0
    # 起始符
    output('68 —— 帧起始符')
    offset += 1
    # 长度
    show_data_source(data[offset:], 2)
    output(' —— 长度L=' + str(int(data[offset + 1] + data[offset], 16)) + '字节')
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
    show_data_source(data[offset:], 2)
    output(' —— 帧头校验')
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


def take_link_layer_2(data):
    offset = 0
    show_data_source(data[offset:], len(data) - 3)
    output(' —— 信息域及时间标签')
    offset += len(data) - 3
    show_data_source(data[offset:], 2)
    output(' —— 帧校验')
    offset += 2
    show_data_source(data[offset:], 1)
    output(' —— 结束符')
    offset += 1
    return offset
