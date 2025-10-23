from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import qtawesome as qta

class TelaFimSessao(QWidget):
    go_to_nova_sessao_aluno = pyqtSignal()
    go_to_professor_login = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter) # Centraliza o conteúdo horizontalmente
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(20)

        # Logo circular
        logo_label = QLabel()
        logo_label.setFixedSize(100, 100)
        logo_label.setMaximumWidth(400) # Limita a largura máxima do logo
        logo_label.setStyleSheet("""
            QLabel {
                background-color: #4A7C8C;
                border-radius: 50px;
                color: white;
                font-size: 18px;
                font-weight: bold;
                qproperty-alignment: AlignCenter;
            }
        """)
        logo_label.setText("Eye\nLearn")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Título principal
        title_label = QLabel("EyeLearn")
        title_label.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        title_label.setMaximumWidth(400) # Limita a largura máxima do título
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2C3E50;")
        main_layout.addWidget(title_label)

        # Subtítulo
        subtitle_label = QLabel("Avaliação Neurocognitiva")
        subtitle_label.setFont(QFont("Arial", 16))
        subtitle_label.setMaximumWidth(400) # Limita a largura máxima do subtítulo
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #7F8C8D;")
        main_layout.addWidget(subtitle_label)

        main_layout.addSpacing(40)

        # Mensagem de sessão concluída
        session_message_container = QWidget()
        session_message_container.setMaximumWidth(600) # Limita a largura máxima da mensagem de sessão
        session_message_layout = QHBoxLayout(session_message_container)
        session_message_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        check_icon_label = QLabel()
        check_icon = qta.icon("fa5s.check-circle", color="#28A745")
        check_icon_label.setPixmap(check_icon.pixmap(24, 24))
        session_message_layout.addWidget(check_icon_label)

        session_title = QLabel("Sessão concluída com sucesso!")
        session_title.setMaximumWidth(600) # Limita a largura máxima do título da sessão
        session_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        session_title.setStyleSheet("color: #2C3E50;")
        session_message_layout.addWidget(session_title)
        main_layout.addWidget(session_message_container)

        session_subtitle = QLabel("Obrigado por participar! Seus resultados foram registrados e estão disponíveis para análise.")
        session_subtitle.setMaximumWidth(600) # Limita a largura máxima do subtítulo da sessão
        session_subtitle.setFont(QFont("Arial", 14))
        session_subtitle.setStyleSheet("color: #7F8C8D;")
        session_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        session_subtitle.setWordWrap(True)
        main_layout.addWidget(session_subtitle)

        main_layout.addSpacing(20)

        # Botão Nova Sessão como Aluno
        self.nova_sessao_aluno_button = QPushButton("Nova Sessão como Aluno")
        self.nova_sessao_aluno_button.setMaximumWidth(400) # Limita a largura máxima do botão
        self.nova_sessao_aluno_button.setFixedHeight(60)
        self.nova_sessao_aluno_button.setStyleSheet("""
            QPushButton {
                background-color: #4A7C8C;
                color: white;
                border-radius: 30px;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #3A6C7C;
            }
            QPushButton:pressed {
                background-color: #2A5C6C;
            }
        """)
        main_layout.addWidget(self.nova_sessao_aluno_button)

        main_layout.addSpacing(15)

        # Botão Entrar como Professor
        self.professor_login_button = QPushButton("Entrar como Professor")
        self.professor_login_button.setMaximumWidth(400) # Limita a largura máxima do botão
        self.professor_login_button.setFixedHeight(60)
        self.professor_login_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #4A7C8C;
                border: 2px solid #4A7C8C;
                border-radius: 30px;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #F0F8FF;
            }
            QPushButton:pressed {
                background-color: #E0F0FF;
            }
        """)
        main_layout.addWidget(self.professor_login_button)

        main_layout.addStretch()

        # Versão
        version_label = QLabel("Versão 2.1.0")
        version_label.setMaximumWidth(400) # Limita a largura máxima da versão
        version_label.setFont(QFont("Arial", 12))
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("color: #95A5A6;")
        main_layout.addWidget(version_label)

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #E8F4F8;")

        self.nova_sessao_aluno_button.clicked.connect(self.go_to_nova_sessao_aluno.emit)
        self.professor_login_button.clicked.connect(self.go_to_professor_login.emit)

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    window = TelaFimSessao()
    window.show()
    app.exec()

