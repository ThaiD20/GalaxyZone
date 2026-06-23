import pygame
import sys
from src.constantes import LARGURA, ALTURA, FPS, PRETO
from src.gerenciador import GerenciadorJogo

def main():

    pygame.init()

    # janela
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("GalaxyZone")

    relogio = pygame.time.Clock()

    jogo = GerenciadorJogo(tela)

    while jogo.rodando:
        relogio.tick(FPS)

        jogo.processar_eventos()
        jogo.atualizar()
        jogo.desenhar()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

    #pojeto finalizado :D