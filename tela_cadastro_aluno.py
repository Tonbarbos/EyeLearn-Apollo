from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QComboBox, QDateEdit, QFormLayout, QSizePolicy, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
import qtawesome as qta

class TelaCadastroAluno(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Cabeçalho
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

        title_label = QLabel("Cadastro de Aluno")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        main_layout.addWidget(header_frame)

        # Área de conteúdo rolável
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #F5F5F5; }")
        
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #F5F5F5;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter) # Centraliza o conteúdo horizontalmente
        content_layout.setSpacing(20)

        # Título e subtítulo
        cadastro_title = QLabel("Cadastro")
        cadastro_title.setMaximumWidth(800) # Limita a largura máxima do título
        cadastro_title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        cadastro_title.setStyleSheet("color: #2C3E50;")
        content_layout.addWidget(cadastro_title)

        cadastro_subtitle = QLabel("Preencha os dados do aluno para continuar")
        cadastro_subtitle.setMaximumWidth(800) # Limita a largura máxima do subtítulo
        cadastro_subtitle.setFont(QFont("Arial", 14))
        cadastro_subtitle.setStyleSheet("color: #7F8C8D;")
        content_layout.addWidget(cadastro_subtitle)

        content_layout.addSpacing(20)

        # Seção: Informações Pessoais
        personal_section = self._create_section_header("Informações Pessoais", "fa5s.user")
        personal_section.setMaximumWidth(800) # Limita a largura máxima da seção
        content_layout.addWidget(personal_section)

        # Nome Completo
        nome_label = QLabel("Nome Completo *")
        nome_label.setMaximumWidth(800) # Limita a largura máxima do label
        nome_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        nome_label.setStyleSheet("color: #2C3E50;")
        content_layout.addWidget(nome_label)

        self.nome_completo_input = QLineEdit()
        self.nome_completo_input.setMaximumWidth(800) # Limita a largura máxima do input
        self.nome_completo_input.setPlaceholderText("Digite o nome completo")
        self.nome_completo_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 1px solid #D0D0D0;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #4A7C8C;
            }
        """)
        content_layout.addWidget(self.nome_completo_input)

        # Data de Nascimento e Gênero
        date_gender_container = QWidget()
        date_gender_container.setMaximumWidth(800)
        date_gender_layout = QHBoxLayout(date_gender_container)
        date_gender_layout.setSpacing(15)

        # Data de Nascimento
        date_layout = QVBoxLayout()
        date_label = QLabel("Data de Nascimento *")
        date_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        date_label.setStyleSheet("color: #2C3E50;")
        date_layout.addWidget(date_label)

        self.data_nascimento_input = QDateEdit()
        self.data_nascimento_input.setCalendarPopup(True)
        self.data_nascimento_input.setDate(QDate.currentDate())
        self.data_nascimento_input.setDisplayFormat("dd/MM/yyyy")
        self.data_nascimento_input.setStyleSheet("""
            QDateEdit {
                padding: 12px;
                border: 1px solid #D0D0D0;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
            }
            QDateEdit:focus {
                border: 2px solid #4A7C8C;
            }
        """)
        date_layout.addWidget(self.data_nascimento_input)
        date_gender_layout.addLayout(date_layout)

        # Gênero
        gender_layout = QVBoxLayout()
        gender_label = QLabel("Gênero *")
        gender_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        gender_label.setStyleSheet("color: #2C3E50;")
        gender_layout.addWidget(gender_label)

        self.genero_combo = QComboBox()
        self.genero_combo.addItems(["Selecione", "Masculino", "Feminino", "Outro"])
        self.genero_combo.setStyleSheet("""
            QComboBox {
                padding: 12px;
                border: 1px solid #D0D0D0;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
            }
            QComboBox:focus {
                border: 2px solid #4A7C8C;
            }
        """)
        gender_layout.addWidget(self.genero_combo)
        date_gender_layout.addLayout(gender_layout)

        content_layout.addWidget(date_gender_container)

        content_layout.addSpacing(20)

        # Seção: Informações Escolares
        school_section = self._create_section_header("Informações Escolares", "fa5s.school")
        school_section.setMaximumWidth(800) # Limita a largura máxima da seção
        content_layout.addWidget(school_section)

        # Instituição
        inst_label = QLabel("Instituição *")
        inst_label.setMaximumWidth(800) # Limita a largura máxima do label
        inst_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        inst_label.setStyleSheet("color: #2C3E50;")
        content_layout.addWidget(inst_label)

        self.instituicao_input = QLineEdit()
        self.instituicao_input.setMaximumWidth(800) # Limita a largura máxima do input
        self.instituicao_input.setPlaceholderText("Nome da escola ou instituição")
        self.instituicao_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 1px solid #D0D0D0;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #4A7C8C;
            }
        """)
        content_layout.addWidget(self.instituicao_input)

        # Série Escolar e Turma
        serie_turma_container = QWidget()
        serie_turma_container.setMaximumWidth(800)
        serie_turma_layout = QHBoxLayout(serie_turma_container)
        serie_turma_layout.setSpacing(15)

        # Série Escolar
        serie_layout = QVBoxLayout()
        serie_label = QLabel("Série Escolar *")
        serie_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        serie_label.setStyleSheet("color: #2C3E50;")
        serie_layout.addWidget(serie_label)

        self.serie_escolar_combo = QComboBox()
        self.serie_escolar_combo.addItems(["Selecione", "1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano"])
        self.serie_escolar_combo.setStyleSheet("""
            QComboBox {
                padding: 12px;
                border: 1px solid #D0D0D0;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
            }
            QComboBox:focus {
                border: 2px solid #4A7C8C;
            }
        """)
        serie_layout.addWidget(self.serie_escolar_combo)
        serie_turma_layout.addLayout(serie_layout)

        # Turma
        turma_layout = QVBoxLayout()
        turma_label = QLabel("Turma")
        turma_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        turma_label.setStyleSheet("color: #2C3E50;")
        turma_layout.addWidget(turma_label)

        self.turma_input = QLineEdit()
        self.turma_input.setPlaceholderText("Ex: Turma A")
        self.turma_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 1px solid #D0D0D0;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #4A7C8C;
            }
        """)
        turma_layout.addWidget(self.turma_input)
        serie_turma_layout.addLayout(turma_layout)

        content_layout.addWidget(serie_turma_container)

        content_layout.addStretch()

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # Botão Continuar
        button_container = QWidget()
        button_container.setStyleSheet("background-color: white; padding: 15px;")
        button_layout = QVBoxLayout(button_container)
        button_layout.setContentsMargins(20, 10, 20, 10)

        self.continue_button = QPushButton("Continuar")
        self.continue_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.continue_button.setFixedHeight(50)
        self.continue_button.setStyleSheet("""
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
        self.continue_button.setMaximumWidth(800) # Limita a largura máxima do botão
        button_layout.addWidget(self.continue_button)
        main_layout.addWidget(button_container)

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #F5F5F5;")

    def _create_section_header(self, title, icon_name):
        section_widget = QWidget()
        section_layout = QHBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 10)
        section_widget.setMaximumWidth(800) # Limita a largura máxima da seção do cabeçalho
        section_layout.setSpacing(10)

        icon_label = QLabel()
        icon = qta.icon(icon_name, color="#4A7C8C")
        icon_label.setPixmap(icon.pixmap(20, 20))
        section_layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #4A7C8C;")
        section_layout.addWidget(title_label)
        section_layout.addStretch()

        return section_widget

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    window = TelaCadastroAluno()
    window.show()
    app.exec()

