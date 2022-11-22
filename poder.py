import time
from imagens import load_image 
from fisica import Fisica

class Poder:
  def __init__(self,imagem,tipo):
    self.imagem = load_image(imagem, scale=0.1)
    self.tipo = tipo
    self.px,self.py = 0,0
    self.valor = False
    self.tempo_de_uso = 0 
    self.vx = 0
    self.vy = 0
    self.largura,self.altura = self.imagem.get_rect().width,self.imagem.get_rect().height
  def lancar(self,jogador,agora):
    if jogador.vida_atual>0 and self.tempo_de_uso == 0:
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
    elif self.tempo_de_uso !=0:
      if self.tipo == "Projetil" and agora - self.tempo_de_uso > 2:
        self.tempo_de_uso = 0
      elif agora - self.tempo_de_uso > 7:
        self.tempo_de_uso = 0
  def movimento(self):
    if self.valor:
      self.px += self.vx
      self.py += self.vy
  def efeito(self,corpos,jogador,agora):
    if self.valor:
      fisica = Fisica()
      if self.tipo == "Projetil":
        for corpo in corpos:
          for ente in corpo:
            if fisica.contato(ente,self):
              ente.vida_atual -= 40
              self.valor = False
      elif self.tipo == "Área":
        for corpo in corpos:
          for ente in corpo:
            if fisica.contato(ente,self):
              ente.vida_atual -= 1
        if agora - self.tempo_de_uso > 5:
          self.valor = False 
      elif self.tipo == "Cura":
        if fisica.contato(jogador,self) and jogador.vida_atual < jogador.vida_maxima:
         jogador.vida_atual+=0.1   
        if agora - self.tempo_de_uso > 5:
          self.valor = False 
  def desenha(self,tela):
    tela.blit(self.imagem, (self.px,self.py))
