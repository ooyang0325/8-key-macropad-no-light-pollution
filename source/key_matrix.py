import board
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

        # Initialise map of macros as an empty 2D list.
        self._macro_map = []
        for i in range(self._row_num):
            self._macro_map.append([])
            for j in range(self._col_num):
                self._macro_map[i].append([])

        # Initialise map of strings as an empty 2D list.
        self._str_map = []
        for i in range(self._row_num):
            self._str_map.append([])
            for j in range(self._col_num):
                self.str_map[i].append([])

        # Load the mode and decription from file.
        txtfile = open(filename, 'r')
        # Temporary list to store the description and process later.
        descriptions = []
        for i in range(2 * row_num):
            line = txtfile.readline()
            r = i // 2          # Convert line number into row number.
            line = line[:-1]            # Remove the \n at the end of the line.

            # If the current line is a mode line, add it into the mode list.
            if i % 2 == 0:
                self._modes.append(line.split(','))
            # If the current line is a description line, add it into the description temporary list.
            else:
                # Add the description line to the discription list.
                splits = []
                start_pos = 0

                # Find the commas used for separation.
                for j, char in enumerate(line):
                    if char == ',':
                        end_pos = j
                        # There will be an even number of double quotes between two commas used for separation.
                        if line.count('"', start_pos, end_pos) % 2 == 0:
                            splits.append(end_pos)              # Store the position of the comma.
                            start_pos = end_pos
                    else:
                        pass

                # Add a new row of descriptions.
                descriptions.append([])
                # Add the first cell from the begin of the line to the first separation comma.
                descriptions[r].append(line[:splits[0]])
                # Add the other cells.
                for j in range(col_num - 2):
                    # The content of the cells start after the comma and before the next comma(for separation).
                    descriptions[r].append(line[splits[j] + 1 : splits[j + 1]])
                # Add the last cell from the last separation comma to the end of the line.
                descriptions[r].append(line[splits[-1] + 1:])
                
                # Process the raw description data so that the decode part of the code can understand.
                for j in range(col_num):
                    description = descriptions[r][j]
                    # Remove the first and last double quote if they exist.
                    if description[0] == '"' and description[-1] == '"':
                        description = description[1:-1]

                    k = 0
                    while k < len(description):
                        # Remove of the the double double quotes when encountered.
                        if description[k:k+2] == '""':
                            description = description[:k] + description[k+1:]
                            k += 1
                        else:
                            k += 1
                    descriptions[r][j] = description

        # Decode the key descriptions.
        for i in range(row_num):
            for j in range(col_num):
                # Break out the macro keys to press.
                if self._modes[i][j] in ('1', '2', '4'):
                    keys = descriptions[i][j].split('++')
                    for key in keys:
                        self._macro_map[i][j].append(KeyMap[key])

                # Write the strings into str_map.
                if self._modes[i][j] == '3':
                    for char in descriptions[i][j]:
                        try:
                            self._str_map[i][j].append(KeyMap[char])
                        except KeyError:
                            self._str_map[i][j].append(KeyMap["Shift"])
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
