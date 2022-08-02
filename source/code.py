import board
import circuitpython_csv as csv
import digitalio
import time
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from key_matrix import SenseMatrix, KeyMatrix
from key_mapping import KeyMap

column_pins = (board.GP11, board.GP10, board.GP9)
row_pins = (board.GP14, board.GP12, board.GP13)
sense_matrix = SenseMatrix(row_pins, column_pins)

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

key_matrix = KeyMatrix("test.csv", sense_matrix.row_num, sense_matrix.col_num)
"""
for i in range(sense_matrix.row_num):
    for j in range(sense_matrix.col_num):
        print(i, j)
        print(key_matrix.get_mode(i, j))
"""

while True:
    pressed, released = sense_matrix.scan()
    
    for p in pressed:
        i = p[0]
        j = p[1]

        this_mode = key_matrix.get_mode(i, j)
        if this_mode in ('1', '2', '4'):
            keyboard.release_all()

            these_keys = key_matrix.get_macro(i, j)
            keyboard.press(*these_keys)

            if this_mode == '1':
                keyboard.release_all()

        if this_mode == '3':
            keyboard.release_all()

            these_keys = key_matrix.get_str(i, j)
            t = 0
            while t < len(these_keys):
                if these_keys[t] == KeyMap["SHIFT"]:
                    keyboard.press(KeyMap["SHIFT"])
                    t += 1

                keyboard.press(these_keys[t])
                keyboard.release_all()

                t += 1

    for r in released:
        keyboard.release_all()
