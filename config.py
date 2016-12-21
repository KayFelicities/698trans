import os
import sys

output_text = ''
show_level = True
auto_trans = True
auto_linklayer = False

line_level = 0
trans_child = None
serial_child = None

serial = None
serial_check = False
serial_param = {
    'baudrate': 9600,
    'bytesize': 8,
    'parity': 'E',
    'stopbits': 1,
    'timeout': 0.05,
}

socket_param = {
    'ip': '121.40.80.159',
    # 'ip': '127.0.0.1',
    'port': 20084,
}
socket = None
socket_check = False

good_L = None
good_HCS = None
good_FCS = None

pathname = ''
if getattr(sys, 'frozen', False):
    pathname = sys._MEIPASS
else:
    pathname = os.path.split(os.path.realpath(__file__))[0]
print("pathname: " + pathname)
