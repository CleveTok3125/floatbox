#!/bin/python

import sys
import pyautogui
import pyperclip
from PyQt6.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QKeyEvent
from typing import Optional


class Hotkey:
    CHANGE_INPUT_METHOD: tuple | None = ("alt", "z")
    PASTE: tuple | None = ("ctrl", "v")


class Config:
    TIMEOUT: int = 360000  # ms
    WIDTH: int = 3  # inch
    CHANGE_INPUT_METHOD_DELAY: int = 50  # ms
    ESCAPE_SEQ = {
        r"\n": "\n",
        r"\t": "\t",
    }


class BorderlessInput(QWidget):
    def __init__(self, timeout=Config.TIMEOUT):
        super().__init__()

        dpi = self.logicalDpiX()
        width_px = int(Config.WIDTH * dpi)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setWindowTitle("floatbox")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout()
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("ENTER to submit, ESC to exit")
        self.line_edit.setFixedWidth(width_px)
        layout.addWidget(self.line_edit)
        self.setLayout(layout)

        QTimer.singleShot(Config.CHANGE_INPUT_METHOD_DELAY, self.send_change_hotkey)

        self.timeout_timer = QTimer()
        self.timeout_timer.setSingleShot(True)
        self.timeout_timer.timeout.connect(self.close)
        self.timeout_timer.start(timeout)

        self.text = None

    def send_change_hotkey(self):
        if Hotkey.CHANGE_INPUT_METHOD:
            pyautogui.hotkey(*Hotkey.CHANGE_INPUT_METHOD)

    def submit(self):
        self.text = self.line_edit.text()
        self.close()

    def keyPressEvent(self, a0: Optional[QKeyEvent]) -> None:
        if a0 is None:
            return

        if a0.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.submit()
        elif a0.key() == Qt.Key.Key_Escape:
            self.text = None
            self.close()
        else:
            super().keyPressEvent(a0)


def ask_text(timeout=Config.TIMEOUT) -> str | None:
    app = QApplication(sys.argv)
    window = BorderlessInput(timeout=timeout)
    window.show()
    app.exec()

    return window.text


def escape_seq(text: str) -> str:
    for key, value in Config.ESCAPE_SEQ.items():
        text = text.replace(key, value)
    return text


def main():
    text = ask_text(timeout=Config.TIMEOUT)
    if not text:
        sys.exit(0)

    text = escape_seq(text=text)

    old_clipboard = pyperclip.paste()
    pyperclip.copy(text)

    if Hotkey.PASTE:
        pyautogui.hotkey(*Hotkey.PASTE)
        pyperclip.copy(old_clipboard)


if __name__ == "__main__":
    main()
