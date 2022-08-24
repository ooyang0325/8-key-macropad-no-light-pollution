import time
import rp2pio
import board
import microcontroller
import adafruit_pioasm


program1 = """
.program myWS2812
.side_set 1

.wrap_target
pull
set y 24
bit_start:
    out x 1             side 1  [2]
    jmp !x zero
one:
    nop                         [4]
    jmp y-- bit_start   side 0  [6]
zero:
    jmp y-- bit_start   side 0  [11]
end:
    in null 32
    push
.wrap
"""

program2 = """
.program myWS2812
.side_set 1

.wrap_target
pull
set y 24
mov isr osr
push
.wrap
"""

assembled = adafruit_pioasm.assemble(program2)
rgbPin = microcontroller.pin.GPIO2

sm = rp2pio.StateMachine(
    assembled, 
    frequency=12800000,
    first_sideset_pin=rgbPin,
    out_shift_right=False,
)

R = 0
G = 0
B = 0

value = bytearray(b"\x00\x00\x00\x00")
value[0] = G
value[1] = R
value[2] = B
# print(value)
sm.clear_rxfifo()
sm.write(value)
print('Wrote some data.')
# print(sm.frequency)
sm.readinto(value)
print(value)
