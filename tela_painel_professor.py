from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QSizePolicy, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import qtawesome as qta

from teacher_dashboard_logic import TeacherDashboardLogic


class TelaPainelProfessor(QWidget):
    go_to_aluno_detalhes = pyqtSignal(int)  # Agora envia o ID (int)
    logout_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic = TeacherDashboardLogic()
        self.setup_ui()
        # Carrega os alunos ao iniciar
        self.refresh_ui()

    def showEvent(self, event):
        """Recarrega a lista sempre que a tela for exibida"""
        self.refresh_ui()
        super().showEvent(event)

    def refresh_ui(self):
        """Busca alunos no banco e recria a lista na tela"""
        # 1. Limpar a lista atual
        while self.students_layout.count():
            item = self.students_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 2. Buscar novos dados
        students = self.logic.get_students()

        if not students:
            lbl = QLabel("Nenhum aluno cadastrado.")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.students_layout.addWidget(lbl)
            return

        # 3. Criar um card para cada aluno
        for student in students:
            card = self._create_student_card(student)
            self.students_layout.addWidget(card)

        self.students_layout.addStretch()

    def _create_student_card(self, student):
        card = QFrame()
        card.setStyleSheet("background-color: white; border-radius: 10px; padding: 10px; border: 1px solid #E0E0E0;")
        card.setMaximumWidth(800)

        layout = QHBoxLayout(card)

        # Ícone
        icon_label = QLabel()
        icon = qta.icon("fa5s.user-graduate", color="#4A7C8C")
        icon_label.setPixmap(icon.pixmap(40, 40))
        layout.addWidget(icon_label)

        # Textos (Nome e Turma)
        text_layout = QVBoxLayout()
        name_label = QLabel(student['nome'])
        name_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #2C3E50;")

        info_label = QLabel(f"{student['turma']} | {student['idade']} anos")
        info_label.setStyleSheet("color: #7F8C8D;")

        text_layout.addWidget(name_label)
        text_layout.addWidget(info_label)
        layout.addLayout(text_layout)

        layout.addStretch()

        # Botão Visualizar
        btn_view = QPushButton("Ver")
        btn_view.setStyleSheet("""
            QPushButton { background-color: #4A7C8C; color: white; border-radius: 5px; padding: 5px 15px; }
            QPushButton:hover { background-color: #3A6C7C; }
        """)
        btn_view.clicked.connect(lambda checked, pid=student['id']: self.go_to_aluno_detalhes.emit(pid))
        layout.addWidget(btn_view)

        # Botão Excluir
        btn_delete = QPushButton()
        btn_delete.setIcon(qta.icon("fa5s.trash", color="white"))
        btn_delete.setStyleSheet("""
            QPushButton { background-color: #FF5252; border-radius: 5px; padding: 5px; }
            QPushButton:hover { background-color: #FF1744; }
        """)
        btn_delete.setFixedSize(30, 30)
        btn_delete.clicked.connect(
            lambda checked, pid=student['id'], name=student['nome']: self.confirmar_exclusao(pid, name))
        layout.addWidget(btn_delete)

        return card

    def confirmar_exclusao(self, student_id, nome):
        reply = QMessageBox.question(
            self, 'Confirmar Exclusão',
            f"Tem certeza que deseja excluir o aluno {nome}?\nTodos os dados e sessões serão perdidos.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.logic.delete_student(student_id):
                self.refresh_ui()  # Recarrega a lista
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível excluir o aluno.")

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
        self.back_button.clicked.connect(self.logout_requested.emit)
        header_layout.addWidget(self.back_button)

        title = QLabel("Meus Alunos")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        main_layout.addWidget(header)

        # Área de Conteúdo (Lista)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: #F5F5F5;")

        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #F5F5F5;")
        self.students_layout = QVBoxLayout(content_widget)
        self.students_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.students_layout.setSpacing(10)
        self.students_layout.setContentsMargins(20, 20, 20, 20)

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)