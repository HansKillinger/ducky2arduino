# !/usr/bin/python3
# -*- coding: utf-8 -*-

# Ducky2Arduino - Converts USB-Rubber-Ducky payloads (Ducky script) to Arduino code.
# Author:
# Hans Killinger <hanskillinger@protonmail.com> 
# https://github.com/HansKillinger
# 
# NOTICE:
# Usage of this program is only allowed within boundaries of law.
# Developer assumes no liability and is not responsible for any misuse or damage caused by this program.


from __future__ import print_function
import sys

out = sys.__stdout__

VERSION = '1.0.0'

# order is important
SPECIAL_BUTTONS = {'CONTROL_RIGHT': 'KEY_RIGHT_CONTROL',
                   'CONTROL_LEFT':  'KEY_LEFT_CONTROL',
                   'CONTROL':       'KEY_LEFT_CONTROL',

                   'CTRL_RIGHT':    'KEY_RIGHT_CONTROL',
                   'CTRL_LEFT':     'KEY_LEFT_CONTROL',
                   'CTRL':          'KEY_LEFT_CONTROL',

                   'SHIFT_RIGHT':   'KEY_RIGHT_SHIFT',
                   'SHIFT_LEFT':    'KEY_LEFT_SHIFT',
                   'SHIFT':         'KEY_LEFT_SHIFT',

                   'ALT_RIGHT':     'KEY_RIGHT_ALT',
                   'ALT_LEFT':      'KEY_LEFT_ALT',
                   'ALT':           'KEY_LEFT_ALT',

                   'GUI_RIGHT':     'KEY_RIGHT_GUI',
                   'GUI_LEFT':      'KEY_LEFT_GUI',
                   'GUI':           'KEY_LEFT_GUI',
                   'WINDOWS':       'KEY_LEFT_GUI',
                   'F1':            'KEY_F1',
                   'F2':            'KEY_F2',
                   'F3':            'KEY_F3',
                   'F4':            'KEY_F4',
                   'F5':            'KEY_F5',
                   'F6':            'KEY_F6',
                   'F7':            'KEY_F7',
                   'F8':            'KEY_F8',
                   'F9':            'KEY_F9',
                   'F10':           'KEY_F10',
                   'F11':           'KEY_F11',
                   'F12':           'KEY_F12',

                   'LEFTARROW':     'KEY_LEFT_ARROW',
                   'RIGHTARROW':    'KEYRIGHT_ARROW',
                   'UPARROW':       'KEY_UP_ARROW',
                   'DOWNARROW':     'KEY_DOWN_ARROW',
                   'LEFT':          'KEY_LEFT_ARROW',
                   'RIGHT':         'KEY_RIGHT_ARROW',
                   'UP':            'KEY_UP_ARROW',
                   'DOWN':          'KEY_DOWN_ARROW',

                   'DELETE':        'KEY_DELETE',
                   'DEL':           'KEY_DELETE',
                   'PRINTSCREEN':   'KEY_PRT_SCR',
                   'TAB':           'KEY_TAB',
                   'ESCAPE':        'KEY_ESC',
                   'SPACE':         'KEY_SPACE',
                   'ENTER':         'KEY_RETURN'}


# arguments


HELP = '''
========== Ducky2Arduino v.''' + VERSION + ''' ==============================
https://github.com/HansKillinger/ducky2arduino/
Convert USB-Rubber-Ducky payloads (Ducky script) to Arduino code.
=============================================================
Author:
Hans Killinger <hanskillinger@protonmail.com>
https://github.com/HansKillinger

Options:
  -h, --help            Show basic help message and exit

Usage:

    python3 ducky2arduino.py [payload.txt] [output_file] - 
     specify payload file and output file

    python ducky2arduino.py [payload.txt]  - 
     converted payload will be saved in "payload.ino"

---------------------------------------------------------------
Ducky payload samples can be found here:
https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Payloads

Or, you can simply write your own payloads using Ducky script:
https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Duckyscript
----------------------------------------------------------------
'''

SUCCESS = 'Success!'
ERROR = 'ERROR! -h or --help for help\n'





payload_input = ''
payload_len = 0

if '-h' in sys.argv or '--help' in sys.argv:
    print(HELP)
    exit()
elif '-v' in sys.argv or '--version' in sys.argv:
    print ('''
========== ducky2arduino v.''' + VERSION + ''' ==============================
https://github.com/HansKillinger/ducky2arduino/
Convert USB-Rubber-Ducky payloads (Ducky script) to Arduino code.
=============================================================''')
    exit()
elif len(sys.argv) == 2:
    try:
        payload_input = open(sys.argv[1], "r")
        sys.stdout = open("payload.ino", "w")
        payload_len = len(open(sys.argv[1], "r").readlines())
    except IOError:
        error_reason = ('File "' + sys.argv[1] + '" does not exist!\n')
        print(ERROR + error_reason)
        exit()
elif len(sys.argv) == 3:
    try:
        payload_input = open(sys.argv[1], "r")
        sys.stdout = open(sys.argv[2] + '.ino', 'w')
        payload_len = len(open(sys.argv[1], "r").readlines())
    except IOError:
        error_reason = ('File "' + sys.argv[1] + '" does not exist!\n')
        print(ERROR + error_reason)
        exit()
elif len(sys.argv) > 3:
    error_reason = 'Too many Arguments'
    print(ERROR + error_reason)
    exit()
else:
    try:
        payload_input = open('payload.txt', "r")
        sys.stdout = open("payload.ino", "w")
        payload_len = len(open('payload.txt', "r").readlines())
    except FileNotFoundError:
        print('\nERROR: Payload file "payload.txt" was not found')
        print(HELP)
        exit()

print ('''// Generated by ducky2arduino https://github.com/HansKillinger/ducky2arduino

#include "Keyboard.h"

void setup() {

''')

for i in range(payload_len):
    line = payload_input.readline().replace('\n', '')

    if len(line) < 1:
        print('', end='')

    else:

        if 'REM' in line:
            print('//', line.replace('REM ', ''))

        else:
            if 'DELAY' in line:
                print(line.replace('DELAY', 'delay(').replace(' ', ''), end='')
                print(');')

            elif 'STRING' in line:
                print('Keyboard.', end='')
                print(line.replace('"', '")); Keyboard.print(char(34)); Keyboard.print("')
                      .replace('\\', '")); Keyboard.print(char(92)); Keyboard.print("')
                      .replace('STRING ', 'print("', end='')
                print('")', end='')
                print(');')

            elif 'MENU' in line:
                line = 'KEY_F10'
                mod = 'MOD_SHIFT_LEFT'
                print('Keyboard.press(', end='')
                print(str(mod), end='')
                print(');')
                print("Keyboard.press('", end='')
                print(str(line), end='')
                print("');")
                print('Keyboard.releaseAll();')

            else:
                for key in SPECIAL_BUTTONS.keys():
                    if key in line:  # order in keys is important
                        line = line.replace(key, '')
                        mod = SPECIAL_BUTTONS.get(key)
                        print('Keyboard.press(', end='')
                        print(str(mod), end='')
                        print(');')

                line = line.replace(' ', '')
                if len(line) > 0:
                        print("Keyboard.press('", end='')
                        print(str(line), end='')
                        print("');")
                print('Keyboard.releaseAll();')

        if len(line) < 1:
            print('', end='')


print('''
}

void loop() {

}''')

payload_input.close()
sys.stdout = out
print(SUCCESS)
