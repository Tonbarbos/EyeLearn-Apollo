import numpy
import cv2
import sys
import os
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QFrame, QMainWindow
from PyQt6.uic import loadUi

# Adicionar o diretório 'project' ao PYTHONPATH para que as importações funcionem
sys.path.append(os.path.join(os.path.dirname(__file__), 'project'))

from project.capturers.haar_blob import HaarCascadeBlobCapture
from project.frame_sources import CameraFrameSource
from project.settings import settings

class EyeTrackerWidget(QMainWindow):
    frame_processed = pyqtSignal(QPixmap, QPixmap, QPixmap)

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.ui_loaded = False
        # Definir caminhos para os arquivos UI e CSS do Eye-Tracker-master
        ui_file_path = os.path.join(os.path.dirname(__file__), 'project', 'gui', 'assets', 'GUImain.ui')
        style_file_path = os.path.join(os.path.dirname(__file__), 'project', 'gui', 'assets', 'style.css')

        try:
            loadUi(ui_file_path, self)
            with open(style_file_path, "r") as css:
                self.setStyleSheet(css.read())
            self.ui_loaded = True
        except Exception as e:
            print(f"Erro ao carregar UI ou CSS do Eye Tracker Master: {e}")
            # Criar uma UI de fallback simples
            fallback_widget = QWidget()
            layout = QVBoxLayout(fallback_widget)
            label = QLabel("Erro ao carregar Eye Tracker UI. Verifique os arquivos.")
            layout.addWidget(label)
            self.setCentralWidget(fallback_widget)
            
            # Inicializar atributos para evitar AttributeError
            self.startButton = QPushButton("Iniciar (Fallback)")
            self.stopButton = QPushButton("Parar (Fallback)")
            self.leftEyeThreshold = QSlider(Qt.Orientation.Horizontal)
            self.rightEyeThreshold = QSlider(Qt.Orientation.Horizontal)
            self.baseImage = QLabel("Base Image (Fallback)")
            self.leftEyeBox = QLabel("Left Eye (Fallback)")
            self.rightEyeBox = QLabel("Right Eye (Fallback)")
            
            layout.addWidget(self.startButton)
            layout.addWidget(self.stopButton)
            layout.addWidget(self.leftEyeThreshold)
            layout.addWidget(self.rightEyeThreshold)
            layout.addWidget(self.baseImage)
            layout.addWidget(self.leftEyeBox)
            layout.addWidget(self.rightEyeBox)

        self.video_source = CameraFrameSource()
        self.capture = HaarCascadeBlobCapture()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Conectar os botões e sliders da UI carregada (ou fallback)
        self.startButton.clicked.connect(self.start_eye_tracker)
        self.stopButton.clicked.connect(self.stop_eye_tracker)
        
        # Inicialmente, o botão de parar deve estar desabilitado
        self.stopButton.setEnabled(False)

    def start_eye_tracker(self):
        try:
            # A propriedade 'cap' pode não existir se a UI não foi carregada corretamente
            if hasattr(self.video_source, 'cap') and not self.video_source.cap.isOpened():
                print("Câmera não disponível. Verifique a conexão.")
                return
            self.video_source.start()
            self.timer.start(settings.REFRESH_PERIOD) # Usar o REFRESH_PERIOD do Eye-Tracker-master
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)
        except SystemError as e:
            print(f"Erro ao iniciar a câmera: {e}")
            self.baseImage.setText(f"Erro: {e}")
            self.startButton.setEnabled(True)
            self.stopButton.setEnabled(False)

    def stop_eye_tracker(self):
        self.timer.stop()
        self.video_source.stop()
        # Limpar os labels de imagem
        self.baseImage.clear()
        self.leftEyeBox.clear()
        self.rightEyeBox.clear()
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)

    def update_frame(self):
        try:
            frame = self.video_source.next_frame()
            if frame is not None:
                # Acessar os valores dos sliders apenas se a UI foi carregada
                l_threshold = self.leftEyeThreshold.value() if self.ui_loaded else 0
                r_threshold = self.rightEyeThreshold.value() if self.ui_loaded else 0

                face, l_eye, r_eye = self.capture.process(frame, l_threshold, r_threshold)
                
                if face is not None:
                    self.display_image(self.opencv_to_qt(face), window="baseImage")

                if l_eye is not None:
                    self.display_image(self.opencv_to_qt(l_eye), window="leftEyeBox")

                if r_eye is not None:
                    self.display_image(self.opencv_to_qt(r_eye), window="rightEyeBox")
            else:
                self.baseImage.setText("Câmera não disponível")
        except Exception as e:
            print(f"Erro durante o processamento do frame: {e}")
            self.baseImage.setText(f"Erro de processamento: {e}")
            self.stop_eye_tracker()

    @staticmethod
    def opencv_to_qt(img) -> QImage:
        """
        Convert OpenCV image to PyQT image
        by changing format to RGB/RGBA from BGR
        """
        qformat = QImage.Format.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:  # RGBA
                qformat = QImage.Format.Format_RGBA8888
            else:  # RGB
                qformat = QImage.Format.Format_RGB888

        img = numpy.require(img, numpy.uint8, "C")
        out_image = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)  # BGR to RGB
        out_image = out_image.rgbSwapped()

        return out_image

    def display_image(self, img: QImage, window="baseImage"):
        """
        Display the image on a window - which is a label specified in the GUI .ui file
        """
        if not self.ui_loaded:
            # Se a UI não foi carregada, apenas imprime para o console ou log
            print(f"Tentativa de exibir imagem em {window}, mas UI não carregada.")
            return

        display_label: QLabel = getattr(self, window, None)
        if display_label is None:
            raise ValueError(f"No such display window in GUI: {window}")

        display_label.setPixmap(QPixmap.fromImage(img))
        display_label.setScaledContents(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EyeTrackerWidget()
    window.show()
    sys.exit(app.exec())
