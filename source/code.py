import board
import digitalio
import time
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from key_matrix import SenseMatrix, KeyMatrix
from key_mapping import KeyMap, ShiftMap

column_pins = (board.GP11, board.GP10, board.GP9)
row_pins = (board.GP14, board.GP12, board.GP13)
sense_matrix = SenseMatrix(row_pins, column_pins)

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

key_matrix = KeyMatrix("keys.csv", sense_matrix.row_num, sense_matrix.col_num)
press_num = [0] * 231


def press_routine(key_list):
    for key in key_list:
        if press_num[key] == 0:
            keyboard.press(key)

        press_num[key] += 1


def release_routine(key_list):
    for key in key_list:
        press_num[key] -= 1

        if press_num[key] == 0:
            keyboard.release(key)


while True:
    pressed, released = sense_matrix.scan()
    
    for p in pressed:
        i = p[0]
        j = p[1]

        this_mode = key_matrix.get_mode(i, j)
        if this_mode in ('1', '2', '4'):
            these_keys = key_matrix.get_macro(i, j)
            press_routine(these_keys)

            if this_mode == '1':
                release_routine(these_keys)

        if this_mode == '3':
            press_num = [0] * 231
            keyboard.release_all()

            these_keys = key_matrix.get_str(i, j)
            t = 0
            while t < len(these_keys):
                if these_keys[t] == KeyMap["Shift"]:
                    keyboard.press(KeyMap["Shift"])
                    t += 1

                keyboard.press(these_keys[t])
                keyboard.release_all()

                t += 1

            press_num = [0] * 231

    for r in released:
        i = r[0]
        j = r[1]

        this_mode = key_matrix.get_mode(i, j)
        if this_mode == '2':
            these_keys = key_matrix.get_macro(i, j)
            release_routine(these_keys)

        if this_mode in ('1', '3'):
            pass
