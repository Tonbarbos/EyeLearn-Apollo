from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QSizePolicy, QSpacerItem
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
import qtawesome as qta
import os

from teacher_dashboard_logic import TeacherDashboardLogic

class TelaPainelProfessor(QWidget):
    go_to_aluno_detalhes = pyqtSignal(str)
    logout_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic = TeacherDashboardLogic()
        self.setup_ui()

    def setup_ui(self):
        # Construir o caminho absoluto para a imagem do mapa de calor
        # Usar o diretório do script atual como base para o caminho relativo
        # Definir caminhos potenciais para a imagem
        possible_image_paths = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "heatmap_exemplo.jpeg"),
            os.path.join(os.getcwd(), "home", "assets", "heatmap_exemplo.jpeg"),
            os.path.join(os.getcwd(), "assets", "heatmap_exemplo.jpeg"),
            "assets/heatmap_exemplo.jpeg", # Caminho relativo simples
            "heatmap_exemplo.jpeg" # Se estiver na raiz do projeto
        ]

        found_image_path = None
        for p in possible_image_paths:
            print(f"DEBUG: Tentando carregar imagem de: {p}")
            if os.path.exists(p):
                found_image_path = p
                print(f"DEBUG: Imagem encontrada em: {found_image_path}")
                break
        
        if found_image_path:
            image_path = found_image_path
        else:
            image_path = "" # Definir como vazio se não for encontrada, para que o fallback seja ativado

        print(f"DEBUG: Diretório de trabalho atual: {os.getcwd()}")
        print(f"DEBUG: Caminho absoluto da imagem: {image_path}")

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
        header_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        title_label = QLabel("Painel de Desempenho")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white;")
        header_layout.addWidget(title_label)
        header_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

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
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter) # Centraliza o conteúdo horizontalmente
        content_layout.setSpacing(20)

        # Informações do Aluno (Exemplo - substituir por dados reais)
        student_info_card = QFrame()
        student_info_card.setStyleSheet("background-color: white; border-radius: 15px; border: 1px solid #E0E0E0; padding: 20px;")
        student_info_card.setMaximumWidth(800) # Limita a largura máxima do card de informações
        student_info_layout = QVBoxLayout(student_info_card)
        student_info_layout.setSpacing(5)

        student_name_label = QLabel("Maria Silva")
        student_name_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        student_name_label.setStyleSheet("color: #2C3E50;")
        student_info_layout.addWidget(student_name_label)

        student_details_label = QLabel("Idade: 10 anos | Turma: 4B | ID: $72106")
        student_details_label.setFont(QFont("Arial", 12))
        student_details_label.setStyleSheet("color: #7F8C8D;")
        student_info_layout.addWidget(student_details_label)
        content_layout.addWidget(student_info_card)

        # Possível Diagnóstico
        diagnosis_card = QFrame()
        diagnosis_card.setStyleSheet("background-color: #FFF3CD; border-radius: 15px; border: 1px solid #FFE082; padding: 20px;")
        diagnosis_card.setMaximumWidth(800) # Limita a largura máxima do card de diagnóstico
        diagnosis_layout = QHBoxLayout(diagnosis_card)
        diagnosis_layout.setSpacing(15)

        alert_icon_label = QLabel()
        alert_icon = qta.icon("fa5s.exclamation-triangle", color="#FFA000")
        alert_icon_label.setPixmap(alert_icon.pixmap(32, 32))
        diagnosis_layout.addWidget(alert_icon_label)

        diagnosis_text_layout = QVBoxLayout()
        diagnosis_title = QLabel("Possível Diagnóstico")
        diagnosis_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        diagnosis_title.setStyleSheet("color: #2C3E50;")
        diagnosis_text_layout.addWidget(diagnosis_title)

        diagnosis_message = QLabel("O aluno pode apresentar dificuldades de aprendizagem ou outras questões relacionadas.")
        diagnosis_message.setFont(QFont("Arial", 12))
        diagnosis_message.setStyleSheet("color: #7F8C8D;")
        diagnosis_message.setWordWrap(True)
        diagnosis_text_layout.addWidget(diagnosis_message)
        diagnosis_layout.addLayout(diagnosis_text_layout)
        content_layout.addWidget(diagnosis_card)

        # Mapa de Calor
        heatmap_card = QFrame()
        heatmap_card.setStyleSheet("background-color: white; border-radius: 15px; border: 1px solid #E0E0E0; padding: 20px;")
        heatmap_card.setMaximumWidth(800) # Limita a largura máxima do card do mapa de calor
        heatmap_layout = QVBoxLayout(heatmap_card)
        heatmap_layout.setSpacing(10)

        heatmap_title = QLabel("Mapa de Calor")
        heatmap_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        heatmap_title.setStyleSheet("color: #2C3E50;")
        heatmap_layout.addWidget(heatmap_title)

        self.heatmap_image_label = QLabel()
        self.heatmap_image_label.setScaledContents(True) # Permite que a imagem seja redimensionada para preencher o QLabel
        self.heatmap_image_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred) # Altera a política de tamanho para preferencial
        self.heatmap_image_label.setMinimumHeight(200) # Garante uma altura mínima para a imagem
        self.heatmap_image_label.setMinimumSize(100, 100) # Garante um tamanho mínimo para o QLabel
        self.heatmap_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if image_path and os.path.exists(image_path):
            heatmap_pixmap = QPixmap(image_path)
            if not heatmap_pixmap.isNull():
                self.heatmap_image_label.setPixmap(heatmap_pixmap)
                print(f"DEBUG: Imagem do mapa de calor carregada com sucesso de {image_path}")
            else:
                print(f"DEBUG: Falha ao carregar QPixmap de {image_path}. O arquivo pode estar corrompido ou não é uma imagem válida.")
                self.heatmap_image_label.setText("Erro: Imagem não pôde ser carregada.")
        else:
            print(f"DEBUG: Arquivo de imagem não encontrado em {image_path}")
            self.heatmap_image_label.setText("Erro: Imagem não encontrada.")

        heatmap_layout.addWidget(self.heatmap_image_label)
        content_layout.addWidget(heatmap_card)
        
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
        self.nav_alunos_button = self._create_nav_button("Alunos", "fa5s.users", True)
        self.nav_relatorios_button = self._create_nav_button("Relatórios", "fa5s.chart-bar", False)
        self.nav_configuracoes_button = self._create_nav_button("Configurações", "fa5s.cog", False)

        navbar_layout.addWidget(self.nav_home_button)
        navbar_layout.addWidget(self.nav_alunos_button)
        navbar_layout.addWidget(self.nav_relatorios_button)
        navbar_layout.addWidget(self.nav_configuracoes_button)
        main_layout.addWidget(navbar_frame)

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #F5F5F5;")

        self.back_button.clicked.connect(self.logout_requested.emit)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # O QLabel com setScaledContents(True) e SizePolicy.Expanding deve lidar com o redimensionamento automaticamente
        # Não é necessário chamar update() explicitamente aqui, a menos que haja lógica de desenho personalizada

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
        button_layout.addWidget(icon_label)

        text_label = QLabel(text)
        text_label.setFont(QFont("Arial", 9))
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
    window = TelaPainelProfessor()
    window.show()
    app.exec()

