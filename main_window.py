from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        # Central Widget

        self.central_widget = QWidget()

        # Layout

        self.v_layout = QVBoxLayout()

        # Setando o Layout dentro do Central Widget

        self.central_widget.setLayout(self.v_layout)

        # Setando o Central Widget

        self.setCentralWidget(self.central_widget)

        # Adicionando título à janela

        self.setWindowTitle("Calculadora")

    def adjust_fixed_size(self) -> None:
        # Tenta ajustar o tamanho da janela ao conteúdo

        self.adjustSize()

        # Tirando o redimensionamento da janela

        self.setFixedSize(self.width(), self.height())

    def addwidget_to_vlayout(self, widget: QWidget) -> None:
        self.v_layout.addWidget(widget)
        
    def make_msg_box(self):
        return QMessageBox(self)
