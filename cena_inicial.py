import pygame as pg
import sys
from configuracoes import Configuracoes
from personagens_criados import Personagens_criados
from copy import copy
from jogador import Jogador 

class Cena_inicial:
  def __init__(self):
    self.tela = Configuracoes.TELA
    self.escolha_jogador1 = False
    self.escolha_jogador2 = False 
    self.posicao = 0 
    self.jogador1 = 0
    self.jogador2 = 0 
    self.titulo = pg.font.SysFont(None,Configuracoes.FONTE_TITULO)
    self.escolha = pg.font.SysFont(None, Configuracoes.FONTE_MENOR)
    self.personagens = pg.font.SysFont(None, Configuracoes.FONTE_MENOR)
    self.Titulo = self.titulo.render(f'Guerra de Cientistas',True,(0,0,0))
    self.Escolha = self.escolha.render(f'Escolha um personagem:', True, (0,0,0))
    self.lista_personagens = Personagens_criados.lista 
    self.lista_escolha = []
    self.encerrada = False
    for i in range(len(self.lista_personagens)):
      personagemi = self.personagens.render(f'{i+1}) {self.lista_personagens[i].nome}',True,(0,0,0))
      self.lista_escolha.append(personagemi)
    self.PX = Configuracoes.LARGURA_TELA // 2 - self.Titulo.get_size()[0] // 2
    self.PY = 0.01 * Configuracoes.ALTURA_TELA
    self.px = Configuracoes.LARGURA_TELA // 2 - self.Escolha.get_size()[0] // 2
    self.py = (0.2 * Configuracoes.ALTURA_TELA // 2) + (self.Escolha.get_size()[1] * 1.5)
    self.px_personagens = 0.05*Configuracoes.LARGURA_TELA 
    self.py_personagens = []
    for i in range(len(self.lista_escolha)):
      pyi = Configuracoes.ALTURA_TELA*(0.3 + 0.1*i) +  (self.lista_escolha[0].get_size()[1]*1.5)
      self.py_personagens.append(pyi)
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
        if (event.type == pg.KEYDOWN and event.key == pg.K_DOWN):
         if self.posicao>=0 and self.posicao<3:
            self.posicao+=1
        elif (event.type == pg.KEYDOWN and event.key == pg.K_UP):
          if self.posicao>0 and self.posicao<=3:
            self.posicao-=1
        if self.escolha_jogador1 == False and event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            self.jogador1 = Jogador(Configuracoes.P1X,Configuracoes.P1Y,(self.lista_personagens)[self.posicao])
            self.escolha_jogador1 = True        
        elif self.escolha_jogador1 and event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            self.jogador2 = Jogador(Configuracoes.P2X,Configuracoes.P2Y,(self.lista_personagens)[self.posicao])
            self.escolha_jogador2 = True        
  def atualiza_estado(self):
      if self.escolha_jogador1 and self.escolha_jogador2:
        self.encerrada = True
  def desenha(self):
    self.tela.fill((255, 255, 255))
    self.tela.blit(self.Titulo, (self.PX,self.PY))
    self.tela.blit(self.Escolha, (self.px, self.py))
    for i in range(len(self.lista_escolha)):
      self.tela.blit(self.lista_escolha[i],(self.px_personagens,self.py_personagens[i]))
    for i in range(len(self.lista_escolha)):
      if self.posicao == i and not self.escolha_jogador1:
        escolha_jogador = self.personagens.render(f' [Jogador 1]',True,(122,122,0))
        self.tela.blit(escolha_jogador,(self.px_personagens+self.lista_escolha[i].get_rect().width,self.py_personagens[i]))
      elif self.posicao == i and self.escolha_jogador1:
        escolha_jogador = self.personagens.render(f' [Jogador 2]',True,(122,122,0))
        self.tela.blit(escolha_jogador,(self.px_personagens+self.lista_escolha[i].get_rect().width,self.py_personagens[i]))
    pg.display.flip() 
