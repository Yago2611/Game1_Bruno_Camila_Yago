import pygame as pg 
import sys 
import time

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
  largura = 43
  altura = 53
  for j in range(6):
      subimagem = imagem.subsurface(pg.Rect(px,py,largura,altura))
      lista.append(subimagem)
      px+=63
  return lista

class Configuracoes:   
    #Definindo as Configuracoes do jogo
    TELA = pg.display.set_mode()  
    LARGURA_TELA,ALTURA_TELA = TELA.get_size()
    FONTE_TITULO = 96
    FONTE_MENOR = 48
    VELOCIDADE = 1
    MINIONS_ANIMACAO_MOVIMENTO = animacao_movimento(load_image("minions.png",scale=1))
    MINIONS_ANIMACAO_MORTE = animacao_morte(load_image("minions.png",scale=1))

class Fisica:
    def __init__(self):
      pass
    def contato(self,corpo1,corpo2):
      return (corpo1.px+corpo1.largura>=corpo2.px and corpo1.px<=corpo2.px+corpo2.largura) and (corpo1.py+corpo1.altura>=corpo2.py and corpo1.py<=corpo2.py+corpo2.altura)

class Mapa:
    def __init__(self):
      self.terra_plana = (0.05*Configuracoes.LARGURA_TELA, 0.1*Configuracoes.ALTURA_TELA, 0.9*Configuracoes.LARGURA_TELA, 0.8*Configuracoes.ALTURA_TELA)
    def limite(self,corpo):
      return (corpo.px <= 0.05*Configuracoes.LARGURA_TELA or corpo.px + corpo.largura >= 0.95*Configuracoes.LARGURA_TELA or corpo.py <= 0.1*Configuracoes.ALTURA_TELA or corpo.py + corpo.altura >= 0.9*Configuracoes.ALTURA_TELA)
    def desenha(self,tela):
      tela.fill((0, 0, 255))
      pg.draw.rect(tela,(0, 255, 0),self.terra_plana,0)

class Poder:
  def __init__(self,imagem):
    self.imagem = load_image(imagem, scale=0.1)
    self.px,self.py = 0,0
    self.valor = False
    self.vx = 0
    self.vy = 0
    self.largura,self.altura = self.imagem.get_rect().width,self.imagem.get_rect().height
  def lancar(self,jogador):
    self.valor = True
    jogador.vetor_direcao()
    self.vx = jogador.vetorx
    self.vy = jogador.vetory
    self.px = jogador.px
    self.py = jogador.py 
  def movimento(self):
    self.px += self.vx
    self.py += self.vy
  def dano(self,corpo):
    if self.px+self.altura>=corpo.px and self.px<=corpo.px+corpo.largura and (self.py+self.largura>=corpo.py and self.py<=corpo.py+corpo.altura):
        corpo.vida -= 50
        self.valor = False
  def desenha(self,tela):
    tela.blit(self.imagem, (self.px,self.py))

class Personagem:
   def __init__(self, nome, imagem, poder):
    self.nome = nome
    self.animacao = animacao_movimento(load_image(imagem,scale=1))
    self.animacao_morte = animacao_morte(load_image(imagem,scale=1))
    self.poder = poder
    self.vida = 100

