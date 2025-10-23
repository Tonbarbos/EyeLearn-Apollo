from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import qtawesome as qta

from eye_tracker_wrapper import EyeTrackerWidget

class TelaEyeTrackerMaster(QWidget):
    back_to_configuracoes = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Cabeçalho --- #
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #4A7C8C; padding: 15px;")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)

        self.back_button = QPushButton()
        self.back_button.setIcon(qta.icon("fa5s.arrow-left", color="white"))
        self.back_button.setFixedSize(40, 40)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
            }
        """)
        header_layout.addWidget(self.back_button)

        title_label = QLabel("Rastreamento Ocular")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        main_layout.addWidget(header_frame)

        # Widget do Eye Tracker
        self.eye_tracker_widget = EyeTrackerWidget()
        main_layout.addWidget(self.eye_tracker_widget)

        main_layout.addStretch()

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #F5F5F5;")

        self.back_button.clicked.connect(self.back_to_configuracoes.emit)

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    window = TelaEyeTrackerMaster()
    window.show()
    app.exec()

