import os
import sys

output_text = ''
show_level = 0
line_level = 0

pathname = ''
if getattr(sys, 'frozen', False):
    pathname = sys._MEIPASS
else:
    pathname = os.path.split(os.path.realpath(__file__))[0]
print("pathname: " + pathname)
