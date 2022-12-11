import time
import sys
import pygame as pg
from imagens import load_image 
from fisica import Fisica
from jogador import Jogador
from mapa import Mapa

class Poder:
  def __init__(self,imagem,tipo):
    self.tipo = tipo
    if tipo == "Teletransporte":
      self.imagem = load_image(imagem, scale=0.05)
    else: 
     self.imagem = load_image(imagem, scale=0.1)
    self.tempo = 0 
    self.px,self.py = 0,0
    self.dano_area = 0.5
    self.dano_projetil = 40
    self.valor = False
    self.tempo_de_uso = 0 
    self.vx = 0
    self.vy = 0
    self.corpo_escolhido = 0
    self.p1_escolhido = False
    self.p2_escolhido = False
    self.largura,self.altura = self.imagem.get_rect().width,self.imagem.get_rect().height
  def lancar(self,jogador,agora):
    if jogador.vida_atual>0 and self.tempo_de_uso == 0 and not jogador.atacado_valor:
      self.valor = True
      self.tempo_de_uso = time.time() 
      jogador.vetor_direcao()
      if self.tipo == "Projetil":
        self.vx = jogador.vetorx
        self.vy = jogador.vetory
        self.px = jogador.px 
        self.py = jogador.py
      elif self.tipo == "Área":
        self.px = jogador.px + 100*jogador.vetorx
        self.py = jogador.py + 100*jogador.vetory
      elif self.tipo == "Cura":
        self.px = jogador.px - 70
        self.py = jogador.py + jogador.largura - 100
      elif self.tipo == "Teletransporte":
        self.px = - 100
        self.py = - 100
        self.tempo_de_uso = 0
        self.corpo_escolhido = 0
        self.p1_escolhido = False
        self.p2_escolhido = False
    elif self.tempo_de_uso !=0:
      if self.tipo == "Projetil" and agora - self.tempo_de_uso > 2:
        self.tempo_de_uso = 0
      elif agora - self.tempo_de_uso > 7:
        self.tempo_de_uso = 0
  def movimento(self):
    if self.valor:
      self.px += self.vx
      self.py += self.vy
  def efeito(self,corpos,jogador,agora,cena_principal):
    mapa = Mapa()
    if self.valor:
      fisica = Fisica()
      if self.tipo == "Teletransporte":
        if not (self.p1_escolhido and self.p2_escolhido):
          cena_principal.tempo_parado = True
          if not self.p1_escolhido and pg.mouse.get_pressed()[0]:
            (p1x, p1y) = pg.mouse.get_pos()
            teste = Jogador(p1x,p1y,jogador.personagem)        
            for corpo in corpos:
              for ente in corpo:
                if fisica.contato(ente,teste):
                  self.corpo_escolhido = ente
                  self.px = ente.px - 15
                  self.py = ente.py - self.altura
                  self.tempo = time.time()
                  self.p1_escolhido = True 
          elif not self.p2_escolhido and pg.mouse.get_pressed()[0] and agora-self.tempo>0.5:  
            (p2x,p2y) = pg.mouse.get_pos()
            teste = Jogador(p2x,p2y,jogador.personagem)
            if fisica.movimento(teste,corpos):
              self.corpo_escolhido.px = p2x
              self.corpo_escolhido.py = p2y      
              self.p2_escolhido = True  
          if self.p1_escolhido and self.p2_escolhido:
            if cena_principal.tempo_parado:
              self.tempo_de_uso = time.time()
              cena_principal.tempo_parado = False
              self.valor = False
      if not cena_principal.tempo_parado:
        if self.tipo == "Projetil":
          if mapa.limite(self):
            self.valor = False
          for corpo in corpos:
            for ente in corpo:
              if fisica.contato(ente,self):
                if jogador.reconhecido != jogador.reconhecimento:
                  ente.vida_atual -= self.dano_projetil
                self.valor = False
                jogador.reconhecido+=1
                if jogador.reconhecido>jogador.reconhecimento:
                  jogador.reconhecido = 1
        elif self.tipo == "Área":
          for corpo in corpos:
            for ente in corpo:
              if fisica.contato(ente,self):
                ente.vida_atual -= self.dano_area
          if agora - self.tempo_de_uso > 5:
            self.valor = False 
        elif self.tipo == "Cura":
          if fisica.contato(jogador,self) and jogador.vida_atual < jogador.vida_maxima:
            jogador.vida_atual+=0.1   
          if agora - self.tempo_de_uso > 5:
            self.valor = False  
  def desenha(self,tela):
    tela.blit(self.imagem, (self.px,self.py))
