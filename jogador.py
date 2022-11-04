import pygame as pg
import PERSONAGENS


class Jogador:
  def __init__ (self,posicao,personagem):
    self.posicao = posicao
    self.personagem = personagem #O jogador ira receber um objeto da classe personagem
    self.vida = personagem.vida
    self.vx = 0
    self.vy = 0
  def mover_cima(self):
    self.vx = -Configuracoes.VELOCIDADE
  def mover_baixo(self):
    self.vx = Configuracoes.VELOCIDADE
  def mover_esquerda(self):
    self.vy = -Configuracoes.VELOCIDADE
  def mover_direita(self):
    self.vy = Configuracoes.VELOCIDADE
  def posicao_na_tela(self):
        self.posicao = (vx, vy)
 
      
# p1 = (pass , PERSONAGENS.nikola_tesla, PERSONAGENS.raios, PERSONAGENS.nikola_tesla)
