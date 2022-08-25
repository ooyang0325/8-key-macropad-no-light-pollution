import time
import rp2pio
import board
import microcontroller
import adafruit_pioasm
import array


program1 = """
.side_set 1

.wrap_target
pull                    side 0
set y 23                side 0
bit_start:
    out x, 1            side 1  [2]
    jmp !x zero         side 1
one:
    nop                 side 1  [4]
    jmp y-- bit_start   side 0  [6]
    jmp end             side 0
zero:
;    nop                 side 0  [7]
;    jmp y-- bit_start   side 0  [3]
    jmp y-- bit_start   side 0  [11]
end:
    mov isr y           side 0
    push                side 0
.wrap
"""

program2 = """
.program myWS2812
.side_set 1

pull
out isr 2
push
"""

assembled = adafruit_pioasm.assemble(program1)
rgbPin = board.GP16

sm = rp2pio.StateMachine(
    assembled,
    frequency=12800000,
    first_sideset_pin=rgbPin,
    out_shift_right=False,
    initial_sideset_pin_state=0,
)

R = 255
G = 255
B = 255

value = array.array('L', [(G << 24) + (R << 16) + (B << 8)])
print(value)
sm.clear_rxfifo()
sm.write(value)
print('Wrote some data.')
time.sleep(0.1)
sm.readinto(value)
print(value)
