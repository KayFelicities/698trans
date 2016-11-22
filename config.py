import sys
import os

text_test = ''

pathname = ''
if getattr(sys, 'frozen', False):
    pathname = sys._MEIPASS
else:
    pathname = os.path.split(os.path.realpath(__file__))[0]
print("pathname: " + pathname)