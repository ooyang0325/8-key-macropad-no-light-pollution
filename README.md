# 8-key-macropad-no-light-pollution

![1654238728052](https://user-images.githubusercontent.com/52309935/171801701-f0228002-cdf0-44e8-84c7-5621b14ae018.png)

## Code Structure
The files to put in the CitcuitPython directory is located inside the **source** folder. There are a few files:
- **code.py**: CircuitPython looks for this file and runs it as the main script after booting up the RP2040-zero. We put the functions related to sending key strokes in this file.
- **key_matrix.py**: We implement the two matrices in this file. First, the **SenseMatrix** is responsible for scanning the matrix on the PCB for key strokes. Second, the **KeyMatrix** is going to read the CSV file(**keys.csv**) and return the corresponding key for the functions in **code.py** to send.
- **key_mapping.py**: There are two python dictionaries in this file. First, the **KeyMap** contains the HID codes for different keys that don't require pressing shift. Second, the **ShiftMap** contains the HID codes for different keys that require pressing shift.

## Code details
1. The reason we use a CSV file to store the key information is just for easy editing, since it can done with spreadsheet software. The __init__() code in KeyMatrix will read this file as a simple text file.
2. To use multiple key strokes in one macro key, put **++** between the two keys a cell in **keys.csv**.

## How to program macros
1. Open **keys.csv** with your preferred spreadsheet software. Remember to turn smart quote off if you are using Libreoffice Calc.
2. Every switch on the PCB is related to two cells in the spreadsheet. The upper cell sets the mode of the switch, while the lower one will set the macro or string to output. Note that there is no switch in the middle of the top row; thus, the corresponding cells should be left as 0 and 0 in the example.
3. When programming *macro*, only use keys that *don't require Shift*. Please use the same name for the keys as shown in [this website](https://zhouer.org/KeyboardTest/). The keys in **key_mapping.py** follow its naming scheme with spaces removed.

## Limitations
1. Due to the USB-HID protocol, at most **6 keys** can be pressed at once. Modifier keys(Ctrl, Shift, Alt, Win) are not counted in the 6 keys as they use the Modifier byte in the input report.
2. The effect of pressing shift will affect every key pressed at that moment. For example, if we press "g" first, then press "!" will result in "G" and "!" in the output. Because "!" is actually "Shift" + "1", the "g" will become "G" due to pressing shift by another key.

## Modes
0. **Switch disabled**: As the name implies, mode 0 will disable the switch and there will be no output when the switch is pressed.
1. **Press once**: When a switch is pressed, the corresponding macro keys will be pressed down in order and then released at once after the last key is pressed.
2. **Press and hold**: When a switch is pressed, the corresponding macro keys will be pressed down in order and held down until the switch is released or another switch is pressed.
3. **Send string**: As the name implies, mode 3 will send a corresponding string once when the switch is pressed.
4. **Rapid press**: When a switch is pressed down the corresponding macro keys will fire at a given rate.

## Project status
1. Only modes 0~3 are implemented.
