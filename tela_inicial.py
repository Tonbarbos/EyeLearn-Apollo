from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPainter, QColor, QBrush
import qtawesome as qta

class TelaInicial(QWidget):
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

        # Seleção de perfil
        profile_selection_label = QLabel("Selecione seu perfil de acesso")
        profile_selection_label.setMaximumWidth(400) # Limita a largura máxima do label de seleção de perfil
        profile_selection_label.setFont(QFont("Arial", 14))
        profile_selection_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        profile_selection_label.setStyleSheet("color: #2C3E50;")
        main_layout.addWidget(profile_selection_label)

        main_layout.addSpacing(20)

        # Botão Aluno
        self.aluno_button = self._create_profile_button("Aluno", "fa5s.user-graduate", "#4A7C8C", "white", hover_color="#3A6C7C", pressed_color="#2A5C6C")
        main_layout.addWidget(self.aluno_button)

        main_layout.addSpacing(15)

        # Botão Professor
        self.professor_button = self._create_profile_button("Professor", "fa5s.chalkboard-teacher", "white", "#4A7C8C", border="2px solid #4A7C8C", hover_color="#F0F8FF", pressed_color="#E0F0FF")
        main_layout.addWidget(self.professor_button)

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

    def _lighten_color(self, hex_color, factor):
        hex_color = hex_color.lstrip("#")
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = [min(255, int(c + (255 - c) * factor)) for c in rgb]
        return f"#{r:02x}{g:02x}{b:02x}"

    def _create_profile_button(self, text, icon_name, bg_color, text_color, border="none", hover_color=None, pressed_color=None):
        if hover_color is None:
            hover_color = self._lighten_color(bg_color, 0.1)
        if pressed_color is None:
            pressed_color = self._lighten_color(bg_color, 0.2)
        button = QPushButton()
        button.setFixedHeight(60)
        button.setMaximumWidth(400) # Limita a largura máxima dos botões de perfil
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: {border};
                border-radius: 30px;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
        """)
        
        layout = QHBoxLayout(button)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        icon = qta.icon(icon_name, color=text_color)
        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(24, 24))
        layout.addWidget(icon_label)
        
        text_label = QLabel(text)
        text_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        text_label.setStyleSheet(f"color: {text_color};")
        layout.addWidget(text_label)
        layout.addStretch()
        
        return button

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    window = TelaInicial()
    window.show()
    app.exec()

