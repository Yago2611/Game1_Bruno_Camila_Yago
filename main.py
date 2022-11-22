import pygame as pg 
import sys 
import time
import random

#Pegar uma imagem
def load_image(name, colorkey=None, scale=1.0):
    image = pg.image.load(name)
    size = image.get_size()
    size = (int(size[0] * scale), int(size[1] * scale))
    image = pg.transform.scale(image, size)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image

def animacao_movimento(imagem):
  lista = []
  px = 14
  py = 515
  largura = 43
  altura = 62
  for i in range(4):
    sublista=[]
    for j in range(9):
      subimagem = imagem.subsurface(pg.Rect(px,py,largura,altura))
      sublista.append(subimagem)
      px+=64
    lista.append(sublista)
    px = 14
    py+=64
  return lista

def animacao_morte(imagem):
  lista = []
  px = 14
  py = 1291
  largura = 55
  altura = 53
  for j in range(6):
      subimagem = imagem.subsurface(pg.Rect(px,py,largura,altura))
      lista.append(subimagem)
      px+=63
  return lista

def animacao_ataque(imagem):
  lista = []
  px = 14
  py = 775
  largura = 54
  altura = 62
  for i in range(4):
    sublista=[]
    for j in range(6):
      subimagem = imagem.subsurface(pg.Rect(px,py,largura,altura))
      sublista.append(subimagem)
      px+=62
    lista.append(sublista)
    px = 14
    py+=64
  return lista

