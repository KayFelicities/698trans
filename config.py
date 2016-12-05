import os
import sys

output_text = ''
show_level = False
line_level = 0
serial = None

pathname = ''
if getattr(sys, 'frozen', False):
    pathname = sys._MEIPASS
else:
    pathname = os.path.split(os.path.realpath(__file__))[0]
print("pathname: " + pathname)
