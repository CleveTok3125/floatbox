# floatbox

A quick workaround to solve the compatibility problem
between applications and input methods on Linux.

## Why

- Some old/incompatible/non-integrated applications with Linux input methods
result in the inability to use system input methods such as iBus, Fcitx or Fcitx5.
- Digging into and fixing this problem can be time-consuming
and laborious without any significant results, and the workarounds may not be convenient.

## Idea

- Display a floating text filling dialog using a framework (e.g. Qt6)
that integrates system input methods.
- Based on passing composed characters directly into the application
using auto-type or clipboard paste instead of input methods. \
  Similar to copying typed text into a text editor and pasting it into the application.
- Use window focus mechanism to enter and pass text from floating dialog into application
without requiring much operation.

## Setup and Usage

### Setup

```fish
python -m venv venv
source venv/bin/activate.fish
pip install -r requirements.txt
```

Read the code and change the configuration accordingly

### Usage

Simply run `python floatbox.py`.
A dialog box will appear in the center of the screen to enter text.
Press ESC to exit or Enter to write the entered text. \
Assign a shortcut key to quickly trigger a command
and change the window behavior for the dialog if it is not focused.
