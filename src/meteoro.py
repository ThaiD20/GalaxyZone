import pygame
import random
import os
from src.constantes import LARGURA, ALTURA, ASSETS_DIR

class Meteoro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        nome_arquivo = random.choice(["asteroid-1.png", "asteroid-2.png"])
        caminho_meteoro = os.path.join(ASSETS_DIR, nome_arquivo)

        self.image = pygame.image.load(caminho_meteoro).convert_alpha()


        if nome_arquivo == "asteroid-1.png":
            self.image = pygame.transform.scale(self.image, (60, 60))  # O maior
        else:
            self.image = pygame.transform.scale(self.image, (40, 40))  # O menor

        # quadrado de colisao
        self.rect = self.image.get_rect()

        # surgimento aleatorio
        self.rect.x = random.randint(0, LARGURA - self.rect.width)
        self.rect.y = random.randint(-150, -60)

        # Velocidade de queda
        self.velocidade_y = random.randint(3, 7)

    def update(self):

        self.rect.y += self.velocidade_y

        # tamanho surtido
        if self.rect.top > ALTURA:
            # movimentação surtida
            nome_arquivo = random.choice(["asteroid-1.png", "asteroid-2.png"])
            caminho_meteoro = os.path.join(ASSETS_DIR, nome_arquivo)
            self.image = pygame.image.load(caminho_meteoro).convert_alpha()

            if nome_arquivo == "asteroid-1.png":
                self.image = pygame.transform.scale(self.image, (60, 60))
            else:
                self.image = pygame.transform.scale(self.image, (40, 40))

            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, LARGURA - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.velocidade_y = random.randint(3, 7)