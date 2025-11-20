from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
import qtawesome as qta
import os

from teacher_dashboard_logic import TeacherDashboardLogic


class TelaDetalhesAluno(QWidget):
    go_to_painel_professor = pyqtSignal()
    logout_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic = TeacherDashboardLogic()
        self.aluno_id = None
        self.setup_ui()

    def set_aluno(self, aluno_id):
        """Chamado pelo main.py para definir qual aluno exibir"""
        self.aluno_id = aluno_id
        self.carregar_dados()

    def carregar_dados(self):
        if not self.aluno_id:
            return

        data = self.logic.get_student_details(self.aluno_id)
        if data:
            self.title_label.setText(f"{data['nomeCompleto']}")

            media = data.get('media_pontuacao', 0)
            self.score_value.setText(f"{int(media)}%")

            # Lógica de diagnóstico
            if media > 0 and media < 50:
                self.diagnosis_card.setStyleSheet("background-color: #FFCDD2; border-radius: 10px; padding: 20px;")
                self.diagnosis_title.setText("Atenção Necessária")
                self.diagnosis_text.setText("O desempenho está abaixo do esperado. Recomenda-se acompanhamento.")
            elif media >= 50:
                self.diagnosis_card.setStyleSheet("background-color: #C8E6C9; border-radius: 10px; padding: 20px;")
                self.diagnosis_title.setText("Desempenho Bom")
                self.diagnosis_text.setText("O aluno apresenta padrões típicos de aprendizado.")
            else:
                self.diagnosis_card.setStyleSheet("background-color: #FFF9C4; border-radius: 10px; padding: 20px;")
                self.diagnosis_title.setText("Sem Dados Suficientes")
                self.diagnosis_text.setText("Realize atividades com o aluno para gerar um diagnóstico.")

            # Carregar o Heatmap do Banco
            heatmap_path = data.get('heatmap_path')

            if heatmap_path and os.path.exists(heatmap_path):
                pixmap = QPixmap(heatmap_path)
                self.heatmap_image_label.setPixmap(pixmap)
                self.heatmap_image_label.setStyleSheet("border: none;")
            else:
                # Placeholder se não houver imagem
                self.heatmap_image_label.clear()
                self.heatmap_image_label.setText("Nenhum mapa de calor disponível.")
                self.heatmap_image_label.setStyleSheet(
                    "border: 1px dashed #CCC; color: #999; qproperty-alignment: AlignCenter;")

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QFrame()
        header.setStyleSheet("background-color: #4A7C8C; padding: 15px;")
        header_layout = QHBoxLayout(header)

        self.back_button = QPushButton()
        self.back_button.setIcon(qta.icon("fa5s.arrow-left", color="white"))
        self.back_button.setStyleSheet("background: transparent; border: none;")
        self.back_button.clicked.connect(self.go_to_painel_professor.emit)
        header_layout.addWidget(self.back_button)

        self.title_label = QLabel("Detalhes do Aluno")
        self.title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: white;")
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()

        main_layout.addWidget(header)

        # Conteúdo
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: #F0F2F5;")

        content = QWidget()
        content.setStyleSheet("background-color: #F0F2F5;")
        layout = QVBoxLayout(content)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Card de Pontuação
        self.score_card = QFrame()
        self.score_card.setMaximumWidth(800)
        self.score_card.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px;")
        score_layout = QVBoxLayout(self.score_card)

        score_title = QLabel("Média Geral")
        score_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_title.setFont(QFont("Arial", 14))
        score_title.setStyleSheet("color: #7F8C8D;")

        self.score_value = QLabel("-")
        self.score_value.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        self.score_value.setStyleSheet("color: #4A7C8C;")
        self.score_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        score_layout.addWidget(score_title)
        score_layout.addWidget(self.score_value)
        layout.addWidget(self.score_card)

        # Card Diagnóstico
        self.diagnosis_card = QFrame()
        self.diagnosis_card.setMaximumWidth(800)
        self.diagnosis_card.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px;")
        diag_layout = QVBoxLayout(self.diagnosis_card)

        self.diagnosis_title = QLabel("Análise")
        self.diagnosis_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.diagnosis_title.setStyleSheet("color: #2C3E50;")

        self.diagnosis_text = QLabel("Aguardando dados...")
        self.diagnosis_text.setFont(QFont("Arial", 12))
        self.diagnosis_text.setWordWrap(True)
        self.diagnosis_text.setStyleSheet("color: #333;")

        diag_layout.addWidget(self.diagnosis_title)
        diag_layout.addWidget(self.diagnosis_text)
        layout.addWidget(self.diagnosis_card)

        # --- CORREÇÃO: Card Mapa de Calor (Heatmap) REINSERIDO ---
        heatmap_card = QFrame()
        heatmap_card.setMaximumWidth(800)
        heatmap_card.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px;")
        heatmap_layout = QVBoxLayout(heatmap_card)

        heatmap_title = QLabel("Mapa de Calor Recente")
        heatmap_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        heatmap_title.setStyleSheet("color: #2C3E50;")
        heatmap_layout.addWidget(heatmap_title)

        # O Label da imagem que estava faltando
        self.heatmap_image_label = QLabel()
        self.heatmap_image_label.setMinimumHeight(300)
        self.heatmap_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.heatmap_image_label.setStyleSheet("border: 1px dashed #CCC; color: #999;")
        self.heatmap_image_label.setScaledContents(True)

        heatmap_layout.addWidget(self.heatmap_image_label)
        layout.addWidget(heatmap_card)
        # ---------------------------------------------------------

        layout.addStretch()
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)


if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication

    app = QApplication([])
    window = TelaDetalhesAluno()
    window.show()
    app.exec()