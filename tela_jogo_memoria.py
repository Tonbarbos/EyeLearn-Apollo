from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGridLayout, QFrame, QSizePolicy, QApplication
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QEvent
from PyQt6.QtGui import QFont, QIcon, QPixmap
import qtawesome as qta
import random
import os
from memory_game_logic import MemoryGameLogic
from database import DatabaseManager
from heatmap_generator import HeatmapGenerator


class TelaJogoMemoria(QWidget):
    game_finished = pyqtSignal(int, int, int)  # score, time_elapsed, errors

    def __init__(self, parent=None):
        super().__init__(parent)
        self.aluno_id_atual = None

        self.game_logic = MemoryGameLogic()
        self.game_logic.connect_game_finished(self.game_finished.emit)
        self.game_logic.connect_game_info_updated(self.update_game_info)
        self.game_logic.connect_card_flipped(self._update_card_ui)
        self.game_logic.connect_card_matched(self._mark_card_matched_ui)
        self.game_logic.connect_card_unmatched(self._unflip_card_ui)
        self.game_logic.connect_game_finished(self.salvar_sessao)

        self.card_buttons = {}
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_logic.update_timer_tick)

        # Inicializa gerador de heatmap
        self.heatmap_gen = HeatmapGenerator(width=800, height=600)

        # CORREÇÃO: Instala um filtro no aplicativo para pegar o mouse EM CIMA dos botões
        QApplication.instance().installEventFilter(self)

        self.setup_ui()
        self.init_game()

    def eventFilter(self, source, event):
        """Monitora o mouse globalmente para gerar o heatmap, mesmo sobre botões."""
        if event.type() == QEvent.Type.MouseMove:
            # Só registra se esta tela estiver visível para o usuário
            if self.isVisible():
                # Converte posição global da tela para posição dentro do widget
                global_pos = event.globalPosition().toPoint()
                local_pos = self.mapFromGlobal(global_pos)

                # Verifica se o mouse está dentro dos limites desta tela
                if self.rect().contains(local_pos):
                    self.heatmap_gen.add_point(local_pos.x(), local_pos.y())

        return super().eventFilter(source, event)

    def set_aluno(self, aluno_id):
        self.aluno_id_atual = aluno_id
        print(f"--- Jogo configurado para o aluno ID: {self.aluno_id_atual} ---")

    def salvar_sessao(self, score, time_elapsed, errors):
        if not self.aluno_id_atual:
            return

        try:
            print("Capturando tela e gerando mapa de calor...")

            # 1. TIRA O PRINT DA TELA DO JOGO
            screenshot = self.grab()
            temp_bg_path = "temp_screenshot.png"
            screenshot.save(temp_bg_path)

            # 2. GERA O HEATMAP USANDO O PRINT COMO FUNDO
            caminho_real_heatmap = self.heatmap_gen.generate_and_save(bg_path=temp_bg_path)

            # Remove o print temporário para não sujar a pasta
            if os.path.exists(temp_bg_path):
                os.remove(temp_bg_path)

            # 3. SALVA NO BANCO (Igual a antes)
            db = DatabaseManager()
            detalhes = f"Jogo da Memória - Score: {score} | Tempo: {time_elapsed}s | Erros: {errors}"

            query = """
                INSERT INTO Sessoes 
                (aluno_id, observacoes, pontuacao_final, tempo_segundos, erros_count, caminhoMapaCalor) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (self.aluno_id_atual, detalhes, score, time_elapsed, errors, caminho_real_heatmap)

            db.execute_query(query, params)
            print(f"✅ Sessão salva com Heatmap (Sobreposto) para Aluno {self.aluno_id_atual}")

            # Reinicia o gerador (mantendo o tamanho correto)
            self.heatmap_gen = HeatmapGenerator(width=800, height=600)

        except Exception as e:
            print(f"❌ Erro ao salvar sessão: {e}")
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        main_layout.setSpacing(0)

        # --- Cabeçalho ---
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #4A7C8C; padding: 15px;")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)

        self.back_button = QPushButton()
        self.back_button.setIcon(qta.icon("fa5s.arrow-left", color="white"))
        self.back_button.setFixedSize(40, 40)
        self.back_button.setStyleSheet(
            "QPushButton { background-color: transparent; border: none; } QPushButton:hover { background-color: rgba(255, 255, 255, 0.1); border-radius: 20px; }")
        header_layout.addWidget(self.back_button)

        title_label = QLabel("Jogo da Memória")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        self.pause_button = QPushButton()
        self.pause_button.setIcon(qta.icon("fa5s.pause", color="white"))
        self.pause_button.setFixedSize(40, 40)
        self.pause_button.setStyleSheet(
            "QPushButton { background-color: transparent; border: none; } QPushButton:hover { background-color: rgba(255, 255, 255, 0.1); border-radius: 20px; }")
        header_layout.addWidget(self.pause_button)
        main_layout.addWidget(header_frame)

        # --- Informações ---
        game_info_frame = QFrame()
        game_info_frame.setStyleSheet("background-color: white; padding: 15px; border-bottom: 1px solid #E0E0E0;")
        game_info_frame.setMaximumWidth(800)
        game_info_layout = QHBoxLayout(game_info_frame)

        # Pontuação
        score_layout = QVBoxLayout()
        score_layout.addWidget(QLabel("Pontuação", styleSheet="color: #7F8C8D; font-size: 12px;"))
        self.score_label = QLabel("0", styleSheet="color: #2C3E50; font-size: 18px; font-weight: bold;")
        score_layout.addWidget(self.score_label)
        game_info_layout.addLayout(score_layout)

        game_info_layout.addStretch()

        # Tempo
        time_layout = QVBoxLayout()
        time_layout.addWidget(QLabel("Tempo", styleSheet="color: #7F8C8D; font-size: 12px;"))
        self.time_label = QLabel("00:00", styleSheet="color: #2C3E50; font-size: 18px; font-weight: bold;")
        time_layout.addWidget(self.time_label)
        game_info_layout.addLayout(time_layout)

        # Erros
        errors_layout = QVBoxLayout()
        errors_layout.addWidget(QLabel("Erros", styleSheet="color: #7F8C8D; font-size: 12px;"))
        self.errors_label = QLabel("0", styleSheet="color: #2C3E50; font-size: 18px; font-weight: bold;")
        errors_layout.addWidget(self.errors_label)
        game_info_layout.addLayout(errors_layout)

        main_layout.addWidget(game_info_frame)

        # --- Grid ---
        game_grid_widget = QWidget()
        game_grid_widget.setMaximumWidth(600)
        game_grid_widget.setStyleSheet("background-color: #F5F5F5; padding: 20px;")
        self.grid_layout = QGridLayout(game_grid_widget)
        self.grid_layout.setSpacing(10)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(game_grid_widget)

        # --- Controles ---
        controls_frame = QFrame()
        controls_frame.setStyleSheet("background-color: white; border-top: 1px solid #E0E0E0; padding: 15px;")
        controls_layout = QHBoxLayout(controls_frame)

        self.hint_button = QPushButton("Dica")
        self.hint_button.setFixedHeight(50)
        self.hint_button.setStyleSheet(
            "QPushButton { background-color: white; color: #4A7C8C; border: 2px solid #4A7C8C; border-radius: 25px; font-size: 16px; font-weight: bold; } QPushButton:hover { background-color: #F0F8FF; }")
        controls_layout.addWidget(self.hint_button)

        self.restart_button = QPushButton("Reiniciar")
        self.restart_button.setFixedHeight(50)
        self.restart_button.setStyleSheet(
            "QPushButton { background-color: #4A7C8C; color: white; border-radius: 25px; font-size: 16px; font-weight: bold; } QPushButton:hover { background-color: #3A6C7C; }")
        self.restart_button.clicked.connect(self.init_game)
        controls_layout.addWidget(self.restart_button)

        main_layout.addWidget(controls_frame)
        self.setLayout(main_layout)

    def init_game(self):
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget: widget.deleteLater()
        self.card_buttons.clear()

        self.game_logic.init_game()
        self.timer.start(1000)

        cols = 4
        for card_id in range(len(self.game_logic.cards_data)):
            btn = QPushButton()
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            btn.setMinimumSize(70, 70)
            btn.setMaximumSize(100, 100)
            btn.setStyleSheet(
                "QPushButton { background-color: white; border-radius: 10px; border: 1px solid #D0D0D0; } QPushButton:hover { background-color: #F0F0F0; }")
            btn.setIcon(qta.icon("fa5s.image", color="#D0D0D0"))
            btn.setIconSize(btn.size() * 0.6)

            # Usando lambda para conectar o clique
            btn.clicked.connect(lambda ch, cid=card_id: self.game_logic.handle_card_click(cid))

            self.grid_layout.addWidget(btn, card_id // cols, card_id % cols)
            self.card_buttons[card_id] = btn

    def _update_card_ui(self, card_id, show_icon):
        btn = self.card_buttons.get(card_id)
        if not btn: return
        if show_icon:
            icon = qta.icon(self.game_logic.get_card_icon_name(card_id), color="#4A7C8C")
            btn.setIcon(icon)
            btn.setStyleSheet(
                "QPushButton { background-color: #E8F4F8; border-radius: 10px; border: 1px solid #4A7C8C; }")
        else:
            btn.setIcon(qta.icon("fa5s.image", color="#D0D0D0"))
            btn.setStyleSheet(
                "QPushButton { background-color: white; border-radius: 10px; border: 1px solid #D0D0D0; }")

    def _mark_card_matched_ui(self, c1, c2):
        for cid in [c1, c2]:
            btn = self.card_buttons.get(cid)
            if btn:
                btn.setEnabled(False)
                btn.setStyleSheet("QPushButton { background-color: #D4EDDA; border: 1px solid #28A745; }")

    def _unflip_card_ui(self, c1, c2):
        self._update_card_ui(c1, False)
        self._update_card_ui(c2, False)

    def update_game_info(self, score, errors, time):
        self.score_label.setText(str(score))
        self.errors_label.setText(str(errors))
        self.time_label.setText(f"{time // 60:02d}:{time % 60:02d}")


if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication

    app = QApplication([])
    w = TelaJogoMemoria()
    w.show()
    app.exec()