class Jogador:  
    def __init__ (self,px,py,personagem):
      self.px = px 
      self.py = py
      self.frame = 0 
      self.personagem = personagem
      self.poder = personagem.poder
      self.vida = personagem.vida
      self.nome = personagem.nome
      self.animacao = personagem.animacao
      self.animacao_morte = personagem.animacao_morte
      self.imagem_principal = self.animacao[0][0]
      self.largura = self.imagem_principal.get_rect().width
      self.altura = self.imagem_principal.get_rect().height
      self.vetorx = Configuracoes.VELOCIDADE
      self.vetory = 0 
      self.vx = 0
      self.vy = 0
      self.vida_atual = 200
      self.vida_maxima = 200
      self.comprimento_barra_vida = 50
      self.razao_vida = self.vida_maxima / self.comprimento_barra_vida
    def desenha_vida(self,tela):
        pg.draw.rect(tela, (255,0,0), (self.px,self.py-20,self.vida_atual/self.razao_vida,10))
        pg.draw.rect(tela, (255,255,255),(self.px,self.py-20,self.comprimento_barra_vida,10),2)
    def cima(self):
      self.vy = - Configuracoes.VELOCIDADE 
    def baixo(self):
      self.vy = Configuracoes.VELOCIDADE
    def esquerda(self):
      self.vx = - Configuracoes.VELOCIDADE
    def direita(self):
      self.vx = Configuracoes.VELOCIDADE
    def diagonal(self):
      modulo = (((self.vx)**2+(self.vy)**2)**0.5)/Configuracoes.VELOCIDADE
      self.vx /= modulo  
      self.vy /= modulo
    def movimento(self,corpos):
      if self.vida_atual>0:
        mapa = Mapa()
        fisica = Fisica()
        novo_px = self.px + self.vx
        novo_py = self.py + self.vy
        jogador_teste = Jogador(novo_px,novo_py,self.personagem)
        for corpo in corpos:
          for ente in corpo:
            if fisica.contato(jogador_teste,ente):
              valor = True
              break
            else:
              valor = False 
          if valor:
            break
        if not mapa.limite(jogador_teste) and not valor:
          self.px = novo_px
          self.py = novo_py
    def desenha(self,tela):
      if self.vida_atual>0:
        self.vetor_direcao()
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
    def __init__(self):
        self.valor = True
        self.frame = 0
        self.px = Configuracoes.LARGURA_TELA//2
        self.py = Configuracoes.ALTURA_TELA//2
        self.vx = 0
        self.vy = 0
        self.tempo_morte = 0 
        self.vetorx = Configuracoes.VELOCIDADE
        self.vetory = 0 
        self.animacao = Configuracoes.MINIONS_ANIMACAO_MOVIMENTO
        self.animacao_morte = Configuracoes.MINIONS_ANIMACAO_MORTE
        self.largura = self.animacao[0][0].get_rect().width
        self.altura = self.animacao[0][0].get_rect().height
        self.vel = 0 
        self.vida_atual = 100
        self.vida_maxima = 100
        self.comprimento_barra_vida = 50
        self.razao_vida = self.vida_maxima / self.comprimento_barra_vida
    def desenha_vida(self,tela):
        pg.draw.rect(tela, (255,0,0), (self.px,self.py-20,self.vida_atual/self.razao_vida,10))
        pg.draw.rect(tela, (255,255,255),(self.px,self.py-20,self.comprimento_barra_vida,10),2)    
    def velocidade(self,jogador1,jogador2):
        if (((jogador1.px-self.px)**2 + (jogador1.py-self.py)**2)**0.5) > (((jogador2.px-self.px)**2 + (jogador2.py-self.py)**2)**0.5): #Comparamos a distancia com os jogadores
          self.vx = jogador2.px - self.px
          self.vy = jogador2.py - self.py
        else:
          self.vx = jogador1.px - self.px
          self.vy = jogador1.py - self.py
       #Encontramos o modulo do vetor velocidade
        self.vel = ((self.vx**2 + self.vy**2)**0.5)/(0.8*Configuracoes.VELOCIDADE)
        self.vx /= self.vel
        self.vy /= self.vel #Formamos os vetores unitarios
    def movimento(self,corpos):
      if self.vida_atual>0:
        mapa = Mapa()
        fisica = Fisica()
        novo_px = self.px + self.vx
        novo_py = self.py + self.vy
        minion_teste = Minions()
        minion_teste.px = novo_px
        minion_teste.py = novo_py
        for corpo in corpos:
          for ente in corpo:
            if fisica.contato(minion_teste,ente):
              valor = True
              break
            else:
              valor = False 
          if valor:
            break
        if not mapa.limite(minion_teste) and not valor:
          self.px = novo_px
          self.py = novo_py 
    def desenha(self,tela):
      if self.vida_atual>0:
        self.vetor_direcao()
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

