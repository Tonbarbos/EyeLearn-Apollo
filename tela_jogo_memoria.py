from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout, QFrame, QSizePolicy
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap
import qtawesome as qta
import random

from memory_game_logic import MemoryGameLogic # Import the new logic class

class TelaJogoMemoria(QWidget):
    game_finished = pyqtSignal(int, int, int) # score, time_elapsed, errors

    def __init__(self, parent=None):
        super().__init__(parent)
        self.game_logic = MemoryGameLogic() # Instantiate the game logic
        self.game_logic.connect_game_finished(self.game_finished.emit)
        self.game_logic.connect_game_info_updated(self.update_game_info)
        self.game_logic.connect_card_flipped(self._update_card_ui)
        self.game_logic.connect_card_matched(self._mark_card_matched_ui)
        self.game_logic.connect_card_unmatched(self._unflip_card_ui)

        self.card_buttons = {} # Map card_id to QPushButton

        self.timer = QTimer(self) # Timer for UI updates, not game logic
        self.timer.timeout.connect(self.game_logic.update_timer_tick)

        self.setup_ui()
        self.init_game()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter) # Centraliza o conteúdo horizontalmente
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

        title_label = QLabel("Jogo da Memória")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        self.pause_button = QPushButton()
        self.pause_button.setIcon(qta.icon("fa5s.pause", color="white"))
        self.pause_button.setFixedSize(40, 40)
        self.pause_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
            }
        """)
        header_layout.addWidget(self.pause_button)
        main_layout.addWidget(header_frame)

        # --- Informações do Jogo --- #
        game_info_frame = QFrame()
        game_info_frame.setStyleSheet("background-color: white; padding: 15px; border-bottom: 1px solid #E0E0E0;")
        game_info_frame.setMaximumWidth(800) # Limita a largura máxima do frame de informações do jogo
        game_info_layout = QHBoxLayout(game_info_frame)
        game_info_layout.setContentsMargins(20, 5, 20, 5)
        game_info_layout.setSpacing(20)

        # Pontuação
        score_layout = QVBoxLayout()
        score_label_title = QLabel("Pontuação")
        score_label_title.setFont(QFont("Arial", 12))
        score_label_title.setStyleSheet("color: #7F8C8D;")
        score_layout.addWidget(score_label_title)
        self.score_label = QLabel("0")
        self.score_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.score_label.setStyleSheet("color: #2C3E50;")
        score_layout.addWidget(self.score_label)
        game_info_layout.addLayout(score_layout)

        # Recorde
        record_layout = QVBoxLayout()
        record_label_title = QLabel("Recorde")
        record_label_title.setFont(QFont("Arial", 12))
        record_label_title.setStyleSheet("color: #7F8C8D;")
        record_layout.addWidget(record_label_title)
        self.record_label = QLabel("0") # Adicionar recorde real depois
        self.record_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.record_label.setStyleSheet("color: #2C3E50;")
        record_layout.addWidget(self.record_label)
        game_info_layout.addLayout(record_layout)

        game_info_layout.addStretch()

        # Tempo
        time_layout = QVBoxLayout()
        time_label_title = QLabel("Tempo")
        time_label_title.setFont(QFont("Arial", 12))
        time_label_title.setStyleSheet("color: #7F8C8D;")
        time_layout.addWidget(time_label_title)
        self.time_label = QLabel("00:00")
        self.time_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.time_label.setStyleSheet("color: #2C3E50;")
        time_layout.addWidget(self.time_label)
        game_info_layout.addLayout(time_layout)

        # Erros
        errors_layout = QVBoxLayout()
        errors_label_title = QLabel("Erros")
        errors_label_title.setFont(QFont("Arial", 12))
        errors_label_title.setStyleSheet("color: #7F8C8D;")
        errors_layout.addWidget(errors_label_title)
        self.errors_label = QLabel("0")
        self.errors_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.errors_label.setStyleSheet("color: #2C3E50;")
        errors_layout.addWidget(self.errors_label)
        game_info_layout.addLayout(errors_layout)

        main_layout.addWidget(game_info_frame)

        # --- Grid do Jogo --- #
        game_grid_widget = QWidget()
        game_grid_widget.setMaximumWidth(600) # Limita a largura máxima do grid do jogo para evitar esticamento excessivo
        game_grid_widget.setStyleSheet("background-color: #F5F5F5; padding: 20px;")
        self.grid_layout = QGridLayout(game_grid_widget)
        self.grid_layout.setSpacing(10)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(game_grid_widget)

        # --- Controles --- #
        controls_frame = QFrame()
        controls_frame.setStyleSheet("background-color: white; border-top: 1px solid #E0E0E0; padding: 15px;")
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setContentsMargins(20, 5, 20, 5)
        controls_layout.setSpacing(15)

        self.hint_button = QPushButton("Dica")
        self.hint_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.hint_button.setMaximumWidth(300) # Limita a largura máxima do botão de dica
        self.hint_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.hint_button.setFixedHeight(50)
        self.hint_button.setStyleSheet("""
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
        controls_layout.addWidget(self.hint_button)

        self.restart_button = QPushButton("Reiniciar")
        self.restart_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.restart_button.setMaximumWidth(300) # Limita a largura máxima do botão de reiniciar
        self.restart_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.restart_button.setFixedHeight(50)
        self.restart_button.setStyleSheet("""
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
        self.restart_button.clicked.connect(self.init_game) # Connect restart button to init_game
        controls_layout.addWidget(self.restart_button)
        main_layout.addWidget(controls_frame)

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #F5F5F5;")

    def init_game(self):
        # Clear existing cards from UI
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.card_buttons.clear()

        self.game_logic.init_game()
        self.timer.start(1000) # Start UI timer

        rows = 4
        cols = 4

        for card_id in range(len(self.game_logic.cards_data)):
            card_button = QPushButton()
            card_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            card_button.setMinimumSize(70, 70) # Tamanho mínimo para os cards
            card_button.setMaximumSize(100, 100) # Tamanho máximo para os cards
            card_button.setStyleSheet(
                "QPushButton { background-color: white; border-radius: 10px; border: 1px solid #D0D0D0; }"
                "QPushButton:hover { background-color: #F0F0F0; }"
            )
            # Adicionar um ícone de placeholder
            placeholder_icon = qta.icon("fa5s.image", color="#D0D0D0")
            card_button.setIcon(placeholder_icon)
            card_button.setIconSize(card_button.size() * 0.6)

            card_button.clicked.connect(lambda checked, c_id=card_id: self.game_logic.handle_card_click(c_id))
            
            row = card_id // cols
            col = card_id % cols
            self.grid_layout.addWidget(card_button, row, col)
            self.card_buttons[card_id] = card_button

    def _update_card_ui(self, card_id, show_icon):
        card_button = self.card_buttons.get(card_id)
        if not card_button: return

        if show_icon:
            icon_name = self.game_logic.get_card_icon_name(card_id)
            icon = qta.icon(icon_name, color="#4A7C8C") # Cor do ícone
            card_button.setIcon(icon)
            card_button.setIconSize(card_button.size() * 0.6)
            card_button.setStyleSheet(
                "QPushButton { background-color: #E8F4F8; border-radius: 10px; border: 1px solid #4A7C8C; }"
            )
        else:
            # Ícone de placeholder quando virado para baixo
            placeholder_icon = qta.icon("fa5s.image", color="#D0D0D0")
            card_button.setIcon(placeholder_icon)
            card_button.setIconSize(card_button.size() * 0.6)
            card_button.setStyleSheet(
                "QPushButton { background-color: white; border-radius: 10px; border: 1px solid #D0D0D0; }"
                "QPushButton:hover { background-color: #F0F0F0; }"
            )

    def _mark_card_matched_ui(self, card1_id, card2_id):
        card1_button = self.card_buttons.get(card1_id)
        card2_button = self.card_buttons.get(card2_id)
        if card1_button: card1_button.setEnabled(False)
        if card2_button: card2_button.setEnabled(False)
        if card1_button: card1_button.setStyleSheet("QPushButton { background-color: #D4EDDA; color: #155724; border-radius: 10px; border: 1px solid #28A745; } ")
        if card2_button: card2_button.setStyleSheet("QPushButton { background-color: #D4EDDA; color: #155724; border-radius: 10px; border: 1px solid #28A745; } ")

    def _unflip_card_ui(self, card1_id, card2_id):
        # Este método é chamado quando as cartas não combinam e precisam ser viradas para baixo novamente.
        # Revertemos o estilo para o estado 'virado para baixo' e removemos o ícone.
        card1_button = self.card_buttons.get(card1_id)
        card2_button = self.card_buttons.get(card2_id)

        if card1_button:
            placeholder_icon = qta.icon("fa5s.image", color="#D0D0D0")
            card1_button.setIcon(placeholder_icon)
            card1_button.setIconSize(card1_button.size() * 0.6)
            card1_button.setStyleSheet(
                "QPushButton { background-color: white; border-radius: 10px; border: 1px solid #D0D0D0; }"
                "QPushButton:hover { background-color: #F0F0F0; }"
            )
        if card2_button:
            placeholder_icon = qta.icon("fa5s.image", color="#D0D0D0")
            card2_button.setIcon(placeholder_icon)
            card2_button.setIconSize(card2_button.size() * 0.6)
            card2_button.setStyleSheet(
                "QPushButton { background-color: white; border-radius: 10px; border: 1px solid #D0D0D0; }"
                "QPushButton:hover { background-color: #F0F0F0; }"
            )

    def update_game_info(self, score, errors, time_elapsed):
        self.score_label.setText(f"{score}")
        self.errors_label.setText(f"{errors}")
        minutes = time_elapsed // 60
        seconds = time_elapsed % 60
        self.time_label.setText(f"{minutes:02d}:{seconds:02d}")

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    window = TelaJogoMemoria()
    window.show()
    app.exec()

