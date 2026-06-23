import pygame
import os

# tela
LARGURA = 450
ALTURA = 800
FPS = 60

# cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)

#fonte size
TAMANHO_FONTE_TITULO = 50
TAMANHO_FONTE_TEXTO = 24

# menu
TITULO_JOGO = "GALAXY ZONE"
TEXTO_START = "START"
TEXTO_COMANDOS = "Setas: Mover  |  Espaço: Atirar"

#(Y)
Y_TITULO = 150
Y_START = ALTURA // 2
Y_COMANDOS = ALTURA - 100

# Pesquisas feitas apontaram para esse "metodo" de procurar arquivo no computador para rodar o jogo em qualquer maquina
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")