import math
from typing import TYPE_CHECKING

import qdarktheme
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton

from utils import convert_to_number, is_empty, is_num_or_dot, is_valid_number
from variables_ import BIG_FONT_SIZE  # QSS - Estilos do QT for Python
from variables_ import (
    MEDIUM_FONT_SIZE,
    MINIMUM_WIDTH,
    PRIMARY_COLOR,
    QSS,
    SMALL_FONT_SIZE,
    TEXT_MARGIN,
)

if TYPE_CHECKING:
    from main_window import MainWindow

# https://doc.qt.io/qtforpython/tutorials/basictutorial/widgetstyling.html


# Dark Theme


# https://pyqtdarktheme.readthedocs.io/en/latest/how_to_use.html


def _setup_theme():
    qdarktheme.setup_theme(
        theme="dark",
        corner_shape="rounded",
        custom_colors={
            "[dark]": {
                "primary": f"{PRIMARY_COLOR}",
            },
            "[light]": {
                "primary": f"{PRIMARY_COLOR}",
            },
        },
        additional_qss=QSS,
    )


class Display(QLineEdit):
    eq_pressed = Signal()
    del_pressed = Signal()
    clear_pressed = Signal()
    input_pressed = Signal(str)
    operator_pressed = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config_style()
        self.setReadOnly(True)

    def config_style(self):
        margins = [TEXT_MARGIN for _ in range(4)]

        self.setStyleSheet(f"font-size: {BIG_FONT_SIZE}px;")

        self.setMinimumHeight(BIG_FONT_SIZE * 2)

        self.setMinimumWidth(MINIMUM_WIDTH)

        self.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.setTextMargins(*margins)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key

        is_enter = key in [KEYS.Key_Enter, KEYS.Key_Return]
        is_delete = key in [KEYS.Key_Backspace, KEYS.Key_Delete]
        is_esc = key in [KEYS.Key_Escape]
        is_operator = key in [
            KEYS.Key_Plus,
            KEYS.Key_Minus,
            KEYS.Key_Slash,
            KEYS.Key_Asterisk,
            KEYS.Key_P,
            KEYS.Key_AsciiCircum,
        ]

        if is_enter or text == "=":
            self.eq_pressed.emit()
            return event.ignore()

        if is_delete:
            self.del_pressed.emit()
            return event.ignore()

        if is_esc:
            self.clear_pressed.emit()
            return event.ignore()

        if is_operator:
            if text.lower() == "p":
                text = "^"
            self.operator_pressed.emit(text)
            return event.ignore()

        if is_empty(text):
            return event.ignore()

        if is_num_or_dot(text):
            self.input_pressed.emit(text)
            return event.ignore()


