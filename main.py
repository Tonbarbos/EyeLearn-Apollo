import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QGraphicsOpacityEffect, QPushButton
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint

from tela_inicial import TelaInicial
from tela_cadastro_aluno import TelaCadastroAluno
from tela_principal_aluno import TelaPrincipalAluno
from tela_calibracao_eye_tracking import TelaCalibracaoEyeTracking
from tela_jogo_memoria import TelaJogoMemoria
from tela_configuracoes import TelaConfiguracoes
from tela_eye_tracker_master import TelaEyeTrackerMaster
from tela_parabens import TelaParabens
from tela_painel_professor import TelaPainelProfessor
from tela_detalhes_aluno import TelaDetalhesAluno
from tela_fim_sessao import TelaFimSessao # Nova importação

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EyeLearn")
        self.setGeometry(100, 100, 480, 800) # Tamanho inicial simulando um celular

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        # Telas da aplicação
        self.tela_inicial = TelaInicial()
        self.tela_cadastro_aluno = TelaCadastroAluno()
        self.tela_principal_aluno = TelaPrincipalAluno()
        self.tela_calibracao_eye_tracking = TelaCalibracaoEyeTracking()
        self.tela_jogo_memoria = TelaJogoMemoria()
        self.tela_configuracoes = TelaConfiguracoes()
        self.tela_rastreamento_ocular = TelaEyeTrackerMaster()
        self.tela_parabens = TelaParabens() # Instancia a tela de parabéns
        self.tela_painel_professor = TelaPainelProfessor() # Instancia a tela do painel do professor
        self.tela_detalhes_aluno = TelaDetalhesAluno() # Instancia a tela de detalhes do aluno
        self.tela_fim_sessao = TelaFimSessao() # Nova instância

        self.stacked_widget.addWidget(self.tela_inicial)
        self.stacked_widget.addWidget(self.tela_cadastro_aluno)
        self.stacked_widget.addWidget(self.tela_principal_aluno)
        self.stacked_widget.addWidget(self.tela_calibracao_eye_tracking)
        self.stacked_widget.addWidget(self.tela_jogo_memoria)
        self.stacked_widget.addWidget(self.tela_configuracoes)
        self.stacked_widget.addWidget(self.tela_rastreamento_ocular)
        self.stacked_widget.addWidget(self.tela_parabens)
        self.stacked_widget.addWidget(self.tela_painel_professor)
        self.stacked_widget.addWidget(self.tela_detalhes_aluno)
        self.stacked_widget.addWidget(self.tela_fim_sessao) # Adiciona a nova tela

        # Definir a tela inicial
        self.stacked_widget.setCurrentWidget(self.tela_inicial)

    def setup_connections(self):
        # Transições da Tela Inicial
        self.tela_inicial.aluno_button.clicked.connect(lambda: self.fade_transition(self.tela_cadastro_aluno))
        self.tela_inicial.professor_button.clicked.connect(lambda: self.fade_transition(self.tela_painel_professor))

        # Transições da Tela de Cadastro de Aluno
        self.tela_cadastro_aluno.back_button.clicked.connect(lambda: self.fade_transition(self.tela_inicial))
        self.tela_cadastro_aluno.continue_button.clicked.connect(lambda: self.fade_transition(self.tela_principal_aluno))

        # Conexões da TelaPrincipalAluno
        self.tela_principal_aluno.jogo_memoria_button.clicked.connect(lambda: self.fade_transition(self.tela_jogo_memoria))
        self.tela_principal_aluno.nav_configuracoes_button.clicked.connect(lambda: self.fade_transition(self.tela_configuracoes))
        self.tela_principal_aluno.nav_logout_button.clicked.connect(lambda: self.fade_transition(self.tela_inicial)) # Conexão do botão de logout

        # Transições do Jogo da Memória
        self.tela_jogo_memoria.back_button.clicked.connect(lambda: self.fade_transition(self.tela_principal_aluno))
        self.tela_jogo_memoria.game_finished.connect(self.show_parabens)

        # Transições da Tela de Calibração de Eye Tracking
        self.tela_calibracao_eye_tracking.back_button.clicked.connect(lambda: self.fade_transition(self.tela_principal_aluno))

        # Transições da Tela de Configurações
        self.tela_configuracoes.back_button.clicked.connect(lambda: self.fade_transition(self.tela_principal_aluno))
        self.tela_configuracoes.eye_tracker_button_clicked.connect(lambda: self.fade_transition(self.tela_rastreamento_ocular))

        # Transições da Tela Rastreamento Ocular
        self.tela_rastreamento_ocular.back_to_configuracoes.connect(lambda: self.fade_transition(self.tela_configuracoes))

        # Transições da Tela de Parabéns
        self.tela_parabens.go_to_principal_aluno.connect(lambda: self.fade_transition(self.tela_principal_aluno))
        self.tela_parabens.logout_requested.connect(lambda: self.fade_transition(self.tela_inicial))

        # Transições do Painel do Professor
        self.tela_painel_professor.go_to_aluno_detalhes.connect(self.show_detalhes_aluno)
        self.tela_painel_professor.logout_requested.connect(lambda: self.fade_transition(self.tela_inicial))

        # Transições da Tela de Detalhes do Aluno
        self.tela_detalhes_aluno.go_to_painel_professor.connect(lambda: self.fade_transition(self.tela_painel_professor))
        self.tela_detalhes_aluno.logout_requested.connect(lambda: self.fade_transition(self.tela_inicial))

        # Transições da Tela de Fim de Sessão
        self.tela_fim_sessao.go_to_nova_sessao_aluno.connect(lambda: self.fade_transition(self.tela_principal_aluno))
        self.tela_fim_sessao.go_to_professor_login.connect(lambda: self.fade_transition(self.tela_painel_professor))

    def show_parabens(self, score, time_elapsed, errors):
        # Remover a tela antiga de parabéns se existir e adicionar a nova
        if self.stacked_widget.indexOf(self.tela_parabens) != -1:
            self.stacked_widget.removeWidget(self.tela_parabens)
        self.tela_parabens = TelaParabens(score=score, time_elapsed=time_elapsed, errors=errors)
        self.stacked_widget.addWidget(self.tela_parabens)
        # Após a tela de parabéns, o fluxo deve ir para a tela de fim de sessão
        self.tela_parabens.go_to_principal_aluno.connect(lambda: self.fade_transition(self.tela_fim_sessao)) # Alterado para ir para TelaFimSessao
        self.tela_parabens.logout_requested.connect(lambda: self.fade_transition(self.tela_inicial))
        self.fade_transition(self.tela_parabens)

    def show_detalhes_aluno(self, aluno_nome):
        # Remover a tela antiga de detalhes do aluno se existir e adicionar a nova
        if self.stacked_widget.indexOf(self.tela_detalhes_aluno) != -1:
            self.stacked_widget.removeWidget(self.tela_detalhes_aluno)
        self.tela_detalhes_aluno = TelaDetalhesAluno(aluno_nome=aluno_nome)
        self.stacked_widget.addWidget(self.tela_detalhes_aluno)
        self.tela_detalhes_aluno.go_to_painel_professor.connect(lambda: self.fade_transition(self.tela_painel_professor))
        self.tela_detalhes_aluno.logout_requested.connect(lambda: self.fade_transition(self.tela_inicial))
        self.fade_transition(self.tela_detalhes_aluno)

    def fade_transition(self, next_widget):
        current_widget = self.stacked_widget.currentWidget()

        self.fade_out_effect = QGraphicsOpacityEffect(current_widget)
        current_widget.setGraphicsEffect(self.fade_out_effect)
        self.fade_out_animation = QPropertyAnimation(self.fade_out_effect, b"opacity")
        self.fade_out_animation.setDuration(200)
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.fade_out_animation.finished.connect(lambda: self._start_fade_in(next_widget, current_widget))
        self.fade_out_animation.start()

    def _start_fade_in(self, next_widget, old_widget):
        self.stacked_widget.setCurrentWidget(next_widget)
        old_widget.setGraphicsEffect(None)

        self.fade_in_effect = QGraphicsOpacityEffect(next_widget)
        next_widget.setGraphicsEffect(self.fade_in_effect)
        self.fade_in_animation = QPropertyAnimation(self.fade_in_effect, b"opacity")
        self.fade_in_animation.setDuration(200)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Type.InCubic)
        self.fade_in_animation.finished.connect(lambda: next_widget.setGraphicsEffect(None))
        self.fade_in_animation.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
