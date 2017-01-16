import config
import serial
import serial.tools.list_ports
import socket
import threading
import time
import traceback
import link_layer
import struct


def start_server(server_port):
    try:
        config.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        config.server.bind(('0.0.0.0', server_port))
        config.server.listen(1)
        config.server_check = True
        threading.Thread(target=server_accept).start()
        return 'ok'
    except Exception:
        traceback.print_exc()
        return 'err'


def is_link_request(re_text):
    if link_layer.get_service_type(re_text) == '01':
        return True
    else:
        return False


def reply_link_request(re_text):
    data = link_layer.data_format(re_text)
    SA_dict = link_layer.get_SA_CA(data)
    config.serial_window.SA_box.setText(SA_dict['SA'])
    config.serial_window.SA_len_box.setText(SA_dict['SA_len'])
    config.serial_window.read_SA_b.setText('已登录')
    config.serial_window.send_button.setEnabled(True)
    config.serial_window.read_SA_b.setEnabled(True)
    config.serial_window.calc_send_box_len()
    reply_text = link_layer.reply_link(data)
    return reply_text


def server_accept():
    while True:
        try:
            config.server_connection, addr = config.server.accept()
            print(addr, "connected")
            threading.Thread(target=server_run).start()
        except Exception:
            break
        if config.server_check is False:
            print('server_run quit')
            break


def server_run():
    while True:
        try:
            re_byte = config.server_connection.recv(4096)
            re_text = ''.join(['%02X ' % x for x in re_byte])
            print(re_text)
        except Exception:
            traceback.print_exc()
            break
        if re_text != '':
            if is_link_request(re_text) is False:
                config.serial_window._receive_signal.emit(re_text)
            else:
                reply_link_text = reply_link_request(re_text)
                data = link_layer.data_format(reply_link_text)
                send_d = b''
                for char in data:
                    send_d += struct.pack('B', int(char, 16))
                config.server_connection.sendall(send_d)
        if config.server_check is False:
            stop_thread(config.server_accept_thread)
            print('server_run quit')
            break


def close_server():
    config.server_check = False
    config.server.close()


def serial_com_scan():
    com_list = []
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        com_list.append(port[0])
    com_list.append('前置机')
    return com_list


def link_serial(serial_com):
    try:
        config.serial = serial.Serial(
            serial_com,
            config.serial_param['baudrate'],
            config.serial_param['bytesize'],
            config.serial_param['parity'],
            config.serial_param['stopbits'],
            timeout=config.serial_param['timeout'])
        config.serial.close()
        config.serial.open()
        config.serial_check = True
        threading.Thread(target=serial_run).start()
        return 'ok'
    except Exception:
        traceback.print_exc()
        return 'err'


def link_socket():
    try:
        config.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        config.socket.connect((config.socket_param['IP'], config.socket_param['port']))
        config.socket_check = True
        threading.Thread(target=socket_run).start()
        return 'ok'
    except Exception:
        traceback.print_exc()
        return 'err'


def close_serial():
    if config.serial_check is False:
        return 'ok'
    try:
        config.serial.close()
        config.serial_check = False
        return 'ok'
    except Exception:
        traceback.print_exc()
        return 'err'


def close_socket():
    if config.socket_check is False:
        return 'ok'
    try:
        config.socket.close()
        config.socket_check = False
    except Exception:
        traceback.print_exc()
        return 'err'


def send(send_text):
    data = link_layer.data_format(send_text)
    send_d = b''
    for char in data:
        send_d += struct.pack('B', int(char, 16))
    if config.serial_check is True:
        config.serial.write(send_d)
    if config.socket_check is True:
        config.socket.sendall(send_d)
    if config.server_check is True:
        config.server_connection.sendall(send_d)


def serial_run():
    while True:
        try:
            data_wait = config.serial.inWaiting()
        except Exception:
            traceback.print_exc()
            break
        re_text = ''
        while data_wait > 0:
            re_data = config.serial.readline()
            for re_char in re_data:
                re_text += '{0:02X} '.format(re_char)
            time.sleep(0.03)
            data_wait = config.serial.inWaiting()
        if re_text != '':
            config.serial_window._receive_signal.emit(re_text)
        if config.serial_check is False:
            print('serial_run quit')
            break


def socket_run():
    while True:
        try:
            re_byte = config.socket.recv(4096)
            re_text = ''.join(['%02X ' % x for x in re_byte])
            print(re_text)
        except Exception:
            traceback.print_exc()
            break
        if re_text != '':
            config.serial_window._receive_signal.emit(re_text)
        if config.socket_check is False:
            print('socket_run quit')
            break
