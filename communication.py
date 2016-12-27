import config
import serial
import serial.tools.list_ports
import socket
import threading
import time
import traceback
import link_layer
import struct


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
