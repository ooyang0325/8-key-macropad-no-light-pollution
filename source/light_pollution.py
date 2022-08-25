import adafruit_pioasm
import board
import rp2pio

from array import array


class PIO_RGB:
    program = """
    .program ws2812
    .side_set 1
    .wrap_target
    bitloop:
        out x 1         side 0  [6]
        jmp !x do_zero  side 1  [3]
    do_one:
        jmp bitloop     side 1  [4]
    do_zero:
        nop             side 0  [4]
    .wrap
    """

    def __init__(self, pin):
        self._RGB_pin = pin
        self._assembled = adafruit_pioasm.assemble(PIO_RGB.program)
        self._sm = rp2pio.StateMachine(
            self._assembled,
            frequency=12800000,
            first_sideset_pin=self._RGB_pin,
            auto_pull=True,
            out_shift_right=False,
            pull_threshold=24,
        )
        self._sm.stop()


    def connect(self):
        self._sm.restart()


    def disconnect(self):
        self._sm.stop()


    def set_colour(self, R: int, G: int, B: int):
        value = array('L', [(G << 24) + (R << 16) + (B << 8)])
        self._sm.write(value)
