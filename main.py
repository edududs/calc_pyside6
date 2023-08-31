import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from views import ButtonGrid, Display, Info, _setup_theme
from main_window import MainWindow
from variables_ import WINDOW_ICON_PATH_STR

if __name__ == "__main__":
    # Cria a aplicação

    app = QApplication(sys.argv)
    _setup_theme()

    window = MainWindow()

    # Define o ícone

    icon = QIcon(WINDOW_ICON_PATH_STR)

    window.setWindowIcon(icon)

    # Info

    info = Info("Sua conta")

    window.addwidget_to_vlayout(info)

    # Display

    display = Display()
    window.addwidget_to_vlayout(display)

    # Button Grid
    buttons_grid = ButtonGrid(display, info, window)
    window.v_layout.addLayout(buttons_grid)

    # Executando tudo

    window.adjust_fixed_size()

    window.show()

    app.exec()
 