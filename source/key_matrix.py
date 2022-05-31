import board
import circuitpython_csv as csv
import digitalio

from key_mapping import KeyMap, ShiftMap


class SenseMatrix:
    def __init__(self, row_pins: tuple, col_pins: tuple):
        assert len(row_pins) > 0, f"The number of rows must be greater than 0."
        assert len(col_pins) > 0, f"The number of columns must be greater than 0."

        self.row_num = len(row_pins)
        self.col_num = len(col_pins)
        self.key_states = []
        for i in range(self.row_num):
            self.key_states.append([False] * self.col_num)

        self.rows = []
        self.cols = []
        for i in range(self.row_num):
            self.rows.append(digitalio.DigitalInOut(row_pins[i]))
            self.rows[i].switch_to_output()

        for i in range(self.col_num):
            self.cols.append(digitalio.DigitalInOut(col_pins[i]))
            self.cols[i].switch_to_input(pull=digitalio.Pull.DOWN)

    def scan(self):
        pressed_keys = []
        released_keys = []
        for i in range(self.row_num):
            self.rows[i].value = True

            for j in range(self.col_num):
                previous_key_state = self.key_states[i][j]
                this_key_state = self.cols[j].value

                if this_key_state and (not previous_key_state):
                    pressed_keys.append([i, j])

                elif (not this_key_state) and previous_key_state:
                    released_keys.append([i, j])

                self.key_states[i][j] = this_key_state

            self.rows[i].value = False

        return pressed_keys, released_keys


class NumMatrix:
    def __init__(self, filename: str, row_num: int, col_num: int):
        assert row_num > 0, f"The number of rows must be greater than 0."
        assert col_num > 0, f"The number of rows must be greater than 0."

        self.row_num = row_num
        self.col_num = col_num
        self.codes = [[0] * col_num for i in range(row_num)]
        self.shifts = [[False] * col_num for i in range(row_num)]
        self.shifted = 0
        self.pressed_codes = [[], []]

        with open(filename) as csvfile:
            lines = list(csv.reader(csvfile))

            for i, line in enumerate(lines):
                for j, key in enumerate(line):
                    try:
                        self.codes[i][j] = KeyMap[key]
                    except KeyError:
                        self.codes[i][j] = ShiftMap[key]
                        self.shifts[i][j] = True
        
    def new_press(self, pressed_keys: list):
        new_pressed = []
        new_shift = False
        if len(pressed_keys):
            for p in pressed_keys:
                i = p[0]
                j = p[1]
                this_code = self.codes[i][j]
                this_shift = self.shifts[i][j]

                if not(this_code in self.pressed_codes[0]):
                    new_pressed.append(this_code)

                if this_shift and not self.shifted:
                    new_shift = True

                self.pressed_codes[0].append(self.codes[i][j])
                self.pressed_codes[1].append(self.shifts[i][j])

        return new_pressed, new_shift
"""            
        def update(self, pressed_keys: list, released_keys: list):
            if len(pressed_keys):
                for p in pressed_keys:
                    i = p[0]
                    j = p[1]

                    self.pressed_codes[0].append(self.codes[i][j])
                    self.pressed_codes[1].append(self.shifts[i][j])

            if len(released_keys):
                for r in released_keys:
                    i = r[0]
                    j = r[1]

                    for k, code in enumerate(self.pressed_codes[0]):
                        if code == self.codes[i][j]:
                            if self.pressed_codes[1][k] == self.shifts[i][j]:
                                del self.pressed_codes[0][k]
                                del self.pressed_codes[1][k]
                                break

                            else:
                                pass

                        else:
                            pass

"""
