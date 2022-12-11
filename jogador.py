import pygame as pg
import time
from minions import Minions
from fisica import Fisica 

class Jogador:
    def __init__ (self,px,py,personagem):
      self.px = px 
      self.py = py
      self.frame = 0 
      self.personagem = personagem
      self.dano_recebido = personagem.dano_recebido
      self.dano_dado = personagem.dano_dado
      self.reconhecimento = personagem.reconhecimento
      self.reconhecido = 1
      self.probabilidade = personagem.probabilidade
      self.teste_probabilistico = 1
      self.tempo_parado = personagem.tempo_parado
      self.ataque_valor = False
      self.atacado_valor = False 
      self.tempo_atacado = 0 
      self.poder = personagem.poder
      self.nome = personagem.nome
      self.animacao = personagem.animacao
      self.animacao_morte = personagem.animacao_morte
      self.animacao_ataque = personagem.animacao_ataque
      self.imagem_principal = self.animacao[0][0]
      self.largura = self.imagem_principal.get_rect().width
      self.altura = self.imagem_principal.get_rect().height
      self.velocidade = personagem.velocidade
      self.vetorx = self.velocidade
      self.vetory = 0 
      self.vx = 0
      self.vy = 0
      self.vida_maxima = personagem.vida_maxima
      self.vida_atual = self.vida_maxima
      self.vida_teste = self.vida_atual
      self.comprimento_barra_vida = 50
      self.razao_vida = self.vida_maxima / self.comprimento_barra_vida
    def desenha_vida(self,tela):
        pg.draw.rect(tela, (255,0,0), (self.px,self.py-20,self.vida_atual/self.razao_vida,10))
        pg.draw.rect(tela, (255,255,255),(self.px,self.py-20,self.comprimento_barra_vida,10),2)
    def cima(self):
      self.vy = - self.velocidade
    def baixo(self):
      self.vy = self.velocidade
    def esquerda(self):
      self.vx = - self.velocidade
    def direita(self):
      self.vx = self.velocidade
    def diagonal(self):
      modulo = (((self.vx)**2+(self.vy)**2)**0.5)/self.velocidade
      self.vx /= modulo  
      self.vy /= modulo
    def ataque(self):
      if self.vida_atual>0 and not self.atacado_valor:
        self.frame = 0
        self.ataque_valor = True
    def atacar(self,corpos,mapa):
      if self.vida_atual> 0 and self.ataque_valor and self.frame == 5:
        fisica = Fisica()
        jogador_teste = Jogador(self.px+self.vetorx,self.py+self.vetory,self.personagem)
        mapa.quebrar(jogador_teste)
        for corpo in corpos:
            for ente in corpo:
              if fisica.contato(jogador_teste,ente):
                  ente.vida_atual-=self.dano_dado*ente.dano_recebido
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
      if(agora - self.tempo_atacado > 2):
        self.atacado_valor = False
        self.tempo_atacado = 0 
    def movimento(self,corpos):
      if self.vida_atual>0:
        fisica = Fisica()
        novo_px = self.px + self.vx
        novo_py = self.py + self.vy
        jogador_teste = Jogador(novo_px,novo_py,self.personagem)
        if not self.atacado_valor and fisica.movimento(jogador_teste,corpos):
          self.px = novo_px
          self.py = novo_py
    def tossir(self,agora):
      self.atacado_valor = True
      self.tempo_atacado = agora-1
      self.vida_atual-=5
    def teste_dano(self):
      if self.vida_atual < self.vida_teste:
        if self.teste_probabilistico == self.probabilidade:
           self.vida_atual = self.vida_teste
        else:
            self.vida_teste = self.vida_atual
        self.teste_probabilistico+=1
      if self.teste_probabilistico>self.probabilidade:
        self.teste_probabilistico = 1
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
