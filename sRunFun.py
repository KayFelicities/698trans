from sFindIDFun import sFindAPDU
from shared_functions import *


def Verify(*data_in):  # True合法
    if data_in[0] != '68' or data_in[len(data_in) - 1] != '16' or int(data_in[2] + data_in[1], 16) != len(data_in) - 2:
        output('报文非法')
        return False
    else:
        output('68 —— 帧起始符')
        return True


def ShowLen(*data_in):
    output(data_in[1] + ' ' + data_in[2] + ' —— 长度域L=' +
           str(int(data_in[2] + data_in[1], 16)) + '字节')
    return 0


def ShowCtrl(*data_in):
    dir_prm_flag = int(data_in[3], 16) >> 6
    frame_separation_flag = (int(data_in[3], 16) >> 5) & 0x01
    function_flag = int(data_in[3], 16) & 0x03
    # print(dir_prm_flag, frame_separation_flag, function_flag)

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
    output(data_in[3] + ' —— 控制域C: ' + frame_type + ' ' + function_type)
    return


# 地址  输出地址所有字节数
def lShowAddr(*data_in):
    # 服务器地址
    server_addr_type = {
        0: ' 单地址',
        1: ' 通配地址',
        2: ' 组地址',
        3: ' 广播地址'
    }[int(data_in[4], 16) >> 6]
    # print('server_addr_type', server_addr_type)
    server_logic_addr = (int(data_in[4], 16) >> 4) & 0x03
    server_addr_len = (int(data_in[4], 16) & 0x0f) + 1
    # print('server_addr_len', server_addr_len)
    server_addr_list = data_in[4: server_addr_len + 6]
    server_addr_list_reverse = data_in[4 + server_addr_len: 4: -1]
    server_addr_data = ''
    server_addr = ''
    for k in range(0, server_addr_len + 1):
        server_addr_data += server_addr_list[k] + ' '
    for k in range(0, server_addr_len):
        server_addr += server_addr_list_reverse[k]
    output(server_addr_data + ' —— 服务器地址: 逻辑地址' + str(server_logic_addr)
           + server_addr_type + server_addr)
    output(data_in[5 + server_addr_len] + ' —— 客户机地址: ' + data_in[5 + server_addr_len])
    return server_addr_len + 2


# 帧头校验HCS
def lShowHCS(offset, *data_in):
    output(data_in[offset] + ' ' + data_in[offset + 1] + ' —— 帧头校验')
    return 2


# 链路层分帧
def lShowFenZen(offset, *data_in):
    frame_separation_flag = (int(data_in[3], 16) >> 5) & 0x01
    if frame_separation_flag == 1:
        frame_separation = int(data_in[4] + data_in[3], 16)
        print('frame_separation', frame_separation)
        frame_separation_seq = frame_separation & 0x3f
        try:
            frame_separation_type = {
                0: '中间帧',
                1: '最后帧',
                2: '确认帧'
            }[frame_separation >> 12]
        except:
            frame_separation_type = '错误'

        output(data_in[offset] + ' ' + data_in[offset + 1] + ' —— 分帧序号:' +
               str(frame_separation_seq) + frame_separation_type)
        return 2
    else:
        return 0


def show_service_type(offset, *data_in):
    server_type_line = sFindAPDU(data_in[offset])
    # print('server_type_line', server_type_line.decode('utf-8'))
    if server_type_line != '':
        output(data_in[offset] + ' —— ' +
               server_type_line.decode('utf-8').split('=')[1].split('\n')[0])
        try:
            server_type2 = int(data_in[offset + 1], 16)
            output(data_in[offset + 1] + ' —— ' +
                   server_type_line.decode('utf-8').split('=')[server_type2 + 2].split('\n')[0])
        except:
            pass
            # output(data_in[offset + 1] + ' —— 错误')
    else:
        output('APDU解析出错')
    return


def ShowOther(offset, *data_in):
    OtherCommand = ''
    for k in range(offset, len(data_in) - 3):
        OtherCommand = OtherCommand + data_in[k] + ' '
    if OtherCommand != '':
        output(OtherCommand + '—— 信息域及时间标签')
    return 0


def ShowFCS16(*data_in):
    output(data_in[len(data_in) - 3] + ' ' + data_in[len(data_in) - 2] + ' —— 帧校验')
    output(data_in[len(data_in) - 1] + ' —— 结束符')
    return 0
