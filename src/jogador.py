import pygame
import os
from src.constantes import LARGURA, ALTURA, ASSETS_DIR
from src.tiro import Tiro


class Jogador:
    def __init__(self):
        caminho_nave = os.path.join(ASSETS_DIR, "nave.png")
        self.imagem = pygame.image.load(caminho_nave).convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (100, 100))

        self.rect = self.imagem.get_rect()
        self.rect.centerx = LARGURA // 2
        self.rect.bottom = ALTURA - 50

        self.velocidade = 6

        # sistema de controle de tiros
        self.grupo_tiros = pygame.sprite.Group()

        # 🔊 NOVO: Carrega o efeito sonoro do tiro na memória
        caminho_som_tiro = os.path.join(ASSETS_DIR, "TiroSimples.mp3")
        self.som_tiro = pygame.mixer.Sound(caminho_som_tiro)
        self.som_tiro.set_volume(0.3)  # Volume equilibrado para não estourar o ouvido

    def controlar(self):
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidade
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.rect.y += self.velocidade

        # BARREIRAS
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > LARGURA: self.rect.right = LARGURA
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > ALTURA: self.rect.bottom = ALTURA

    def atirar(self):
        """Cria um novo tiro e toca o efeito sonoro"""
        novo_tiro = Tiro(self.rect.centerx, self.rect.top)
        self.grupo_tiros.add(novo_tiro)

        # 🔊 NOVO: Toca o som do laser toda vez que essa função for chamada!
        self.som_tiro.play()

    def desenhar(self, tela):
        self.grupo_tiros.draw(tela)
        tela.blit(self.imagem, self.rect)