class Info(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config_style()

    def config_style(self):
        self.setStyleSheet(f"font-size: {SMALL_FONT_SIZE}px;")

        self.setAlignment(Qt.AlignmentFlag.AlignRight)


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config_style()

    def config_style(self):
        font = self.font()

        font.setPixelSize(MEDIUM_FONT_SIZE)

        self.setFont(font)

        self.setMinimumSize(75, 75)


class ButtonGrid(QGridLayout):
    def __init__(self, display: Display, info, window: "MainWindow", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._grid_mask = [
            ["C", "◀", "^", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["", "0", ".", "="],
        ]

        self.display = display
        self.info = info
        self.window = window
        self._equation = ""
        self._equation_initial_value = "Sua conta"
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equation_initial_value

        self._make_grid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value

        self.info.setText(value)

    def _make_grid(self):
        self.display.del_pressed.connect(self._backspace)
        self.display.eq_pressed.connect(self._eq)
        self.display.clear_pressed.connect(self._clear)
        self.display.input_pressed.connect(self._insert_to_display)
        self.display.operator_pressed.connect(self._config_left_op)

        for i, row_data in enumerate(self._grid_mask):
            for j, button_text in enumerate(row_data):
                button = Button(button_text)

                slot = self._make_slot(self._insert_to_display, button_text)

                if button_text == "":
                    continue

                if button_text != "0":
                    if not is_num_or_dot(button_text) and not is_empty(button_text):
                        button.setProperty("cssClass", "specialButton")

                        self._config_special_button(button)

                    self.addWidget(button, i, j)

                else:
                    button0 = Button(button_text)

                    self.addWidget(button0, i, j - 1, 1, 2)

                    self._connect_button_clicked(button0, slot)

                self._connect_button_clicked(button, slot)

    def _connect_button_clicked(self, button: Button, slot):
        button.clicked.connect(slot)

    def _config_special_button(self, button: Button):
        text = button.text()

        if text == "C":
            self._connect_button_clicked(button, self._clear)

        if text in "+-/*^":
            self._connect_button_clicked(
                button, self._make_slot(self._config_left_op, text)
            )

        if text == "=":
            self._connect_button_clicked(button, self._eq)

        if text == "◀":
            self._connect_button_clicked(button, self.display.backspace)

    @Slot()
    def _make_slot(self, func, *args, **kwargs):
        @Slot(bool)
        def real_slot(_):
            func(*args, **kwargs)

        return real_slot

    @Slot()
    def _insert_to_display(self, text) -> None:
        new_display_value = self.display.text() + text

        if not is_valid_number(new_display_value):
            return

        self.display.insert(text)
        self.display.setFocus()

    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equation_initial_value
        self.display.clear()
        self.display.setFocus()

    @Slot()
    def _config_left_op(self, text):
        display_text = self.display.text()  # Deverá ser meu número _left

        self.display.clear()
        self.display.setFocus()

        # Se a pessoa clicou no operador sem
        # configurar um número
        if not is_valid_number(display_text) and self._left is None and text != "-":
            self._show_error("Você não digitou nada")
            return

        if text == "-" and self._left is None and not display_text:
            self._left = 0

        # Se houver algo no número da esquerda,
        # não fazemos nada. Aguardaremos o número da direito.
        if self._left is None:
            self._left = convert_to_number(display_text)

        if self._left is not None and self._op and is_valid_number(display_text):
            self._right = convert_to_number(display_text)
            result = self._calc_result(self._left, self._op, self._right)
            self.info.setText(f"{self.equation} = {result}")

        self._op = text

        self.equation = f"{self._left} {self._op}"

    def _calc_result(self, left, op, right):
        self.equation = f"{left} {op} {right}"
        result = "error"
        try:
            if "^" in self.equation and isinstance(left, float | int):
                result = math.pow(left, right)
                self._left = result
                self._right = None
                result = convert_to_number(str(result))
                return result
            else:
                result = eval(self.equation)
                self._left = result
                self._right = None
                result = convert_to_number(str(result))
                return result

        except ZeroDivisionError:
            self._show_error("Divisão por zero")
        except OverflowError:
            self._show_error("Esta conta não pode ser realizada")

        if result == "error":
            self._left = None
        return result

    @Slot()
    def _eq(self):
        text_display = self.display.text()

        if not is_valid_number(text_display) or self._left is None or self._op is None:
            self._show_error("Conta incompleta")
            return

        self._right = convert_to_number(text_display)
        result = self._calc_result(self._left, self._op, self._right)
        self.info.setText(f"{self.equation} = {result}")

        self.display.clear()
        self.display.setFocus()

    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

    def _make_dialog(self, text):
        msg_box = self.window.make_msg_box()
        msg_box.setText(text)
        return msg_box

    def _show_error(self, text):
        msg_box = self._make_dialog(text)
        msg_box.setIcon(msg_box.Icon.Critical)
        msg_box.exec()
        self.display.setFocus()

    def _show_info(self, text):
        msg_box = self.window.make_msg_box(text)
        msg_box.setIcon(msg_box.Icon.Information)
        msg_box.exec()
        self.display.setFocus()


if __name__ == "__main__":
    pass