class Configuracoes:   
    #Definindo as Configuracoes do jogo
    TELA = pg.display.set_mode((1280,768),pg.FULLSCREEN)  
    LARGURA_TELA,ALTURA_TELA = TELA.get_size()
    FONTE_TITULO = 96
    FONTE_MENOR = 48
    VELOCIDADE = 1
    P1X,P1Y = (0.3*LARGURA_TELA,ALTURA_TELA//2 - 20)
    P2X,P2Y = (0.7*LARGURA_TELA,ALTURA_TELA//2 - 20)

class Imagens:
  MINIONS_ANIMACAO_MOVIMENTO = animacao_movimento(load_image("minions.png",scale=1))
  MINIONS_ANIMACAO_MORTE = animacao_morte(load_image("minions.png",scale=1))
  MINIONS_ANIMACAO_ATAQUE = animacao_ataque(load_image("minions.png",scale=1))
  GRAMA = load_image("grama.png",scale=1)
  AGUA = load_image("agua.png",scale=1)
  TIJOLO = load_image("tijolo.png",scale=1)
  MADEIRA = load_image("madeira.png",scale=1)

class Cronometro:
    def __init__(self,inicio):
       self.inicio = inicio
    def atualiza(self,tempo,agora):
      if (agora-self.inicio>1):
        tempo[1]-=1
        if tempo[1]<0:
            tempo[1]=59
            tempo[0]-=1
        self.inicio = time.time()
    def desenha(self,tempo,tela):
       cronometro = pg.font.SysFont(None, Configuracoes.FONTE_MENOR)
       Cronometro = cronometro.render(f'{tempo[0]}:{tempo[1]:02d}',True,(0,0,0))
       tamanho_cronometro = Cronometro.get_size()
       largura_cronometro = tamanho_cronometro[0]
       tela.blit(Cronometro, (Configuracoes.LARGURA_TELA /2 - largura_cronometro//2,0.1*Configuracoes.ALTURA_TELA))

class Estado_Jogo:
  def __init__(self,inicio):
    self.inicio_animacao = inicio
    self.inicio_minions = inicio
    self.inicio_morte = 0 
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

class Fisica:
    def __init__(self):
      pass
    def contato(self,corpo1,corpo2):
      return (corpo1.px+corpo1.largura>=corpo2.px and corpo1.px<=corpo2.px+corpo2.largura) and (corpo1.py+corpo1.altura>=corpo2.py and corpo1.py<=corpo2.py+corpo2.altura)
    def distancia(self,corpo1,corpo2):
      return (((((corpo1.px+corpo1.largura)//2)-((corpo2.px+corpo2.largura)//2))**2 + ((((corpo1.py+corpo1.altura)//2))-((corpo2.py+corpo2.altura)//2))**2)**0.5)
    def movimento(self,novo_corpo,corpos):
      mapa = Mapa()
      for corpo in corpos:
          for ente in corpo:
            if self.contato(novo_corpo,ente):
              valor = True
              break
            else:
              valor = False 
          if valor:
            break
      if not mapa.limite(novo_corpo) and not valor:
          return True
      else:
          return False

class Mapa:
    def __init__(self):
      self.terra_plana = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,0,0,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,0,0,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,2,2,2,1,1,1,0,0,1,1,1,2,2,2,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,0,0,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,0,0,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,2,2,2,1,1,1,0,0,1,1,1,2,2,2,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,0,0,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,0,0,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    def limite(self,corpo):
      if corpo.px+corpo.largura>Configuracoes.LARGURA_TELA or corpo.py+corpo.altura> Configuracoes.ALTURA_TELA or corpo.px < 0 or corpo.py <0:
        return True
      x = int(corpo.px//32)
      y = int(corpo.py//32) 
      x2 = int((corpo.px + corpo.largura)//32)
      y2 = int((corpo.py + corpo.altura)//32)
      if self.terra_plana[y][x] == 2 or self.terra_plana[y][x2] == 2 or self.terra_plana[y2][x] == 2 or self.terra_plana[y2][x2] == 2:
        return True
      else: 
        return False
    def dano(self,corpo):
      x = int(corpo.px//32)
      y = int(corpo.py//32) 
      x2 = int((corpo.px + corpo.largura)//32)
      y2 = int((corpo.py + corpo.altura)//32)
      if self.terra_plana[y][x] == 0 or self.terra_plana[y][x2] == 0 or self.terra_plana[y2][x] == 0 or self.terra_plana[y2][x2] == 0:
        corpo.vida_atual -= 0.1
    def quebrar(self,corpo):
      x = int(corpo.px//32)
      y = int(corpo.py//32) 
      x2 = int((corpo.px + corpo.largura)//32)
      y2 = int((corpo.py + corpo.altura)//32)
      if self.terra_plana[y][x] == 3 and x in [18,21]:
        self.terra_plana[y][x] = 1
      elif x in [19,20]:
        self.terra_plana[y][x] = 0
      if self.terra_plana[y][x2] == 3 and x2 in [18,21]:
        self.terra_plana[y][x2] = 1
      elif x2 in [19,20]:
        self.terra_plana[y][x2] = 0
      if self.terra_plana[y2][x] == 3 and x in [18,21]:
        self.terra_plana[y2][x] = 1
      elif x in [19,20]:
        self.terra_plana[y2][x] = 0
      if self.terra_plana[y2][x2] == 3 and x2 in [18,21]:
        self.terra_plana[y2][x2] = 1
      elif x2 in [19,20]:
        self.terra_plana[y2][x2] = 0
    def desenha(self,tela):
      for i in range(len(self.terra_plana)):
        for j in range(len(self.terra_plana[i])):
          if self.terra_plana[i][j] == 0:
           tela.blit(Imagens.AGUA, (32*j,32*i))
          elif self.terra_plana[i][j] == 1:
            tela.blit(Imagens.GRAMA, (32*j,32*i))
          elif self.terra_plana[i][j] == 2:
            tela.blit(Imagens.TIJOLO, (32*j,32*i))
          elif self.terra_plana[i][j] == 3:
            tela.blit(Imagens.MADEIRA, (32*j,32*i))

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

class Personagem:
   def __init__(self, nome, imagem, poder):
    self.nome = nome
    self.velocidade = Configuracoes.VELOCIDADE
    self.vida_maxima = 200
    self.animacao = animacao_movimento(load_image(imagem,scale=1))
    self.animacao_morte = animacao_morte(load_image(imagem,scale=1))
    self.animacao_ataque = animacao_ataque(load_image(imagem,scale=1))
    self.poder = poder

class Jogador:  
    def __init__ (self,px,py,personagem):
      self.px = px 
      self.py = py
      self.frame = 0 
      self.personagem = personagem
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
      if self.vida_atual>0:
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
                  ente.vida_atual-=10
                  novo_ente = Minions(corpos)
                  novo_ente.px = ente.px + 20*self.vetorx
                  novo_ente.py = ente.py + 20*self.vetory
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
        jogador_teste = Jogador(novo_px,novo_py,self.personagem)
        if not self.atacado_valor and fisica.movimento(jogador_teste,corpos):
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

class Cena_final:
  def __init__(self,jogador1,jogador2,tela):
    self.jogador1 = jogador1
    self.jogador2 = jogador2
    self.tela = tela
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

def main():
   #Inicializando o pygame
   pg.init()
   cena_inicial = True
   cena_principal = False
   cena_final = False
   minions = [] 
   tela = Configuracoes.TELA
   escolha_jog1 = False
   escolha_jog2 = False 
   posicao = 0 
   while cena_inicial:
    for event in pg.event.get():
        if event.type == (pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or (pg.key.get_pressed()[pg.K_ESCAPE]): 
            print("Encerrando o programa.")
            sys.exit()
    titulo = pg.font.SysFont(None,Configuracoes.FONTE_TITULO)
    escolha = pg.font.SysFont(None, Configuracoes.FONTE_MENOR)
    personagens = pg.font.SysFont(None, Configuracoes.FONTE_MENOR)
    Raio = Poder("raio.png","Projetil")
    Nuvem = Poder("nuvem.png","Área")
    Cura = Poder("cura.png","Cura")
    Gato = Poder("gato.png","Projetil")
    Nikola = Personagem("Nikola Tesla","nikola.png",Raio) 
    Marie = Personagem("Marie Curie","marie.png",Nuvem)
    Darwin = Personagem("Charles Darwin", "darwin.png", Cura)
    Darwin.vida_maxima = 400 #Vantagem
    Darwin.velocidade *= 0.5 #Desvantagem
    Erwin = Personagem("Erwin Schrodinger","erwin.png",Gato)
    lista_personagens = [Nikola,Marie,Darwin,Erwin]
    Titulo = titulo.render(f'Guerra de Cientistas',True,(0,0,0))
    Escolha = escolha.render(f'Escolha um personagem:', True, (0,0,0))
    lista_escolha_personagens = []
    for i in range(len(lista_personagens)):
      personagemi = personagens.render(f'{i+1}) {lista_personagens[i].nome}',True,(0,0,0))
      lista_escolha_personagens.append(personagemi)
    tela.fill((255, 255, 255))
    PX = Configuracoes.LARGURA_TELA // 2 - Titulo.get_size()[0] // 2
    PY = 0.01 * Configuracoes.ALTURA_TELA
    px = Configuracoes.LARGURA_TELA // 2 - Escolha.get_size()[0] // 2
    py = (0.2 * Configuracoes.ALTURA_TELA // 2) + (Escolha.get_size()[1] * 1.5)
    px_personagens = 0.05*Configuracoes.LARGURA_TELA 
    py_personagens = []
    for i in range(len(lista_escolha_personagens)):
      pyi = Configuracoes.ALTURA_TELA*(0.3 + 0.1*i) +  (lista_escolha_personagens[0].get_size()[1]*1.5)
      py_personagens.append(pyi)
    tela.blit(Titulo, (PX,PY))
    tela.blit(Escolha, (px, py))
    for i in range(len(lista_escolha_personagens)):
      tela.blit(lista_escolha_personagens[i],(px_personagens,py_personagens[i]))

    if (event.type == pg.KEYDOWN and event.key == pg.K_DOWN):
        if posicao>=0 and posicao<3:
            posicao+=1
    elif (event.type == pg.KEYDOWN and event.key == pg.K_UP):
        if posicao>0 and posicao<=3:
            posicao-=1

    if escolha_jog1 == False and event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
        jogador1 = Jogador(Configuracoes.P1X,Configuracoes.P1Y,lista_personagens[posicao])
        escolha_jog1 = True        
    elif escolha_jog1 and event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
        jogador2 = Jogador(Configuracoes.P2X,Configuracoes.P2Y,lista_personagens[posicao])
        escolha_jog2 = True        

    #Escolha dos personagens
    for i in range(len(lista_escolha_personagens)):
      if posicao == i and not escolha_jog1:
        escolha_jogador = personagens.render(f' [Jogador 1]',True,(122,122,0))
        tela.blit(escolha_jogador,(px_personagens+lista_escolha_personagens[i].get_rect().width,py_personagens[i]))
      elif posicao == i and escolha_jog1:
        escolha_jogador = personagens.render(f' [Jogador 2]',True,(122,122,0))
        tela.blit(escolha_jogador,(px_personagens+lista_escolha_personagens[i].get_rect().width,py_personagens[i]))

    if escolha_jog1 and escolha_jog2:
        cena_inicial = False
        cena_principal = True
    
    pg.display.flip() 
   
   #Cena Principal
   tempo = [1,30]
   jogador2.vetorx *=-1
   mapa = Mapa()
   cronometro = Cronometro(time.time())
   estado_jogo = Estado_Jogo(time.time())
   while cena_principal:
    for event in pg.event.get():
        if event.type == (pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or (pg.key.get_pressed()[pg.K_ESCAPE]): 
            print("Encerrando o programa.")
            sys.exit()
   
    fisica = Fisica()
    agora = time.time()
    if (event.type == pg.KEYDOWN and event.key == pg.K_d) or (pg.key.get_pressed()[pg.K_d]):
      jogador1.direita()
    elif (event.type == pg.KEYDOWN and event.key == pg.K_a) or (pg.key.get_pressed()[pg.K_a]):
      jogador1.esquerda()
    else:
      jogador1.vx = 0 
    if (event.type == pg.KEYDOWN and event.key == pg.K_l) or (pg.key.get_pressed()[pg.K_l]):
      jogador2.direita()
    elif (event.type == pg.KEYDOWN and event.key == pg.K_j) or (pg.key.get_pressed()[pg.K_j]):
      jogador2.esquerda()
    else:
      jogador2.vx = 0 
    if (event.type == pg.KEYDOWN and event.key == pg.K_s) or (pg.key.get_pressed()[pg.K_s]):
      jogador1.baixo()
    elif (event.type == pg.KEYDOWN and event.key == pg.K_w) or (pg.key.get_pressed()[pg.K_w]):
      jogador1.cima()
    else:
      jogador1.vy = 0  
    if (event.type == pg.KEYDOWN and event.key == pg.K_k) or (pg.key.get_pressed()[pg.K_k]):
      jogador2.baixo()
    elif (event.type == pg.KEYDOWN and event.key == pg.K_i) or (pg.key.get_pressed()[pg.K_i]):
      jogador2.cima()
    else:
      jogador2.vy = 0 
    if (jogador1.vx!=0) and (jogador1.vy!=0):
      jogador1.diagonal()
    if (jogador2.vx!=0) and (jogador2.vy!=0):
      jogador2.diagonal()
    #Mudar a posicao dos jogadores
    jogador1.movimento([[jogador2],minions])
    jogador2.movimento([[jogador1],minions])
    
    #Desenhar a tela
    mapa.desenha(tela)
    mapa.dano(jogador1)
    mapa.dano(jogador2)
    #Pegar uma imagem
    jogador1.desenha(tela)
    jogador2.desenha(tela)
    jogador1.desenha_vida(tela)
    jogador2.desenha_vida(tela)

    #Poder
    if event.type == pg.KEYDOWN and event.key == pg.K_e or (pg.key.get_pressed()[pg.K_e]):
      jogador1.poder.lancar(jogador1,agora)
    if event.type == pg.KEYDOWN and event.key == pg.K_q or (pg.key.get_pressed()[pg.K_q]):
      jogador1.ataque()

    if event.type == pg.KEYDOWN and event.key == pg.K_o or (pg.key.get_pressed()[pg.K_o]):
      jogador2.poder.lancar(jogador2,agora)
    if event.type == pg.KEYDOWN and event.key == pg.K_u or (pg.key.get_pressed()[pg.K_u]):
      jogador2.ataque()

    jogador1.atacar([[jogador2],minions],mapa)
    jogador2.atacar([[jogador1],minions],mapa)
    jogador1.atacado(agora)
    jogador2.atacado(agora)
    jogador1.poder.efeito([[jogador2],minions],jogador1,agora)
    jogador2.poder.efeito([[jogador1],minions],jogador2,agora)

    #Minions
    estado_jogo.gera_minions(agora,[[jogador1,jogador2],minions])
    for minion in minions:
      if minion.valor:
          minion.velocidade(jogador1,jogador2)
          minions_teste = minions[:]
          minions_teste.remove(minion)
          if (fisica.distancia(minion,jogador1) <50 or fisica.distancia(minion,jogador2)<50) and not minion.ataque_valor:
            minion.ataque()
          minion.atacar([[jogador1,jogador2]],mapa)
          minion.atacado(agora)
          minion.movimento([[jogador1,jogador2],minions_teste])
          mapa.dano(minion)
          minion.desenha(tela) 
          minion.desenha_vida(tela)
          if minion.vida_atual <= 0 and minion.tempo_morte == 0:
            minion.frame = 0 
            minion.tempo_morte = time.time()
          if minion.tempo_morte!=0 and agora - minion.tempo_morte > 2:
            minion.valor = False
      else:
        minions.remove(minion)
    
    if jogador1.poder.valor:
      jogador1.poder.movimento()
      jogador1.poder.desenha(tela)
    if jogador2.poder.valor:
      jogador2.poder.movimento()
      jogador2.poder.desenha(tela)

    estado_jogo.animacao(agora,[[jogador1,jogador2],minions])
    cronometro.atualiza(tempo,agora)
    cronometro.desenha(tempo,tela)
    cena_principal = estado_jogo.encerra(agora,tempo,jogador1,jogador2)
    cena_final = not cena_principal

    pg.display.flip()
    
    if cena_final:
      final = Cena_final(jogador1,jogador2,tela)
      final.rodar()

if __name__ == "__main__":
   main() 
