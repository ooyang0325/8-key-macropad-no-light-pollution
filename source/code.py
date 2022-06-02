import board
import circuitpython_csv as csv
import digitalio
import time
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from key_matrix import SenseMatrix, NumMatrix
from key_mapping import KeyMap

column_pins = (board.GP11, board.GP10, board.GP9)
row_pins = (board.GP14, board.GP12, board.GP13)
sense_matrix = SenseMatrix(row_pins, column_pins)

print('Done pin initialization')

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

while True:
    pressed, released = sense_matrix.scan()
    
    print(f"pressed: {pressed}")
    print(f"released: {released}")

    time.sleep(1)
#    new_pressed, new_shift = num.new_press(pressed)
#    print(new_pressed)
