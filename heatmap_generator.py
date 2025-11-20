import cv2
import numpy as np
import os
from datetime import datetime


class HeatmapGenerator:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.points = []

    def add_point(self, x, y):
        """Adiciona um ponto (coordenada) à lista."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.points.append((x, y))

    def generate_and_save(self, output_folder="assets/heatmaps", bg_path=None):
        """
        Gera o mapa de calor.
        Se 'bg_path' for informado, usa essa imagem como fundo.
        """

        # 1. Base preta para o heatmap (escala de cinza)
        heatmap_gray = np.zeros((self.height, self.width), dtype=np.uint8)

        # 2. Desenha círculos brancos onde o mouse passou
        for x, y in self.points:
            # Raio 30 para ficar bem visível
            cv2.circle(heatmap_gray, (x, y), 10, 255, -1)

        # 3. Suavização (Blur) forte para criar o efeito de calor
        # (101, 101) é o tamanho do borrão (deve ser ímpar)
        heatmap_blurred = cv2.GaussianBlur(heatmap_gray, (101, 101), 0)

        # 4. Coloração (JET: Azul = Frio, Vermelho = Quente)
        heatmap_color = cv2.applyColorMap(heatmap_blurred, cv2.COLORMAP_JET)

        # 5. Misturar com o fundo (O SEGREDO)
        final_image = heatmap_color

        if bg_path and os.path.exists(bg_path):
            try:
                # Carrega o print do jogo (que você tirou na tela do jogo)
                background = cv2.imread(bg_path)

                # Garante que o fundo tem o mesmo tamanho do heatmap
                background = cv2.resize(background, (self.width, self.height))

                final_image = cv2.addWeighted(background, 0.6, heatmap_color, 0.4, 0)
                print("Fundo do jogo aplicado com sucesso.")
            except Exception as e:
                print(f"Erro ao mesclar fundo: {e}")
        else:
            print("Nenhum fundo fornecido ou arquivo não encontrado. Gerando apenas o calor.")

        # 6. Salvar
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        filename = f"heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        full_path = os.path.join(output_folder, filename)

        cv2.imwrite(full_path, final_image)
        print(f"Mapa de calor salvo em: {full_path}")

        self.points = []  # Limpa para a próxima partida
        return full_path