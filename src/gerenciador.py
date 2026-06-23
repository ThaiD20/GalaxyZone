import pygame
import sys
import os
import random
from src.constantes import (
    LARGURA, ALTURA, PRETO, BRANCO, AMARELO, ASSETS_DIR,
    TITULO_JOGO, TEXTO_START, TEXTO_COMANDOS, Y_TITULO, Y_START, Y_COMANDOS,
    TAMANHO_FONTE_TITULO, TAMANHO_FONTE_TEXTO
)
from src.cenario import FundoParallax
from src.jogador import Jogador
from src.meteoro import Meteoro


class GerenciadorJogo:
    def __init__(self, tela):
        self.tela = tela
        self.estado = "MENU"
        self.rodando = True

        self.carregar_assets_menu()
        self.tocar_musica_menu()

        # fonte
        self.fonte_placar = pygame.font.Font(None, TAMANHO_FONTE_TEXTO)
        self.fonte_game_over = pygame.font.Font(None, TAMANHO_FONTE_TITULO)

        # Inicializa
        self.reiniciar_jogo()

    def reiniciar_jogo(self):
        self.cenario_fase1 = FundoParallax()
        self.jogador = Jogador()
        self.pontuacao = 0
        self.vidas = 5  # VIDA DA NAVE

        # controle de records
        self.mostrar_recorde = False
        self.timer_recorde = 0

        # criando meteoro
        self.grupo_meteoros = pygame.sprite.Group()
        for i in range(8):
            self.grupo_meteoros.add(Meteoro())

    def carregar_assets_menu(self):
        caminho_fundo = os.path.join(ASSETS_DIR, "FundoMenu.png")
        self.fundo_menu = pygame.image.load(caminho_fundo).convert_alpha()
        self.fundo_menu = pygame.transform.scale(self.fundo_menu, (LARGURA, ALTURA))

        self.fonte_titulo = pygame.font.Font(None, TAMANHO_FONTE_TITULO)
        self.fonte_instrucoes = pygame.font.Font(None, TAMANHO_FONTE_TEXTO)

    def tocar_musica_menu(self):
        caminho_musica = os.path.join(ASSETS_DIR, "MenuSong.ogg")
        pygame.mixer.music.load(caminho_musica)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def iniciar_fase_1(self):
        self.estado = "JOGANDO"
        caminho_musica_fase = os.path.join(ASSETS_DIR, "Fase1.ogg")
        pygame.mixer.music.load(caminho_musica_fase)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False

            if self.estado == "MENU":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        self.iniciar_fase_1()

            elif self.estado == "JOGANDO":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        self.jogador.atirar()

            # Enter apos game over
            elif self.estado == "GAME_OVER":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        self.reiniciar_jogo()
                        self.iniciar_fase_1()


            elif self.estado == "VITORIA":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        self.reiniciar_jogo()
                        self.estado = "MENU"
                        self.tocar_musica_menu()

    def checar_colisoes(self):
        # Colisão de tiros com meteoros
        colisoes_tiro = pygame.sprite.groupcollide(self.jogador.grupo_tiros, self.grupo_meteoros, True, True)
        for colisao in colisoes_tiro:
            self.pontuacao += 1


            if self.pontuacao >= 50:
                self.estado = "VITORIA"
                return  # Para a execução do método aqui para evitar bugs

            self.grupo_meteoros.add(Meteoro())

            if self.pontuacao > 0 and self.pontuacao % 10 == 0:
                self.mostrar_recorde = True
                self.timer_recorde = 90

        # Colisão da nave com meteoros
        colisoes_nave = pygame.sprite.spritecollide(self.jogador, self.grupo_meteoros, True)
        for colisao in colisoes_nave:
            self.vidas -= 1

            #  GAME OVER
            if self.vidas <= 0:
                self.estado = "GAME_OVER"
                return

            self.grupo_meteoros.add(Meteoro())  # retorno do meteoro

    def atualizar(self):
        if self.estado == "MENU":
            pass
        elif self.estado == "JOGANDO":
            self.cenario_fase1.atualizar()
            self.jogador.controlar()
            self.jogador.grupo_tiros.update()
            self.grupo_meteoros.update()
            self.checar_colisoes()

            # tempo de exibicao do record
            if self.mostrar_recorde:
                self.timer_recorde -= 1
                if self.timer_recorde <= 0:
                    self.mostrar_recorde = False

    def desenhar(self):

        if self.estado == "MENU":
            self.tela.blit(self.fundo_menu, (0, 0))

            texto_titulo = self.fonte_titulo.render(TITULO_JOGO, True, AMARELO)
            texto_start = self.fonte_instrucoes.render(TEXTO_START, True, BRANCO)
            texto_comandos = self.fonte_instrucoes.render(TEXTO_COMANDOS, True, BRANCO)

            self.tela.blit(texto_titulo, (LARGURA // 2 - texto_titulo.get_width() // 2, Y_TITULO))
            self.tela.blit(texto_start, (LARGURA // 2 - texto_start.get_width() // 2, Y_START))
            self.tela.blit(texto_comandos, (LARGURA // 2 - texto_comandos.get_width() // 2, Y_COMANDOS))

        elif self.estado == "JOGANDO":
            self.tela.fill((0, 0, 0))
            self.cenario_fase1.desenhar(self.tela)
            self.grupo_meteoros.draw(self.tela)
            self.jogador.desenhar(self.tela)

            texto_placar = self.fonte_placar.render(f"PONTOS: {self.pontuacao}", True, BRANCO)
            texto_vidas = self.fonte_placar.render(f"VIDAS: {self.vidas}", True, (255, 100, 100))
            self.tela.blit(texto_placar, (20, 20))
            self.tela.blit(texto_vidas, (20, 50))

            # record
            if self.mostrar_recorde:
                texto_rec = self.fonte_placar.render("¡NOVO RECORDE!", True, AMARELO)
                self.tela.blit(texto_rec, (LARGURA // 2 - texto_rec.get_width() // 2, 20))

        elif self.estado == "GAME_OVER":
            self.tela.fill((0, 0, 0))  # tela game over

            texto_go = self.fonte_game_over.render("GAME OVER", True, (255, 0, 0))
            texto_retry = self.fonte_placar.render("Pressione ENTER para Recomeçar", True, BRANCO)
            texto_pontos_finais = self.fonte_placar.render(f"Pontuação Final: {self.pontuacao}", True, AMARELO)

            self.tela.blit(texto_go, (LARGURA // 2 - texto_go.get_width() // 2, ALTURA // 2 - 80))
            self.tela.blit(texto_pontos_finais, (LARGURA // 2 - texto_pontos_finais.get_width() // 2, ALTURA // 2))
            self.tela.blit(texto_retry, (LARGURA // 2 - texto_retry.get_width() // 2, ALTURA // 2 + 60))

        # === SEU NOVO ESTADO DE VITÓRIA AQUI ===
        elif self.estado == "VITORIA":
            self.tela.fill((0, 0, 0))  # Tela preta igual você pediu

            # Textos da tela de vitória
            texto_vit = self.fonte_game_over.render("VITÓRIA!", True, AMARELO)
            texto_voltar = self.fonte_placar.render("Pressione ENTER para Voltar ao Menu", True, BRANCO)

            # Centralizando os textos na tela
            self.tela.blit(texto_vit, (LARGURA // 2 - texto_vit.get_width() // 2, ALTURA // 2 - 40))
            self.tela.blit(texto_voltar, (LARGURA // 2 - texto_voltar.get_width() // 2, ALTURA // 2 + 40))