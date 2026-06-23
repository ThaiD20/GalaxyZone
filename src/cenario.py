import pygame
import os
from src.constantes import LARGURA, ALTURA, ASSETS_DIR


class CamadaParallax:
    def __init__(self, nome_arquivo, velocidade):
        self.velocidade = velocidade


        caminho_imagem = os.path.join(ASSETS_DIR, nome_arquivo)

        # Carrega a imagem e força ela a caber na largura e altura da tela
        self.imagem = pygame.image.load(caminho_imagem).convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (LARGURA, ALTURA))


        self.y1 = 0
        self.y2 = -ALTURA

    def atualizar(self):

        self.y1 += self.velocidade
        self.y2 += self.velocidade

        # loop de imagem
        if self.y1 >= ALTURA:
            self.y1 = -ALTURA + (self.y1 - ALTURA)


        if self.y2 >= ALTURA:
            self.y2 = -ALTURA + (self.y2 - ALTURA)

    def desenhar(self, tela):
        # desenhando a imagem
        tela.blit(self.imagem, (0, self.y1))
        tela.blit(self.imagem, (0, self.y2))


class FundoParallax:
    def __init__(self):

        self.camadas = [
            CamadaParallax("BG.png", 0.5),  # O fundo lento
            CamadaParallax("blue-stars.png", 1.5)  # estrelas rapidas
        ]

    def atualizar(self):
        # Atualiza o movimento
        for camada in self.camadas:
            camada.atualizar()

    def desenhar(self, tela):
        # ordem de "desenho" de camadas
        for camada in self.camadas:
            camada.desenhar(tela)