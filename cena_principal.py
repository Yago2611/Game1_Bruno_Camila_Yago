import pygame as pg
import sys 
import time
from cronometro import Cronometro 
from estado_jogo import Estado_jogo
from fisica import Fisica 
from mapa import Mapa

class Cena_principal:
  def __init__(self,cena_inicial):
    self.tela = cena_inicial.tela
    self.jogador1 = cena_inicial.jogador1
    self.jogador2 = cena_inicial.jogador2
    self.encerrada = False
    self.tempo_parado = False
    self.minions = []
    self.tempo = [1,30]
    self.jogador2.vetorx *=-1
    self.mapa = Mapa()
    self.cronometro = Cronometro(time.time())
    self.estado_jogo = Estado_jogo(time.time())
    self.fisica = Fisica()
    self.agora = time.time()
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
        if not self.tempo_parado:
          if (event.type == pg.KEYDOWN and event.key == pg.K_d) or (pg.key.get_pressed()[pg.K_d]):
            self.jogador1.direita()
          elif (event.type == pg.KEYDOWN and event.key == pg.K_a) or (pg.key.get_pressed()[pg.K_a]):
            self.jogador1.esquerda()
          else:
            self.jogador1.vx = 0 
          if (event.type == pg.KEYDOWN and event.key == pg.K_l) or (pg.key.get_pressed()[pg.K_l]):
            self.jogador2.direita()
          elif (event.type == pg.KEYDOWN and event.key == pg.K_j) or (pg.key.get_pressed()[pg.K_j]):
            self.jogador2.esquerda()
          else:
            self.jogador2.vx = 0 
          if (event.type == pg.KEYDOWN and event.key == pg.K_s) or (pg.key.get_pressed()[pg.K_s]):
            self.jogador1.baixo()
          elif (event.type == pg.KEYDOWN and event.key == pg.K_w) or (pg.key.get_pressed()[pg.K_w]):
            self.jogador1.cima()
          else:
            self.jogador1.vy = 0  
          if (event.type == pg.KEYDOWN and event.key == pg.K_k) or (pg.key.get_pressed()[pg.K_k]):
            self.jogador2.baixo()
          elif (event.type == pg.KEYDOWN and event.key == pg.K_i) or (pg.key.get_pressed()[pg.K_i]):
            self.jogador2.cima()
          else:
            self.jogador2.vy = 0 
          if event.type == pg.KEYDOWN and event.key == pg.K_e or (pg.key.get_pressed()[pg.K_e]):
            self.jogador1.poder.lancar(self.jogador1,self.agora)
          if event.type == pg.KEYDOWN and event.key == pg.K_q or (pg.key.get_pressed()[pg.K_q]):
            self.jogador1.ataque()
          if event.type == pg.KEYDOWN and event.key == pg.K_o or (pg.key.get_pressed()[pg.K_o]):
            self.jogador2.poder.lancar(self.jogador2,self.agora)
          if event.type == pg.KEYDOWN and event.key == pg.K_u or (pg.key.get_pressed()[pg.K_u]):
            self.jogador2.ataque()
  def atualiza_estado(self):
      self.agora = time.time()
      self.jogador1.poder.efeito([[self.jogador2],self.minions],self.jogador1,self.agora,self)
      self.jogador2.poder.efeito([[self.jogador1],self.minions],self.jogador2,self.agora,self)
      if not self.tempo_parado:
        if (self.jogador1.vx!=0) and (self.jogador1.vy!=0):
          self.jogador1.diagonal()
        if (self.jogador2.vx!=0) and (self.jogador2.vy!=0):
          self.jogador2.diagonal()
        self.jogador1.teste_dano()
        self.jogador2.teste_dano()
        self.jogador1.movimento([[self.jogador2],self.minions])
        self.jogador2.movimento([[self.jogador1],self.minions])
        self.jogador1.poder.movimento()
        self.jogador2.poder.movimento()
        self.jogador1.atacar([[self.jogador2],self.minions],self.mapa)
        self.jogador2.atacar([[self.jogador1],self.minions],self.mapa)
        self.jogador1.atacado(self.agora)
        self.jogador2.atacado(self.agora)
        self.estado_jogo.gera_minions(self.agora,[[self.jogador1,self.jogador2],self.minions])
        for minion in self.minions:
          if minion.valor:
              minion.velocidade(self.jogador1,self.jogador2)
              self.minions_teste = self.minions[:]
              self.minions_teste.remove(minion)
              if (self.fisica.distancia(minion,self.jogador1) <50 or self.fisica.distancia(minion,self.jogador2)<50) and not minion.ataque_valor:
                minion.ataque(self.agora)
              minion.atacado(self.agora)
              minion.movimento([[self.jogador1,self.jogador2],self.minions_teste])
              minion.atacar([[self.jogador1,self.jogador2]],self.mapa)
              self.mapa.dano(minion)
              if minion.vida_atual <= 0 and minion.tempo_morte == 0:
                minion.frame = 0 
                minion.tempo_morte = time.time()
              if minion.tempo_morte!=0 and self.agora - minion.tempo_morte > 2:
                minion.valor = False
          else:
            self.minions.remove(minion)
        self.mapa.dano(self.jogador1)
        self.mapa.dano(self.jogador2)
        self.estado_jogo.animacao(self.agora,[[self.jogador1,self.jogador2],self.minions])
        self.estado_jogo.tosse(self.agora,[self.jogador1,self.jogador2])
        self.cronometro.atualiza(self.tempo,self.agora)
      self.encerrada = not self.estado_jogo.encerra(self.agora,self.tempo,self.jogador1,self.jogador2)
  def desenha(self):
    self.mapa.desenha(self.tela)
    self.jogador1.desenha(self.tela)
    self.jogador2.desenha(self.tela)
    self.jogador1.desenha_vida(self.tela)
    self.jogador2.desenha_vida(self.tela)
    for minion in self.minions:
      if minion.valor:
            minion.desenha(self.tela) 
            minion.desenha_vida(self.tela)
    if self.jogador1.poder.valor:
        self.jogador1.poder.desenha(self.tela)
    if self.jogador2.poder.valor:
        self.jogador2.poder.desenha(self.tela)
    self.cronometro.desenha(self.tempo,self.tela)
    pg.display.flip()
