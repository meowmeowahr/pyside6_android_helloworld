import platform
import sys
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QApplication,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.count = 0

        # simple QSS to test styling on Android
        self.setStyleSheet(
            """
            QMainWindow {
                background: #040610;
            }
            QPushButton {
                border: none;
                border-radius: 8px;
                background: #efeffa;
                color: #040610;
            }
            QPushButton:pressed {
                background: #ffffff;
            }
            QLabel {
                color: #efeffa;
            }
            QTextEdit {
                background: #141620;
                color: #efeffa;
                border-radius: 8px;
                border: 2px solid #dfdfea;
                padding: 8px;
            }
            """
        )

        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        self.root_layout = QVBoxLayout(self.widget)
        self.root_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.root_layout.addStretch()

        self.counter_label = QLabel(f"Times pressed: {self.count}")
        self.counter_label.setFont(QFont(self.font().family(), 22))
        self.root_layout.addWidget(
            self.counter_label, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.counter_button = QPushButton("+")
        self.counter_button.setFont(QFont(self.font().family(), 22))
        self.counter_button.setFixedHeight(56)
        self.counter_button.setFixedWidth(64)
        self.counter_button.clicked.connect(self.count_up)
        self.root_layout.addWidget(
            self.counter_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.root_layout.addStretch()

        self.platform_info = QTextEdit()
        self.platform_info.setReadOnly(True)
        self.platform_info.setText(
            f"sys.platform: {sys.platform}\n\nsys.executable: {sys.executable}\n\nsys.argv: {sys.argv}\n\nsys.version: {sys.version}\n\nplatform.architecture: {platform.architecture()}\n\nplatform.machine: {platform.machine()}\n\nplatform.release: {platform.release()}"
        )
        self.root_layout.addWidget(self.platform_info)

        # forced window refresh
        # this is needed due to some partial viewport update bugs
        self.repaint_timer = QTimer()
        self.repaint_timer.setInterval(1000 // 30)  # forced 30fps repaint
        self.repaint_timer.timeout.connect(self.repaint)
        if sys.argv == ["notaninterpreterreally"]:
            # argv will always be ['notaninterpreterreally'] with buildozer
            # there is no need for this on desktop
            self.repaint_timer.start()

        self.show()

    def count_up(self):
        self.count += 1
        self.counter_label.setText(f"Times pressed: {self.count}")


if __name__ == "__main__":
    app = QApplication([])
    win = MainWindow()
    app.exec()
