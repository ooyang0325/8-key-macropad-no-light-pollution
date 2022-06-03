# 8-key-macropad-no-light-pollution
## Code Structure
The files to put in the CitcuitPython directory is located inside the **source** folder. There are a few files:
- **code.py**: CircuitPython looks for this file and runs it as the main script after booting up the RP2040-zero. We (are going to) put the functions related to sending key strokes in this file.
- **key_matrix.py**: We implement the two matrices in this file. First, the **senseMatrix** is responsible for scanning the matrix on the PCB for key strokes. Second, the **keyMatrix** (not yet implemented) is going to read the CSV file and return the corresponding key for the functions in **code.py** to send.
- **key_mapping.py**: There are two python dictionaries in this file. First, the **keyMap** contains the HID codes for different keys that don't require pressing shift. Second, the **shiftMap** contains the HID codes for different keys that require pressing shift.

## Limitations
1. Due to the USB-HID protocol, at most **6 keys** can be pressed at once. Modifier keys(CTRL, SHIFT, ALT, GUI) are not counted in the 6 keys as they use the Modifier byte in the input report.
2. The effect of pressing shift will affect every key pressed at that moment. For example, if we press "g" first, then press "!" will result in "G" and "!" in the output. Because "!" is actually "SHIFT" + "1", the "g" will become "G" due to pressing shift by another key.
