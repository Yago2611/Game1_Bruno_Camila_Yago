import pygame as pg
import sys
from configuracoes import Configuracoes

class Cena_final:
  def __init__(self,cena_principal):
    self.jogador1 = cena_principal.jogador1
    self.jogador2 = cena_principal.jogador2
    self.tela = cena_principal.tela
    self.encerrada = False
    self.titulo = pg.font.SysFont(None,Configuracoes.FONTE_TITULO)
    self.subtitulo = pg.font.SysFont(None,Configuracoes.FONTE_MENOR)
    self.Titulo = self.titulo.render(f'Guerra de Cientistas',True,(0,0,0))
    if self.jogador1.vida_atual>0 and self.jogador2.vida_atual>0:
      self.Subtitulo = self.subtitulo.render(f'Empate Técnico',True,(0,0,0))
    elif self.jogador1.vida_atual <= 0 and self.jogador2.vida_atual <= 0:
      self.Subtitulo = self.subtitulo.render(f'Vitória dos Minions',True,(0,0,0))
    elif self.jogador2.vida_atual<=0:
      self.Subtitulo = self.subtitulo.render(f'O Melhor Cientista da Historia: {self.jogador1.nome} [Jogador 1]', True, (0,0,0))
    else:
      self.Subtitulo = self.subtitulo.render(f'O Melhor Cientista da Historia: {self.jogador2.nome} [Jogador 2]', True, (0,0,0))
    self.tela.fill((255, 255, 255))
    self.PX = Configuracoes.LARGURA_TELA // 2 - self.Titulo.get_size()[0] // 2
    self.PY = Configuracoes.ALTURA_TELA //2 - self.Titulo.get_size()[1]
    self.px = Configuracoes.LARGURA_TELA // 2 - self.Subtitulo.get_size()[0] // 2
    self.py = (self.PY) + (self.Subtitulo.get_size()[1] * 3)
  def rodar(self):
    while not self.encerrada:
      self.tratamento_de_eventos()
      self.atualiza_estado()
      self.desenha()
  def tratamento_de_eventos(self):
    for event in pg.event.get():
        if event.type == (pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or (pg.key.get_pressed()[pg.K_ESCAPE]): 
            print("Encerrando o programa.")
            sys.exit()
  def atualiza_estado(self):
    pass
  def desenha(self):
        self.tela.fill((255, 255, 255))
        self.tela.blit(self.Titulo, (self.PX,self.PY))
        self.tela.blit(self.Subtitulo, (self.px, self.py))
        pg.display.flip()
