from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import qtawesome as qta

from congratulations_screen_logic import CongratulationsScreenLogic

class TelaParabens(QWidget):
    go_to_principal_aluno = pyqtSignal()
    logout_requested = pyqtSignal()

    def __init__(self, parent=None, score=0, time_elapsed=0, errors=0):
        super().__init__(parent)
        self.logic = CongratulationsScreenLogic(score, time_elapsed, errors)
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

        title_label = QLabel("Tarefas Concluídas")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        self.share_button = QPushButton()
        self.share_button.setIcon(qta.icon("fa5s.share-alt", color="white"))
        self.share_button.setFixedSize(40, 40)
        self.share_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
            }
        """)
        header_layout.addWidget(self.share_button)
        main_layout.addWidget(header_frame)

        # --- Área de conteúdo rolável --- #
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #F5F5F5; }")
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #F5F5F5;")
        content_widget.setMaximumWidth(800) # Limita a largura máxima do conteúdo rolável
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter) # Centraliza o conteúdo horizontalmente
        content_layout.setSpacing(20)

        # Mensagem de Parabéns
        congrats_label = QLabel(self.logic.get_congratulations_message())
        congrats_label.setMaximumWidth(800) # Limita a largura máxima do label de parabéns
        congrats_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        congrats_label.setStyleSheet("color: #2C3E50;")
        congrats_label.setWordWrap(True)
        content_layout.addWidget(congrats_label)

        subtitle_label = QLabel(self.logic.get_subtitle_message())
        subtitle_label.setMaximumWidth(800) # Limita a largura máxima do subtítulo
        subtitle_label.setFont(QFont("Arial", 14))
        subtitle_label.setStyleSheet("color: #7F8C8D;")
        subtitle_label.setWordWrap(True)
        content_layout.addWidget(subtitle_label)

        content_layout.addSpacing(20)

        # Pontuação Geral
        score_card = QFrame()
        score_card.setMaximumWidth(800) # Limita a largura máxima do card de pontuação
        score_card.setStyleSheet("background-color: white; border-radius: 15px; border: 1px solid #E0E0E0; padding: 20px;")
        score_layout = QVBoxLayout(score_card)
        score_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_layout.setSpacing(10)

        score_title = QLabel("Pontuação Geral")
        score_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        score_title.setStyleSheet("color: #2C3E50;")
        score_layout.addWidget(score_title, alignment=Qt.AlignmentFlag.AlignCenter)

        score_value = QLabel(self.logic.get_formatted_score())
        score_value.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        score_value.setStyleSheet("color: #4A7C8C;")
        score_layout.addWidget(score_value, alignment=Qt.AlignmentFlag.AlignCenter)

        stars_layout = QHBoxLayout()
        stars_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        star_rating = self.logic.get_star_rating()
        for i in range(5):
            star_icon = qta.icon("fa5s.star", color="#FFD700" if i < star_rating else "#D0D0D0")
            star_label = QLabel()
            star_label.setPixmap(star_icon.pixmap(24, 24))
            stars_layout.addWidget(star_label)
        score_layout.addLayout(stars_layout)
        content_layout.addWidget(score_card)

        content_layout.addSpacing(20)

        # Resultados por Atividade
        results_label = QLabel("Resultados por Atividade")
        results_label.setMaximumWidth(800) # Limita a largura máxima do título de resultados por atividade
        results_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        results_label.setStyleSheet("color: #2C3E50;")
        content_layout.addWidget(results_label)

        activity_results = self.logic.get_activity_results()
        # Exemplo de como adicionar um card de resultado de atividade
        self._add_activity_result_card(content_layout, activity_results["activity_name"], activity_results["score"], activity_results["time"], activity_results["errors"], self.logic.get_activity_star_rating())

        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #F5F5F5;")

        self.back_button.clicked.connect(self.go_to_principal_aluno.emit)
        # self.logout_button.clicked.connect(self.logout_requested.emit) # Botão de logout removido do cabeçalho, se necessário, adicionar em outro lugar

    def _add_activity_result_card(self, layout, activity_name, score_str, time_str, errors_str, star_rating):
        card_frame = QFrame()
        card_frame.setMaximumWidth(800) # Limita a largura máxima do card de resultado de atividade
        card_frame.setStyleSheet("background-color: white; border-radius: 15px; border: 1px solid #E0E0E0; padding: 15px;")
        card_layout = QVBoxLayout(card_frame)
        card_layout.setSpacing(10)

        activity_title = QLabel(activity_name)
        activity_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        activity_title.setStyleSheet("color: #2C3E50;")
        card_layout.addWidget(activity_title)

        details_layout = QHBoxLayout()
        details_layout.setSpacing(15)

        # Pontuação
        score_layout = QVBoxLayout()
        score_layout.setSpacing(2)
        score_label_title = QLabel("Pontuação")
        score_label_title.setFont(QFont("Arial", 11))
        score_label_title.setStyleSheet("color: #7F8C8D;")
        score_layout.addWidget(score_label_title)
        score_value = QLabel(score_str)
        score_value.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        score_value.setStyleSheet("color: #4A7C8C;")
        score_layout.addWidget(score_value)
        details_layout.addLayout(score_layout)

        # Tempo
        time_layout = QVBoxLayout()
        time_layout.setSpacing(2)
        time_label_title = QLabel("Tempo")
        time_label_title.setFont(QFont("Arial", 11))
        time_label_title.setStyleSheet("color: #7F8C8D;")
        time_layout.addWidget(time_label_title)
        time_value = QLabel(time_str)
        time_value.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        time_value.setStyleSheet("color: #4A7C8C;")
        time_layout.addWidget(time_value)
        details_layout.addLayout(time_layout)

        # Erros
        errors_layout = QVBoxLayout()
        errors_layout.setSpacing(2)
        errors_label_title = QLabel("Erros")
        errors_label_title.setFont(QFont("Arial", 11))
        errors_label_title.setStyleSheet("color: #7F8C8D;")
        errors_layout.addWidget(errors_label_title)
        errors_value = QLabel(errors_str)
        errors_value.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        errors_value.setStyleSheet("color: #4A7C8C;")
        errors_layout.addWidget(errors_value)
        details_layout.addLayout(errors_layout)

        details_layout.addStretch()

        # Estrelas de avaliação
        activity_stars_layout = QHBoxLayout()
        activity_stars_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        for i in range(5):
            star_icon = qta.icon("fa5s.star", color="#FFD700" if i < star_rating else "#D0D0D0")
            star_label = QLabel()
            star_label.setPixmap(star_icon.pixmap(16, 16))
            activity_stars_layout.addWidget(star_label)
        details_layout.addLayout(activity_stars_layout)

        card_layout.addLayout(details_layout)

        layout.addWidget(card_frame)

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    window = TelaParabens(score=85, time_elapsed=150, errors=3)
    window.show()
    app.exec()

