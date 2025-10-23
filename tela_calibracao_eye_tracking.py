from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar, QSizePolicy, QFrame
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap
import qtawesome as qta

class TelaCalibracaoEyeTracking(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Cabeçalho
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

        title_label = QLabel("Calibração de Rastreamento Ocular")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        info_button = QPushButton()
        info_button.setIcon(qta.icon("fa5s.question-circle", color="white"))
        info_button.setFixedSize(40, 40)
        info_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
            }
        """)
        header_layout.addWidget(info_button)
        main_layout.addWidget(header_frame)

        # Área de conteúdo
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Título da calibração
        calibration_title = QLabel("Calibração do Olhar")
        calibration_title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        calibration_title.setStyleSheet("color: #2C3E50;")
        content_layout.addWidget(calibration_title)

        # Instruções
        instructions_label = QLabel("Siga o ponto com seus olhos enquanto ele se move pela tela.")
        instructions_label.setFont(QFont("Arial", 14))
        instructions_label.setStyleSheet("color: #7F8C8D;")
        instructions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions_label.setWordWrap(True)
        content_layout.addWidget(instructions_label)

        content_layout.addSpacing(30)

        # Placeholder para animação/gráfico de calibração (substituir por widget real)
        eye_icon_label = QLabel()
        eye_icon = qta.icon("fa5s.eye", color="#4A7C8C")
        eye_icon_label.setPixmap(eye_icon.pixmap(128, 128))
        eye_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(eye_icon_label)

        content_layout.addSpacing(30)

        # Status de detecção de olhos
        status_layout = QHBoxLayout()
        status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        check_icon_label = QLabel()
        check_icon = qta.icon("fa5s.check-circle", color="#28A745")
        check_icon_label.setPixmap(check_icon.pixmap(20, 20))
        status_layout.addWidget(check_icon_label)

        eyes_detected_label = QLabel("Olhos detectados")
        eyes_detected_label.setFont(QFont("Arial", 14))
        eyes_detected_label.setStyleSheet("color: #28A745;")
        status_layout.addWidget(eyes_detected_label)
        content_layout.addLayout(status_layout)

        # Barra de progresso da calibração
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(70) # Exemplo de progresso
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #E0E0E0;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background-color: #4A7C8C;
                border-radius: 4px;
            }
        """)
        content_layout.addWidget(self.progress_bar)

        content_layout.addStretch()

        # Botões de ação
        self.start_activity_button = QPushButton("Iniciar Atividade")
        self.start_activity_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.start_activity_button.setFixedHeight(50)
        self.start_activity_button.setStyleSheet("""
            QPushButton {
                background-color: #4A7C8C;
                color: white;
                border-radius: 25px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #3A6C7C;
            }
            QPushButton:pressed {
                background-color: #2A5C6C;
            }
        """)
        content_layout.addWidget(self.start_activity_button)

        self.skip_calibration_button = QPushButton("Pular calibração")
        self.skip_calibration_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.skip_calibration_button.setFixedHeight(50)
        self.skip_calibration_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #4A7C8C;
                border: 2px solid #4A7C8C;
                border-radius: 25px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #F0F8FF;
            }
            QPushButton:pressed {
                background-color: #E0F0FF;
            }
        """)
        content_layout.addWidget(self.skip_calibration_button)

        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #F5F5F5;")

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    window = TelaCalibracaoEyeTracking()
    window.show()
    app.exec()

