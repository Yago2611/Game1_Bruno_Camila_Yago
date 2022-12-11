import time
from minions import Minions

class Estado_jogo:
  def __init__(self,inicio):
    self.inicio_animacao = inicio
    self.inicio_minions = inicio
    self.inicio_morte = 0 
    self.inicio_tosse = inicio
  def encerra(self,agora,tempo,jogador1,jogador2):
    if jogador1.vida_atual<=0 and self.inicio_morte == 0:
        jogador1.frame = 0
        self.inicio_morte = time.time()
    if jogador2.vida_atual<=0 and self.inicio_morte == 0:
        jogador2.frame = 0
        self.inicio_morte = time.time()
    if(tempo[0] == 0 and tempo[1] == 0):
        return False
    elif self.inicio_morte!=0 and (agora - self.inicio_morte) > 3:
      return False
    else:
      return True 
  def gera_minions(self,agora,corpos):
    if agora - self.inicio_minions > 3 and len(corpos[1]) < 3:
      minion = Minions(corpos)
      corpos[1].append(minion)
      self.inicio_minions = agora
  def animacao(self,agora,corpos):
    if agora - self.inicio_animacao > 0.15: #Velocidade da animacao
      for corpo in corpos:
        for ente in corpo:
          ente.frame+=1
      self.inicio_animacao = agora
  def tosse(self,agora,corpos):
    if agora - self.inicio_tosse > 10:
      for corpo in corpos:
        if corpo.tempo_parado == 10:
          corpo.tossir(agora)
      self.inicio_tosse = agora
