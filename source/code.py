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

keys = []
with open('keys.csv') as csvfile:
    csvreader = csv.reader(csvfile)

    for row in csvreader:
        keys.append(row)

column_pins = (board.GP6, board.GP7, board.GP8, board.GP9)
row_pins = (board.GP5, board.GP4, board.GP3, board.GP2, board.GP1)
sense_matrix = SenseMatrix(row_pins, column_pins)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

print('Done pin initialization')

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)
num = NumMatrix('num.csv', 5, 4)

while True:
    pressed, released = sense_matrix.scan()
    
    new_pressed, new_shift = num.new_press(pressed)
    print(new_pressed)
