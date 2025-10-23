from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
import qtawesome as qta

class TelaDetalhesAluno(QWidget):
    go_to_painel_professor = pyqtSignal()
    logout_requested = pyqtSignal()

    def __init__(self, parent=None, aluno_nome="Aluno Desconhecido"):
        super().__init__(parent)
        self.aluno_nome = aluno_nome
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Header --- #
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #4CAF50; color: white; padding: 15px;")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 10, 20, 10)

        self.back_button = QPushButton(qta.icon("fa5s.arrow-left", color="white"), "")
        self.back_button.setStyleSheet("QPushButton { border: none; background-color: transparent; } ")
        header_layout.addWidget(self.back_button)

        title_label = QLabel(f"{self.aluno_nome} - Painel")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        self.logout_button = QPushButton(qta.icon("fa5s.sign-out-alt", color="white"), "")
        self.logout_button.setStyleSheet("QPushButton { border: none; background-color: transparent; } ")
        header_layout.addWidget(self.logout_button)
        main_layout.addWidget(header_frame)

        # --- Scrollable Content Area --- #
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #F0F2F5; }")
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #F0F2F5;")
        content_widget.setMaximumWidth(800) # Limita a largura máxima do conteúdo rolável
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter) # Centraliza o conteúdo horizontalmente
        content_layout.setSpacing(15)

        # Pontuação Geral
        score_card = QFrame()
        score_card.setMaximumWidth(800) # Limita a largura máxima do card de pontuação
        score_card.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px;")
        score_layout = QVBoxLayout(score_card)
        score_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        score_title = QLabel("Pontuação Geral")
        score_title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        score_title.setStyleSheet("color: #333;")
        score_layout.addWidget(score_title, alignment=Qt.AlignmentFlag.AlignCenter)

        score_value = QLabel("100%") # Pontuação hipotética
        score_value.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        score_value.setStyleSheet("color: #4CAF50;")
        score_layout.addWidget(score_value, alignment=Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(score_card)

        content_layout.addSpacing(20)

        # Possível Diagnóstico
        diagnosis_card = QFrame()
        diagnosis_card.setMaximumWidth(800) # Limita a largura máxima do card de diagnóstico
        diagnosis_card.setStyleSheet("background-color: #FFC107; border-radius: 10px; padding: 20px;")
        diagnosis_layout = QVBoxLayout(diagnosis_card)

        diagnosis_title = QLabel("Diagnóstico")
        diagnosis_title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        diagnosis_title.setStyleSheet("color: white;")
        diagnosis_layout.addWidget(diagnosis_title)

        diagnosis_text = QLabel("Os padrões de eye tracking e desempenho cognitivo sugerem indicadores compatíveis com TDAH (Transtorno do Déficit de Atenção e Hiperatividade). Esta é uma análise preliminar. Recomenda-se avaliação clínica completa por profissional especializado.")
        diagnosis_text.setFont(QFont("Arial", 12))
        diagnosis_text.setStyleSheet("color: white;")
        diagnosis_text.setWordWrap(True)
        diagnosis_layout.addWidget(diagnosis_text)
        content_layout.addWidget(diagnosis_card)

        content_layout.addSpacing(20)

        # Mapa Ocular (Heatmap)
        heatmap_card = QFrame()
        heatmap_card.setMaximumWidth(800) # Limita a largura máxima do card do mapa de calor
        heatmap_card.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px;")
        heatmap_layout = QVBoxLayout(heatmap_card)

        heatmap_title = QLabel("Mapa de Calor")
        heatmap_title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        heatmap_title.setStyleSheet("color: #333;")
        heatmap_layout.addWidget(heatmap_title)

        # Placeholder para o heatmap
        self.heatmap_image_label = QLabel()
        heatmap_pixmap = QPixmap("home/assets/heatmap_exemplo.jpeg")
        # Escalar a imagem para um tamanho razoável ou deixar o layout lidar com isso inicialmente
        # Por enquanto, vamos apenas definir o pixmap e ajustar o tamanho do QLabel
        self.heatmap_image_label.setPixmap(heatmap_pixmap)
        self.heatmap_image_label.setScaledContents(True) # Permite que o QLabel escale a imagem para preencher o espaço
        self.heatmap_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.heatmap_image_label.setStyleSheet("border: 1px dashed #CCC; min-height: 200px; color: #999;")
        self.heatmap_image_label.setMinimumHeight(200) # Garante uma altura mínima para a imagem
        heatmap_layout.addWidget(self.heatmap_image_label)
        content_layout.addWidget(heatmap_card)

        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #F0F2F5;")

        self.back_button.clicked.connect(self.go_to_painel_professor.emit)
        self.logout_button.clicked.connect(self.logout_requested.emit)

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    window = TelaDetalhesAluno(aluno_nome="Maria Silva")
    window.show()
    app.exec()
