from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QFrame, QSizePolicy, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import qtawesome as qta

from student_dashboard_logic import StudentDashboardLogic


class TelaPrincipalAluno(QWidget):
    # Sinais para navegação
    go_to_atividades = pyqtSignal()
    go_to_progresso = pyqtSignal()
    go_to_configuracoes = pyqtSignal()
    go_to_jogo_memoria = pyqtSignal()
    logout_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic = StudentDashboardLogic()
        self.setup_ui()

    def set_aluno(self, aluno_id):
        """Recebe o ID do main.py e atualiza a tela"""
        print(f"--- Tela Principal: Recebi o ID {aluno_id}. Atualizando... ---")  # Debug
        self.logic.set_student_id(aluno_id)
        self.refresh_ui()

    def refresh_ui(self):
        """Atualiza os widgets com os dados novos do banco"""
        info = self.logic.get_student_info()
        print(f"--- Tela Principal: Dados recebidos da lógica: {info} ---")  # Debug

        # Atualiza os textos (agora funciona porque setup_ui usa self.)
        self.greeting_label.setText(self.logic.get_greeting_message())
        self.info_label.setText(f"{info['class']}")
        self.level_text.setText(f"Nível {info['level']}")

        # Opcional: Atualizar lista de atividades recentes aqui se necessário
        # self._refresh_recent_activities()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Cabeçalho ---
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #4A7C8C; padding: 20px;")
        header_layout = QVBoxLayout(header_frame)
        header_frame.setMaximumWidth(800)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        header_layout.setContentsMargins(20, 15, 20, 15)
        header_layout.setSpacing(10)

        # Linha superior: saudação e notificação
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)

        student_info = self.logic.get_student_info()  # Dados iniciais (Visitante)

        # CORREÇÃO: Usando self.greeting_label para poder atualizar depois
        self.greeting_label = QLabel(self.logic.get_greeting_message())
        self.greeting_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.greeting_label.setMaximumWidth(600)
        self.greeting_label.setStyleSheet("color: white;")
        top_layout.addWidget(self.greeting_label)

        top_layout.addStretch()

        notification_button = QPushButton()
        notification_button.setIcon(qta.icon("fa5s.bell", color="white"))
        notification_button.setFixedSize(40, 40)
        notification_button.setStyleSheet("""
            QPushButton { background-color: transparent; border: none; }
            QPushButton:hover { background-color: rgba(255, 255, 255, 0.1); border-radius: 20px; }
        """)
        top_layout.addWidget(notification_button)
        header_layout.addLayout(top_layout)

        # Linha inferior: informações do aluno
        info_layout = QHBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)

        # CORREÇÃO: Usando self.info_label
        self.info_label = QLabel(f"{student_info['class']}")
        self.info_label.setMaximumWidth(600)
        self.info_label.setFont(QFont("Arial", 14))
        self.info_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        info_layout.addWidget(self.info_label)

        info_layout.addStretch()

        level_widget = QWidget()
        level_widget.setMaximumWidth(200)
        level_layout = QHBoxLayout(level_widget)
        level_layout.setContentsMargins(10, 5, 10, 5)
        level_layout.setSpacing(5)
        level_widget.setStyleSheet("QWidget { background-color: rgba(255, 255, 255, 0.2); border-radius: 15px; }")

        level_icon_label = QLabel()
        level_icon = qta.icon("fa5s.star", color="#FFD700")
        level_icon_label.setPixmap(level_icon.pixmap(16, 16))
        level_layout.addWidget(level_icon_label)

        # CORREÇÃO: Usando self.level_text
        self.level_text = QLabel(f"Nível {student_info['level']}")
        self.level_text.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.level_text.setStyleSheet("color: white;")
        level_layout.addWidget(self.level_text)

        info_layout.addWidget(level_widget)
        header_layout.addLayout(info_layout)

        main_layout.addWidget(header_frame)

        # --- Área de conteúdo rolável ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #F5F5F5; }")

        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #F5F5F5;")
        content_widget.setMaximumWidth(800)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        content_layout.setSpacing(20)

        # Atividades Disponíveis
        available_title = QLabel("Atividades Disponíveis")
        available_title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        available_title.setMaximumWidth(800)
        available_title.setStyleSheet("color: #2C3E50;")
        content_layout.addWidget(available_title)

        # Grid de atividades
        activities_grid = QGridLayout()
        activities_grid.setSpacing(15)
        activities_grid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        activities = self.logic.get_available_activities()
        for i, activity in enumerate(activities):
            row = i // 2
            col = i % 2
            card = self._create_activity_card(
                activity["title"], activity["icon"], activity["status"], activity["color"]
            )
            if activity["title"] == "Jogo da Memória":
                self.jogo_memoria_button = card
                self.jogo_memoria_button.clicked.connect(self.go_to_jogo_memoria.emit)
            activities_grid.addWidget(card, row, col)

        activities_grid_container = QWidget()
        activities_grid_container.setMaximumWidth(800)
        activities_grid_container.setLayout(activities_grid)
        content_layout.addWidget(activities_grid_container)

        # Atividades Recentes
        recent_title = QLabel("Atividades Recentes")
        recent_title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        recent_title.setMaximumWidth(800)
        recent_title.setStyleSheet("color: #2C3E50;")
        content_layout.addWidget(recent_title)

        # Carrega atividades (vazio inicialmente se não tiver aluno)
        for activity in self.logic.get_recent_activities():
            recent_card = self._create_recent_activity_card(
                activity["title"], activity["icon"], activity["score"], activity["date"]
            )
            content_layout.addWidget(recent_card)

        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # Barra de navegação inferior
        nav_bar = QFrame()
        nav_bar.setMaximumWidth(800)
        nav_bar.setStyleSheet("background-color: white; border-top: 1px solid #E0E0E0;")
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(0, 5, 0, 5)
        nav_layout.setSpacing(0)

        self.nav_home_button = self._add_nav_button(nav_layout, "Início", "fa5s.home", True)
        self.nav_home_button.setMaximumWidth(150)
        self.nav_atividades_button = self._add_nav_button(nav_layout, "Atividades", "fa5s.th-list")
        self.nav_atividades_button.setMaximumWidth(150)
        self.nav_progresso_button = self._add_nav_button(nav_layout, "Progresso", "fa5s.chart-bar")
        self.nav_progresso_button.setMaximumWidth(150)
        self.nav_configuracoes_button = self._add_nav_button(nav_layout, "Configurações", "fa5s.cog")
        self.nav_configuracoes_button.setMaximumWidth(150)
        self.nav_configuracoes_button.clicked.connect(self.go_to_configuracoes.emit)

        self.nav_logout_button = self._add_nav_button(nav_layout, "Sair", "fa5s.sign-out-alt")
        self.nav_logout_button.setMaximumWidth(150)
        self.nav_logout_button.clicked.connect(self.logout_requested.emit)

        main_layout.addWidget(nav_bar)

    def _create_activity_card(self, title, icon_name, status, color):
        card = QPushButton()
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        card.setMinimumHeight(140)
        card.setMaximumWidth(380)
        card.setStyleSheet(f"""
            QPushButton {{ background-color: white; border-radius: 15px; border: none; text-align: center; }}
            QPushButton:hover {{ background-color: #F8F9FA; }}
            QPushButton:pressed {{ background-color: #E8E9EA; }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.setSpacing(10)

        icon_container = QWidget()
        icon_container.setFixedSize(60, 60)
        icon_container.setStyleSheet(f"QWidget {{ background-color: {color}; border-radius: 30px; }}")
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.setContentsMargins(0, 0, 0, 0)

        icon_label = QLabel()
        icon = qta.icon(icon_name, color="white")
        icon_label.setPixmap(icon.pixmap(30, 30))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(icon_label)

        card_layout.addWidget(icon_container, alignment=Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2C3E50;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        card_layout.addWidget(title_label)

        status_label = QLabel(status)
        status_label.setFont(QFont("Arial", 10))
        status_label.setStyleSheet(f"color: {color};")
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(status_label)

        return card

    def _create_recent_activity_card(self, title, icon_name, score, date):
        card = QFrame()
        card.setMaximumWidth(800)
        card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; border: none; }")
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.setSpacing(15)

        icon_container = QWidget()
        icon_container.setFixedSize(40, 40)
        icon_container.setStyleSheet("QWidget { background-color: #7FB3D5; border-radius: 20px; }")
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.setContentsMargins(0, 0, 0, 0)

        icon_label = QLabel()
        icon = qta.icon(icon_name, color="white")
        icon_label.setPixmap(icon.pixmap(20, 20))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(icon_label)

        card_layout.addWidget(icon_container)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2C3E50;")
        text_layout.addWidget(title_label)

        info_layout = QHBoxLayout()
        date_label = QLabel(date)
        date_label.setFont(QFont("Arial", 11))
        date_label.setStyleSheet("color: #7F8C8D;")
        info_layout.addWidget(date_label)
        info_layout.addStretch()
        text_layout.addLayout(info_layout)

        card_layout.addLayout(text_layout)

        score_label = QLabel(score)
        score_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        score_label.setStyleSheet("color: #4A7C8C;")
        card_layout.addWidget(score_label)

        return card

    def _add_nav_button(self, layout, text, icon_name, is_active=False):
        button = QPushButton()
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.setMinimumHeight(60)

        btn_layout = QVBoxLayout(button)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_layout.setSpacing(5)

        icon_color = "#4A7C8C" if is_active else "#95A5A6"
        text_color = "#4A7C8C" if is_active else "#95A5A6"

        icon = qta.icon(icon_name, color=icon_color)
        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(24, 24))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text_label = QLabel(text)
        text_label.setFont(QFont("Arial", 10))
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setStyleSheet(f"color: {text_color};")

        btn_layout.addWidget(icon_label)
        btn_layout.addWidget(text_label)

        button.setStyleSheet("""
            QPushButton { background-color: transparent; border: none; }
            QPushButton:hover { background-color: #F0F0F0; }
        """)

        layout.addWidget(button)
        return button


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    app = QApplication([])
    window = TelaPrincipalAluno()
    window.show()
    app.exec()