def main():

   #Inicializando o pygame
   pg.init()
    
   cena_inicial = True
   cena_principal = False
   cena_final = False
    
   #Dados dos minions
   minions = []
   
   #Criando a tela 
   tela = pg.display.set_mode((0,0),pg.FULLSCREEN)

   #Cena Inicial
   escolha_jog1 = False
   escolha_jog2 = False 
   posicao = 0 
   while cena_inicial:
    for event in pg.event.get():
        #Evento de fechar a janela
        if event.type == (pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or (pg.key.get_pressed()[pg.K_ESCAPE]): 
            print("Encerrando o programa.")
            sys.exit()
    titulo = pg.font.SysFont(None,Configuracoes.FONTE_TITULO)
    escolha = pg.font.SysFont(None, Configuracoes.FONTE_MENOR)
    personagens = pg.font.SysFont(None, Configuracoes.FONTE_MENOR)
    Raio = Poder("raio.png")
    Nuvem = Poder("nuvem.png")
    Nikola = Personagem("Nikola Tesla","nikola.png",Raio) 
    Marie = Personagem("Marie Curie","marie.png",Nuvem)
    Titulo = titulo.render(f'Guerra de Cientistas',True,(0,0,0))
    Escolha = escolha.render(f'Escolha um personagem:', True, (0,0,0))
    Personagem1 = personagens.render(f'1) {Nikola.nome}', True, (0,0,0))
    Personagem2 = personagens.render(f'2) {Marie.nome}', True, (0,0,0))
    tela.fill((255, 255, 255))
    PX = Configuracoes.LARGURA_TELA // 2 - Titulo.get_size()[0] // 2
    PY = 0.01 * Configuracoes.ALTURA_TELA
    px = Configuracoes.LARGURA_TELA // 2 - Escolha.get_size()[0] // 2
    py = (0.2 * Configuracoes.ALTURA_TELA // 2) + (Escolha.get_size()[1] * 1.5)
    px_personagens = 0.05*Configuracoes.LARGURA_TELA 
    py1 = (Configuracoes.ALTURA_TELA*0.3) + (Personagem1.get_size()[1] * 1.5)
    py2 = (Configuracoes.ALTURA_TELA*0.4) + (Personagem1.get_size()[1] * 1.5)
    tela.blit(Titulo, (PX,PY))
    tela.blit(Escolha, (px, py))
    tela.blit(Personagem1, (px_personagens, py1))
    tela.blit(Personagem2, (px_personagens, py2))

    if (event.type == pg.KEYDOWN and event.key == pg.K_DOWN):
        if posicao>=0 and posicao<1:
            posicao+=1
        time.sleep(0.1)
        
    elif (event.type == pg.KEYDOWN and event.key == pg.K_UP):
        if posicao>0 and posicao<=1:
            posicao-=1
        time.sleep(0.1)

    if escolha_jog1 == False and event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
        if posicao == 0:
          jogador1 = Jogador(0.1*Configuracoes.LARGURA_TELA,Configuracoes.ALTURA_TELA//2,Nikola)
        if posicao == 1:
          jogador1 = Jogador(0.1*Configuracoes.LARGURA_TELA,Configuracoes.ALTURA_TELA//2,Marie)
        escolha_jog1 = True
        time.sleep(0.2)
    elif escolha_jog1 and event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
        if posicao == 0:
          jogador2 = Jogador(0.9*Configuracoes.LARGURA_TELA,Configuracoes.ALTURA_TELA//2,Nikola)
        if posicao == 1:
          jogador2 = Jogador(0.9*Configuracoes.LARGURA_TELA,Configuracoes.ALTURA_TELA//2,Marie)
        escolha_jog2 = True
        time.sleep(0.2)

    #Escolha dos personagens
    if posicao == 0 and escolha_jog1 == False:
        Personagem1 = personagens.render(f'1) Nikola Tesla  [Jogador 1]', True, (122,122,0))
        tela.blit(Personagem1, (px_personagens, py1))
    elif posicao == 0 and escolha_jog1:
        Personagem1 = personagens.render(f'1) Nikola Tesla  [Jogador 2]', True, (122,122,0))
        tela.blit(Personagem1, (px_personagens, py1))
    if posicao == 1 and escolha_jog1 == False:
        Personagem2 = personagens.render(f'2) Marie Curie [Jogador 1]', True, (122,122,0))
        tela.blit(Personagem2, (px_personagens, py2))
    elif posicao == 1 and escolha_jog1:
        Personagem2 = personagens.render(f'2) Marie Curie [Jogador 2]', True, (122,122,0))
        tela.blit(Personagem2, (px_personagens, py2))

    if escolha_jog1 and escolha_jog2:
        cena_inicial = False
        cena_principal = True
    
    pg.display.flip() 
   
   #Cena Principal
   #Análise de eventos
   tempo = [1,30]
   inicio_cronometro = time.time()
   inicio_minions = time.time()
   inicio_animacao = time.time()
   inicio_morte = 0   
   jogador2.vetorx *=-1
   while cena_principal:
    for event in pg.event.get():
        #Evento de fechar a janela
        if event.type == (pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or (pg.key.get_pressed()[pg.K_ESCAPE]): 
            print("Encerrando o programa.")
            sys.exit()
            
    #Mudar a velocidade dos jogadores
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
    mapa = Mapa()
    mapa.desenha(tela)
    #Pegar uma imagem
    jogador1.desenha(tela)
    jogador2.desenha(tela)
    jogador1.desenha_vida(tela)
    jogador2.desenha_vida(tela)

    #Poder
    if event.type == pg.KEYDOWN and event.key == pg.K_e or (pg.key.get_pressed()[pg.K_e]):
      jogador1.poder.lancar(jogador1)
    if event.type == pg.KEYDOWN and event.key == pg.K_q or (pg.key.get_pressed()[pg.K_q]):
      jogador1.poder.lancar(jogador1)

    if event.type == pg.KEYDOWN and event.key == pg.K_o or (pg.key.get_pressed()[pg.K_o]):
      jogador2.poder.lancar(jogador2)
    if event.type == pg.KEYDOWN and event.key == pg.K_u or (pg.key.get_pressed()[pg.K_u]):
      jogador2.poder.lancar(jogador2)

    fisica = Fisica()
    agora = time.time()

    #Minions

    if agora - inicio_minions > 3 and len(minions) < 5:
      minion = Minions()
      minions.append(minion)
      inicio_minions = agora
    for minion in minions:
      if minion.valor:
          if fisica.contato(minion,jogador1.poder):
            minion.vida_atual -= 1
          if fisica.contato(minion, jogador2.poder):
            minion.vida_atual -= 1
          minion.velocidade(jogador1,jogador2)
          minions_teste = minions[:]
          minions_teste.remove(minion)
          minion.movimento([[jogador1,jogador2],minions_teste])
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

    if fisica.contato(jogador2, jogador1.poder):
      jogador2.vida_atual = jogador2.vida_atual-1
    if fisica.contato(jogador1,jogador2.poder):
      jogador1.vida_atual = jogador1.vida_atual-1

    if agora - inicio_animacao > 0.15: #Velocidade da animacao
      jogador1.frame +=1 
      jogador2.frame +=1
      for minion in minions:
        minion.frame +=1 
      inicio_animacao = agora
        
    cronometro = pg.font.SysFont(None, Configuracoes.FONTE_MENOR)
    Cronometro = cronometro.render(f'{tempo[0]}:{tempo[1]:02d}',True,(0,0,0))
    tamanho_cronometro = Cronometro.get_size()
    largura_cronometro = tamanho_cronometro[0]
    tela.blit(Cronometro, (Configuracoes.LARGURA_TELA /2 - largura_cronometro//2,0.1*Configuracoes.ALTURA_TELA))
    
    if (agora-inicio_cronometro>1):
        tempo[1]-=1
        if tempo[1]<0:
            tempo[1]=59
            tempo[0]-=1
        inicio_cronometro = time.time()
    
    if(tempo[0] == 0 and tempo[1] == 0):
        cena_principal = False
        cena_final = True
    if jogador1.vida_atual<=0 and inicio_morte == 0:
        jogador1.frame = 0
        inicio_morte = time.time()
    if jogador2.vida_atual<=0 and inicio_morte == 0:
        jogador2.frame = 0
        inicio_morte = time.time()
    if inicio_morte!=0 and (agora - inicio_morte) > 3:
          cena_principal = False
          cena_final = True

    #Atualizar a tela
    pg.display.flip()
    #Cena Final 
    while cena_final:
        for event in pg.event.get():
        #Evento de fechar a janela
           if event.type == (pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or (pg.key.get_pressed()[pg.K_ESCAPE]): 
            sys.exit()
        titulo = pg.font.SysFont(None,Configuracoes.FONTE_TITULO)
        subtitulo = pg.font.SysFont(None,Configuracoes.FONTE_MENOR)
        Titulo = titulo.render(f'Guerra de Cientistas',True,(0,0,0))
        if jogador1.vida_atual>0 and jogador2.vida_atual>0:
          Subtitulo = subtitulo.render(f'Empate Técnico',True,(0,0,0))
        elif jogador2.vida_atual<=0:
          Subtitulo = subtitulo.render(f'O Melhor Cientista da Historia: {jogador1.nome} [Jogador 1]', True, (0,0,0))
        else:
          Subtitulo = subtitulo.render(f'O Melhor Cientista da Historia: {jogador2.nome} [Jogador 2]', True, (0,0,0))
        tela.fill((255, 255, 255))
        PX = Configuracoes.LARGURA_TELA // 2 - Titulo.get_size()[0] // 2
        PY = Configuracoes.ALTURA_TELA //2 - Titulo.get_size()[1]
        px = Configuracoes.LARGURA_TELA // 2 - Subtitulo.get_size()[0] // 2
        py = (PY) + (Subtitulo.get_size()[1] * 3)
        tela.blit(Titulo, (PX,PY))
        tela.blit(Subtitulo, (px, py))
        pg.display.flip()

if __name__ == "__main__":
   main() 
