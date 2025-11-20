from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QFrame,
    QSizePolicy, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import qtawesome as qta

from database import DatabaseManager


class TelaLoginAluno(QWidget):
    # Sinais
    login_realizado = pyqtSignal(int)  # Envia o ID do aluno escolhido
    ir_para_cadastro = pyqtSignal()  # Sinal para ir para a tela de cadastro se não tiver conta
    back_to_inicial = pyqtSignal()  # Botão de voltar

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.carregar_alunos()  # Carrega a lista ao iniciar

    def carregar_alunos(self):
        """Busca os alunos no banco e preenche o ComboBox"""
        self.aluno_combo.clear()
        self.aluno_combo.addItem("Selecione seu nome...", None)  # Item padrão

        db = DatabaseManager()
        query = "SELECT id, nomeCompleto FROM Alunos ORDER BY nomeCompleto ASC"

        try:
            alunos = db.fetch_all(query)
            for aluno in alunos:
                # Adiciona o Nome visível e o ID oculto (userData)
                self.aluno_combo.addItem(aluno['nomeCompleto'], aluno['id'])
        except Exception as e:
            print(f"Erro ao carregar alunos: {e}")

    def confirmar_login(self):
        # Pega o ID armazenado no item selecionado (userData)
        aluno_id = self.aluno_combo.currentData()
        print(f"--- DEBUG TELA LOGIN: Botão clicado! ID selecionado: {aluno_id} ---")
        if aluno_id:
            print(f"Login confirmado para ID: {aluno_id}")
            self.login_realizado.emit(aluno_id)
        else:
            QMessageBox.warning(self, "Atenção", "Por favor, selecione um aluno na lista.")

    def showEvent(self, event):
        """Recarrega a lista toda vez que a tela é exibida (caso alguém novo tenha se cadastrado)"""
        self.carregar_alunos()
        super().showEvent(event)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        main_layout.setSpacing(10)
        main_layout.addStretch()
        # --- Cabeçalho com botão voltar ---
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        self.back_button = QPushButton()
        self.back_button.setIcon(qta.icon("fa5s.arrow-left", color="#4A7C8C"))
        self.back_button.setStyleSheet("background: transparent; border: none;")
        self.back_button.setFixedSize(40, 40)
        header_layout.addWidget(self.back_button)
        header_layout.addStretch()

        container = QWidget()
        container.setMaximumWidth(500)
        container.setFixedHeight(50)
        container.setLayout(header_layout)
        main_layout.addWidget(container)

        # --- Card de Login ---
        card = QFrame()
        card.setMaximumWidth(500)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                padding: 30px;
                border: 1px solid #E0E0E0;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(20)

        title = QLabel("Quem é você?")
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #2C3E50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)

        # Lista de Alunos
        self.aluno_combo = QComboBox()
        self.aluno_combo.setFixedHeight(50)
        self.aluno_combo.setFont(QFont("Arial", 14))
        self.aluno_combo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                background-color: #F9F9F9;
            }
            QComboBox::drop-down { border: none; }
        """)
        card_layout.addWidget(self.aluno_combo)

        # Botão Entrar
        self.btn_entrar = QPushButton("Entrar")
        self.btn_entrar.setFixedHeight(50)
        self.btn_entrar.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.btn_entrar.setStyleSheet("""
            QPushButton {
                background-color: #4A7C8C;
                color: white;
                border-radius: 25px;
            }
            QPushButton:hover { background-color: #3A6C7C; }
        """)
        self.btn_entrar.clicked.connect(self.confirmar_login)
        card_layout.addWidget(self.btn_entrar)

        # Botão Criar Nova Conta
        self.btn_novo = QPushButton("Não estou na lista (Criar Cadastro)")
        self.btn_novo.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #7F8C8D;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover { color: #4A7C8C; text-decoration: underline; }
        """)
        self.btn_novo.clicked.connect(self.ir_para_cadastro.emit)
        card_layout.addWidget(self.btn_novo)

        main_layout.addWidget(card)
        main_layout.addStretch()
        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #F5F5F5;")

        self.back_button.clicked.connect(self.back_to_inicial.emit)


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    app = QApplication([])
    w = TelaLoginAluno()
    w.show()
    app.exec()