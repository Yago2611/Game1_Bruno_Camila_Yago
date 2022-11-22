import random
import pygame as pg
import time   
from fisica import Fisica
from configuracoes import Configuracoes
from imagens import Imagens 


class Minions:
    def __init__(self,corpos):
        fisica = Fisica()
        self.valor = True
        self.frame = 0
        self.vx = 0
        self.vy = 0
        self.tempo_morte = 0 
        self.tempo_atacado = 0 
        self.ataque_valor = False
        self.atacado_valor = False 
        self.vetorx = Configuracoes.VELOCIDADE
        self.vetory = 0 
        self.animacao = Imagens.MINIONS_ANIMACAO_MOVIMENTO
        self.animacao_morte = Imagens.MINIONS_ANIMACAO_MORTE
        self.animacao_ataque = Imagens.MINIONS_ANIMACAO_ATAQUE
        self.largura = self.animacao[0][0].get_rect().width
        self.altura = self.animacao[0][0].get_rect().height
        self.vel = 0 
        self.vida_atual = 100
        self.vida_maxima = 100
        self.comprimento_barra_vida = 50
        self.razao_vida = self.vida_maxima / self.comprimento_barra_vida
        self.px = Configuracoes.LARGURA_TELA//2
        self.py = Configuracoes.ALTURA_TELA//2
        while not fisica.movimento(self,corpos):
          self.px = random.randrange(0,Configuracoes.LARGURA_TELA-self.largura)
          self.py = random.randrange(0,Configuracoes.ALTURA_TELA-self.altura)
    def desenha_vida(self,tela):
        pg.draw.rect(tela, (255,0,0), (self.px,self.py-20,self.vida_atual/self.razao_vida,10))
        pg.draw.rect(tela, (255,255,255),(self.px,self.py-20,self.comprimento_barra_vida,10),2)    
    def velocidade(self,jogador1,jogador2):
        fisica = Fisica()
        if fisica.distancia(self,jogador1) > fisica.distancia(self,jogador2):
          self.vx = jogador2.px - self.px
          self.vy = jogador2.py - self.py
        else:
          self.vx = jogador1.px - self.px
          self.vy = jogador1.py - self.py
       #Encontramos o modulo do vetor velocidade
        self.vel = ((self.vx**2 + self.vy**2)**0.5)/(0.8*Configuracoes.VELOCIDADE)
        self.vx /= self.vel
        self.vy /= self.vel #Formamos os vetores unitarios
    def ataque(self):
      if self.vida_atual>0:
        self.frame = 0
        self.ataque_valor = True    
    def atacar(self,corpos,mapa):
      if self.vida_atual> 0 and self.ataque_valor and self.frame == 5:
        fisica = Fisica()
        minion_teste = Minions(corpos)
        minion_teste.px = self.px + self.vetorx
        minion_teste.py = self.py + self.vetory
        mapa.quebrar(minion_teste)
        for corpo in corpos:
            for ente in corpo:
              if fisica.contato(minion_teste,ente):
                  ente.vida_atual-=10
                  novo_ente = Minions(corpos)
                  novo_ente.px = ente.px + 50*self.vetorx
                  novo_ente.py = ente.py + 50*self.vetory
                  corpos_teste = []
                  for x in corpos:
                    x_teste = x[:]
                    corpos_teste.append(x_teste)
                  for x_teste in corpos_teste:
                    if ente in x_teste:
                      x_teste.remove(ente)
                  if fisica.movimento(novo_ente,corpos_teste):
                    ente.px = novo_ente.px
                    ente.py = novo_ente.py
                  ente.atacado_valor = True 
        self.ataque_valor = False
        self.frame = 0
    def atacado(self,agora):
      if(self.atacado_valor and self.tempo_atacado == 0):
        self.tempo_atacado = time.time()
      if(agora - self.tempo_atacado > 3):
        self.atacado_valor = False
        self.tempo_atacado = 0 
    def movimento(self,corpos):
      if self.vida_atual>0:
        fisica = Fisica()
        novo_px = self.px + self.vx
        novo_py = self.py + self.vy
        minion_teste = Minions(corpos)
        minion_teste.px = novo_px
        minion_teste.py = novo_py
        if not self.atacado_valor and fisica.movimento(minion_teste,corpos):
          self.px = novo_px
          self.py = novo_py
    def desenha(self,tela):
      if self.vida_atual>0:
        self.vetor_direcao()
        if self.ataque_valor:
          if self.vetory <0:
            n = 0
          elif self.vetorx < 0:
            n = 1
          elif self.vetory > 0:
            n = 2
          elif self.vetorx > 0:
            n = 3
          if self.frame>5:
            self.frame = 5
          tela.blit(self.animacao_ataque[n][self.frame],(self.px,self.py))
        else:
          if self.vy<0:
            n = 0
          elif self.vx<0:
            n = 1
          elif self.vy>0:
            n = 2
          elif self.vx>0:
            n = 3
          else:
            n = -1
          if self.frame>8:
            self.frame = 0
          if n>=0:
            tela.blit(self.animacao[n][self.frame],(self.px,self.py))
          if self.vx == 0 and self.vy == 0:
              if self.vetory <0:
                tela.blit(self.animacao[0][0],(self.px,self.py))
              elif self.vetorx < 0:
                tela.blit(self.animacao[1][0],(self.px,self.py))
              elif self.vetory > 0:
                tela.blit(self.animacao[2][0],(self.px,self.py))
              elif self.vetorx > 0:
                tela.blit(self.animacao[3][0],(self.px,self.py))
              else:
                tela.blit(self.animacao[n][self.frame],(self.px,self.py))
      else:
        if self.frame>5:
          self.frame = 5
        tela.blit(self.animacao_morte[self.frame],(self.px,self.py))
    def vetor_direcao(self):
      if not (self.vx == 0 and self.vy ==0):
        self.vetorx = self.vx
        self.vetory = self.vy
