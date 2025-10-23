from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QSizePolicy, QSpacerItem
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import qtawesome as qta

class TelaConfiguracoes(QWidget):
    back_to_principal_aluno = pyqtSignal()
    eye_tracker_button_clicked = pyqtSignal()

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

        title_label = QLabel("Configurações")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        main_layout.addWidget(header_frame)

        # --- Área de conteúdo rolável --- #
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #F5F5F5; }")
        content_widget = QWidget()
        content_widget.setMaximumWidth(800) # Limita a largura máxima do conteúdo rolável
        content_widget.setStyleSheet("background-color: #F5F5F5;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter) # Centraliza o conteúdo horizontalmente
        content_layout.setSpacing(20)

        # Seção: Conta e Perfil
        content_layout.addWidget(self._create_section_title("Conta e Perfil"))
        self._add_setting_item(content_layout, "Conta", "fa5s.user", "Gerenciar perfil")
        self._add_setting_item(content_layout, "Privacidade", "fa5s.lock", "Gerenciar permissões e dados")

        # Seção: Preferências
        content_layout.addWidget(self._create_section_title("Preferências"))
        self._add_setting_item(content_layout, "Acessibilidade", "fa5s.star", "Ajustes para necessidades especiais")
        self._add_setting_item(content_layout, "Idioma", "fa5s.globe", "Português (Brasil)")
        self._add_setting_item_with_toggle(content_layout, "Notificações", "fa5s.bell", "Gerenciar alertas e lembretes")
        self.eye_tracker_button = self._add_setting_item(content_layout, "Rastreamento Ocular", "fa5s.eye", "Configurações de rastreamento ocular")

        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # --- Barra de Navegação Inferior --- #
        navbar_frame = QFrame()
        navbar_frame.setStyleSheet("background-color: white; border-top: 1px solid #E0E0E0;")
        navbar_layout = QHBoxLayout(navbar_frame)
        navbar_layout.setContentsMargins(0, 0, 0, 0)
        navbar_layout.setSpacing(0)

        self.nav_home_button = self._create_nav_button("Início", "fa5s.home", False)
        self.nav_atividades_button = self._create_nav_button("Atividades", "fa5s.puzzle-piece", False)
        self.nav_progresso_button = self._create_nav_button("Progresso", "fa5s.chart-line", False)
        self.nav_configuracoes_button = self._create_nav_button("Configurações", "fa5s.cog", True) # Ativo

        navbar_layout.addWidget(self.nav_home_button)
        navbar_layout.addWidget(self.nav_atividades_button)
        navbar_layout.addWidget(self.nav_progresso_button)
        navbar_layout.addWidget(self.nav_configuracoes_button)
        main_layout.addWidget(navbar_frame)

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #F5F5F5;")

        self.back_button.clicked.connect(self.back_to_principal_aluno.emit)
        self.eye_tracker_button.clicked.connect(self.eye_tracker_button_clicked.emit)

    def _create_section_title(self, title):
        label = QLabel(title)
        label.setMaximumWidth(800) # Limita a largura máxima do título da seção
        label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        label.setStyleSheet("color: #2C3E50; margin-top: 10px;")
        return label

    def _add_setting_item(self, layout, title, icon_name, description):
        item_button = QPushButton()
        item_button.setStyleSheet(
            "QPushButton { background-color: white; border: none; text-align: left; padding: 15px; }"
            "QPushButton:hover { background-color: #F5F5F5; }"
        )
        item_button.setMaximumWidth(800) # Limita a largura máxima do item de configuração
        item_layout = QHBoxLayout(item_button)
        item_layout.setContentsMargins(0, 0, 0, 0)

        icon_label = QLabel()
        icon = qta.icon(icon_name, color="#4A7C8C")
        icon_label.setPixmap(icon.pixmap(24, 24))
        item_layout.addWidget(icon_label)

        text_layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14))
        title_label.setStyleSheet("color: #2C3E50;")
        text_layout.addWidget(title_label)

        description_label = QLabel(description)
        description_label.setFont(QFont("Arial", 10))
        description_label.setStyleSheet("color: #7F8C8D;")
        text_layout.addWidget(description_label)
        item_layout.addLayout(text_layout)
        item_layout.addStretch()

        arrow_icon = qta.icon("fa5s.chevron-right", color="#9E9E9E")
        arrow_label = QLabel()
        arrow_label.setPixmap(arrow_icon.pixmap(16, 16))
        item_layout.addWidget(arrow_label)

        layout.addWidget(item_button)
        return item_button # Retorna o botão para que possa ser conectado

    def _add_setting_item_with_toggle(self, layout, title, icon_name, description):
        item_widget = QWidget()
        item_widget.setStyleSheet("background-color: white; border: none; padding: 15px;")
        item_widget.setMaximumWidth(800) # Limita a largura máxima do item de configuração com toggle
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(0, 0, 0, 0)

        icon_label = QLabel()
        icon = qta.icon(icon_name, color="#4A7C8C")
        icon_label.setPixmap(icon.pixmap(24, 24))
        item_layout.addWidget(icon_label)

        text_layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14))
        title_label.setStyleSheet("color: #2C3E50;")
        text_layout.addWidget(title_label)

        description_label = QLabel(description)
        description_label.setFont(QFont("Arial", 10))
        description_label.setStyleSheet("color: #7F8C8D;")
        text_layout.addWidget(description_label)
        item_layout.addLayout(text_layout)
        item_layout.addStretch()

        # Toggle Switch (simplificado, pode ser substituído por um widget customizado)
        toggle_button = QPushButton()
        toggle_button.setFixedSize(50, 30)
        toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #D0D0D0;
                border-radius: 15px;
            }
            QPushButton:checked {
                background-color: #4CAF50;
            }
        """)
        toggle_button.setCheckable(True)
        item_layout.addWidget(toggle_button)

        layout.addWidget(item_widget)

    def _create_nav_button(self, text, icon_name, is_active):
        button = QPushButton()
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.setMinimumHeight(60)
        button_layout = QVBoxLayout(button)
        button_layout.setContentsMargins(0, 5, 0, 5)
        button_layout.setSpacing(2)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_color = "#4A7C8C" if is_active else "#7F8C8D"
        text_color = "#4A7C8C" if is_active else "#7F8C8D"

        icon_label = QLabel()
        icon = qta.icon(icon_name, color=icon_color)
        icon_label.setPixmap(icon.pixmap(24, 24))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text_label = QLabel(text)
        text_label.setFont(QFont("Arial", 10))
        text_label.setStyleSheet(f"color: {text_color};")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(text_label)

        button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #F0F2F5;
            }
        """)
        return button

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    window = TelaConfiguracoes()
    window.show()
    app.exec()

