import os
import sys

output_text = ''
show_level = True
auto_trans = True
line_level = 0
serial = None
trans_child = None
serial_child = None
serial_check = False

pathname = ''
if getattr(sys, 'frozen', False):
    pathname = sys._MEIPASS
else:
    pathname = os.path.split(os.path.realpath(__file__))[0]
print("pathname: " + pathname)
