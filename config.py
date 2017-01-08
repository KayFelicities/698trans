import os
import sys

output_text = ''
show_level = True
auto_trans = True
auto_fix = False

line_level = 0
trans_window = None
serial_window = None
about_window = None
config_window = None
param_window = None
task_window = None

CA_addr = '10'

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
    'IP': '121.40.80.159',
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
