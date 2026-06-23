import pygame
import os
from src.constantes import ASSETS_DIR


class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # imagem
        caminho_tiro = os.path.join(ASSETS_DIR, "tiro.png")
        self.image = pygame.image.load(caminho_tiro).convert_alpha()

        # proporção
        self.image = pygame.transform.scale(self.image, (10, 25))

        self.rect = self.image.get_rect()

        # O tiro nasce na nave
        self.rect.centerx = x
        self.rect.bottom = y


        self.velocidade = 10

    def update(self):

        self.rect.y -= self.velocidade


        if self.rect.bottom < 0:
            self.kill()