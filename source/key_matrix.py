import board
import circuitpython_csv as csv
import digitalio

from key_mapping import KeyMap, ShiftMap


class SenseMatrix:
    def __init__(self, row_pins: tuple, col_pins: tuple):

        # Check for nonzero pin lists.
        assert len(row_pins) > 0, f"The number of rows must be greater than 0."
        assert len(col_pins) > 0, f"The number of columns must be greater than 0."

        self._row_num = len(row_pins)
        self._col_num = len(col_pins)

        # Initialize key_states matrix, which is used for storing whether a key is pressed-down.
        self._key_states = []
        for i in range(self._row_num):
            self._key_states.append([False] * self._col_num)

        # Initialize pins. Column pins are set as input with pulldown, row pins are set as output.
        self._rows = []
        self._cols = []
        for i in range(self._row_num):
            self._rows.append(digitalio.DigitalInOut(row_pins[i]))
            self._rows[i].switch_to_output()

        for i in range(self._col_num):
            self._cols.append(digitalio.DigitalInOut(col_pins[i]))
            self._cols[i].switch_to_input(pull=digitalio.Pull.DOWN)

    def scan(self):
        pressed_keys = []
        released_keys = []

        for i in range(self._row_num):
            self._rows[i].value = True           # Switch a row to high to scan.

            for j in range(self._col_num):
                previous_key_state = self._key_states[i][j]          # Store the previous key state to compare later.
                this_key_state = self._cols[j].value                 # Read the current key state.

                if this_key_state and (not previous_key_state):     # Just pressed.
                    pressed_keys.append([i, j])

                elif (not this_key_state) and previous_key_state:   # Just released.
                    released_keys.append([i, j])

                self._key_states[i][j] = this_key_state              # Store the current key state for comparison in the next scan.

            self._rows[i].value = False          # Switch the row to low.

        return pressed_keys, released_keys


    @property
    def row_num(self):
        return self._row_num


    @property
    def col_num(self):
        return self._col_num


class KeyMatrix:
    def __init__(self, filename: str, row_num: int, col_num: int):

        # Check for greater than 0 number of rows and columns.
        assert row_num > 0, f"The number of rows must be greater than 0."
        assert col_num > 0, f"The number of rows must be greater than 0."

        # Assign attributes.
        self._row_num = row_num
        self._col_num = col_num
        self._modes = []

        self._macro_map = []
        for i in range(self._row_num):
            self._macro_map.append([])
            for j in range(self._col_num):
                self._macro_map[i].append([])

        self._str_map = []
        for i in range(self._row_num):
            self._str_map.append([])
            for j in range(self._col_num):
                self.str_map[i].append([])

        # Load the mode and decription from file.
        descriptions = []
        txtfile = open(filename, 'r')
        for i in range(2 * row_num):
            line = txtfile.readline()
            print(line)

            if i % 2 == 0:
                self._modes.append(line.split(','))
                self._modes[i // 2][-1] = self._modes[i // 2][-1][:-1] 
            else:
                if line.count(',') == 2:
                    descriptions.append(line.split(','))
                    descriptions[i // 2][-1] = descriptions[i // 2][-1][:-1]
                else :
                    pass

        # Decode the key descriptions.
        for i in range(row_num):
            for j in range(col_num):
                # Break out the macro keys to press.
                if self._modes[i][j] in ('1', '2', '4'):
                    keys = descriptions[i][j].split('-+-')
                    for key in keys:
                        self._macro_map[i][j].append(KeyMap[key])

                # Write the strings into str_map.
                if self._modes[i][j] == '3':
                    for char in descriptions[i][j]:
                        try:
                            self._str_map[i][j].append(KeyMap[char])
                        except KeyError:
                            self._str_map[i][j].append(KeyMap["SHIFT"])
                            self._str_map[i][j].append(ShiftMap[char])


    def get_mode(self, i: int, j: int):
        return self._modes[i][j]


    def get_macro(self, i: int, j: int):
        return self._macro_map[i][j]


    def get_str(self, i: int, j: int):
        return self._str_map[i][j]


    @property
    def modes(self):
        return self._modes


    @property
    def macro_map(self):
        return self._macro_map


    @property
    def str_map(self):
        return self._str_map
        
