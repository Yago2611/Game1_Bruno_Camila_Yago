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

class Poder: 
    def __init__(self,imagem):
        self.imagem = load_image(imagem, scale=0.1)
        self.valor = False
        self.px = 0 
        self.py = 0
        self.largura = self.imagem.get_rect().width
        self.altura = self.imagem.get_rect().height
        self.vx = Configuracoes.VELOCIDADE
        self.vy = 0 
    def lancar (self,jogador):
        self.valor = True
        self.px = jogador.px
        self.py = jogador.py 
    def movimento(self):
        self.px+=self.vx
        self.py+=self.vy
    def desenha (self,tela):
        tela.blit(self.imagem,(self.px,self.py))

class Personagem:
   def __init__(self, nome, imagem, poder):
    self.nome = nome
    self.imagem = imagem
    self.poder = poder
    self.vida = 100
    
class Jogador:  
    def __init__ (self,px,py,personagem):
      self.py = py
      self.px = px 
      self.poder = personagem.poder
      self.personagem = personagem #O jogador ira receber um objeto da classe personagem
      self.vida = personagem.vida
      self.vx = 0
      self.vy = 0
      self.vida_atual = 100
      self.vida_maxima = 200
      self.comprimento_barra_vida = 50
      self.razao_vida = self.vida_maxima / self.comprimento_barra_vida
    def vida(self):
        pg.draw.rect(Configuracoes.TELA, (255,0,0), (self.px,self.py-20,self.vida_atual/self.razao_vida,10))
        pg.draw.rect(Configuracoes.TELA, (255,255,255),(self.px,self.py-20,self.comprimento_barra_vida,10),2)    

class Configuracoes:   
    #Definindo as Configuracoes do jogo
    TELA = pg.display.set_mode()  
    LARGURA_TELA,ALTURA_TELA = TELA.get_size()
    FONTE_TITULO = 96
    FONTE_MAIOR = 48
    FONTE_MENOR = 48
    VELOCIDADE = 5
    raios = Poder("raio.png")
    nuvem = Poder("nuvem.png")
    nikola_tesla = Personagem("Nikola Tesla", "nikola.png", raios)
    marie_curie = Personagem("Marie Curie", "marie.png", nuvem)

class Minions:
    def __init__(self):
        self.valor = True
        self.px = Configuracoes.LARGURA_TELA//2
        self.py = Configuracoes.ALTURA_TELA//2
        self.vx = 0
        self.vy = 0 
        self.vida = 100
        self.imagem = load_image('minion.png', scale=1)
        self.largura = self.imagem.get_rect().width
        self.altura = self.imagem.get_rect().height
        self.vel = 0 
    def velocidade(self,jogador1,jogador2):
        if (((jogador1.px-self.px)**2 + (jogador1.py-self.py)**2)**0.5) > (((jogador2.px-self.px)**2 + (jogador2.py-self.py)**2)**0.5): #Comparamos a distancia com os jogadores
            self.vx = jogador1.px - self.px
            self.vy = jogador1.py - self.py
        else:
            self.vx = jogador2.px - self.px
            self.vy = jogador2.py - self.py
        self.vel = ((self.vx**2 + self.vy**2)**0.5)/2 #Encontramos o modulo do vetor velocidade
        self.vx /= self.vel
        self.vy /= self.vel #Formamos os vetores unitarios
    def movimento(self):
        self.px += self.vx
        self.py += self.vy 
    def desenha(self,tela):
        tela.blit(self.imagem, (self.px,self.py))
        

def main():

   #Inicializando o pygame
   pg.init()
    
   cena_inicial = True
   cena_principal = False
   cena_final = False

   #Dados dos jogadores
   P1_X = 0.1*Configuracoes.LARGURA_TELA
   P1_Y = Configuracoes.ALTURA_TELA//2 
   P2_X = 0.9*Configuracoes.LARGURA_TELA
   P2_Y = Configuracoes.ALTURA_TELA//2 
    
   #Dados dos minions
   minion = Minions()
   tempo_referencia = 0
   
   #Criando a tela 
   tela = pg.display.set_mode((Configuracoes.LARGURA_TELA, Configuracoes.ALTURA_TELA),pg.FULLSCREEN)

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
    escolha = pg.font.SysFont(None, Configuracoes.FONTE_MAIOR)
    personagens = pg.font.SysFont(None, Configuracoes.FONTE_MENOR)
    Titulo = titulo.render(f'Guerra de Cientistas',True,(0,0,0))
    Escolha = escolha.render(f'Escolha um personagem:', True, (0,0,0))
    Personagem1 = personagens.render(f'1) Nikola Tesla', True, (0,0,0))
    Personagem2 = personagens.render(f'2) Marie Curie', True, (0,0,0))
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
          jogador1 = Jogador(0.1*Configuracoes.LARGURA_TELA,Configuracoes.ALTURA_TELA//2,Configuracoes.nikola_tesla)
        if posicao == 1:
          jogador1 = Jogador(0.1*Configuracoes.LARGURA_TELA,Configuracoes.ALTURA_TELA//2,Configuracoes.marie_curie)
        escolha_jog1 = True
        time.sleep(0.2)
    elif escolha_jog1 and event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
        if posicao == 0:
          jogador2 = Jogador(0.9*Configuracoes.LARGURA_TELA,Configuracoes.ALTURA_TELA//2,Configuracoes.nikola_tesla)
        if posicao == 1:
          jogador2 = Jogador(0.9*Configuracoes.LARGURA_TELA,Configuracoes.ALTURA_TELA//2,Configuracoes.marie_curie)
        escolha_jog2 = True
        time.sleep(0.2)


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
   comeco = time.time()
   while cena_principal:
    for event in pg.event.get():
        #Evento de fechar a janela
        if event.type == (pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or (pg.key.get_pressed()[pg.K_ESCAPE]): 
            print("Encerrando o programa.")
            sys.exit()
    imagem1 = load_image('nikola.png', scale=1)
    imagem2 = load_image('marie.png', scale=1)
    rect = imagem1.get_rect()
    LARGURA_JOGADOR = rect.width
    ALTURA_JOGADOR = rect.height
            
    #Mudar a velocidade dos jogadores
    if (event.type == pg.KEYDOWN and event.key == pg.K_d) or (pg.key.get_pressed()[pg.K_d]):
      P1_VX = Configuracoes.VELOCIDADE
    elif (event.type == pg.KEYDOWN and event.key == pg.K_a) or (pg.key.get_pressed()[pg.K_a]):
      P1_VX = -Configuracoes.VELOCIDADE
    else:
      P1_VX = 0 
    if (event.type == pg.KEYDOWN and event.key == pg.K_l) or (pg.key.get_pressed()[pg.K_l]):
      P2_VX = Configuracoes.VELOCIDADE
    elif (event.type == pg.KEYDOWN and event.key == pg.K_j) or (pg.key.get_pressed()[pg.K_j]):
      P2_VX = -Configuracoes.VELOCIDADE
    else:
      P2_VX = 0 
    if (event.type == pg.KEYDOWN and event.key == pg.K_s) or (pg.key.get_pressed()[pg.K_s]):
      P1_VY = Configuracoes.VELOCIDADE
    elif (event.type == pg.KEYDOWN and event.key == pg.K_w) or (pg.key.get_pressed()[pg.K_w]):
      P1_VY = -Configuracoes.VELOCIDADE
    else:
      P1_VY = 0 
    if (event.type == pg.KEYDOWN and event.key == pg.K_k) or (pg.key.get_pressed()[pg.K_k]):
      P2_VY = Configuracoes.VELOCIDADE
    elif (event.type == pg.KEYDOWN and event.key == pg.K_i) or (pg.key.get_pressed()[pg.K_i]):
      P2_VY = -Configuracoes.VELOCIDADE
    else:
      P2_VY = 0 
    if (P1_VX!=0) and (P1_VY!=0):
      P1_VY *= (2**0.5)/2
      P1_VX *= (2**0.5)/2
    if (P2_VX!=0) and (P2_VY!=0):
      P2_VY *= (2**0.5)/2
      P2_VX *= (2**0.5)/2
    #Mudar a posicao dos jogadores
    Novo_P1_X = P1_X + P1_VX
    if (Novo_P1_X<=(0.95*(Configuracoes.LARGURA_TELA)-LARGURA_JOGADOR)) and (Novo_P1_X>=0.05*Configuracoes.LARGURA_TELA):
      P1_X = Novo_P1_X
    Novo_P2_X = P2_X + P2_VX
    if (Novo_P2_X<=(0.95*(Configuracoes.LARGURA_TELA)-LARGURA_JOGADOR)) and (Novo_P2_X>=0.05*Configuracoes.LARGURA_TELA):
      P2_X = Novo_P2_X
    Novo_P1_Y = P1_Y + P1_VY
    if (Novo_P1_Y<=(0.9*(Configuracoes.ALTURA_TELA)-ALTURA_JOGADOR)) and (Novo_P1_Y>=0.1*Configuracoes.ALTURA_TELA):
      P1_Y = Novo_P1_Y
    Novo_P2_Y = P2_Y + P2_VY
    if (Novo_P2_Y<=(0.9*(Configuracoes.ALTURA_TELA)-ALTURA_JOGADOR)) and (Novo_P2_Y>=0.1*Configuracoes.ALTURA_TELA):
      P2_Y = Novo_P2_Y
    
    #Desenhar a tela
    tela.fill((0, 0, 255))
    pg.draw.rect(tela,(0, 255, 0),(0.05*Configuracoes.LARGURA_TELA, 0.1*Configuracoes.ALTURA_TELA, 0.9*Configuracoes.LARGURA_TELA, 0.8*Configuracoes.ALTURA_TELA),0)
    #Pegar uma imagem
    tela.blit(imagem1, (P1_X,P1_Y))
    tela.blit(imagem2, (P2_X,P2_Y))
    #Desenha os jogadores
    vida_atual = 100
    vida_maxima = 200
    comprimento_barra_vida = 50
    razao_vida = vida_maxima / comprimento_barra_vida

    pg.draw.rect(tela, (255,0,0), (Novo_P1_X,Novo_P1_Y-20,vida_atual/razao_vida,10))
    pg.draw.rect(tela, (255,255,255),(Novo_P1_X,Novo_P1_Y-20,comprimento_barra_vida,10),2)
    #Minions
    if minion.valor:
        minion.velocidade(jogador1,jogador2)
        minion.movimento()
        minion.desenha(tela)


    #Poder
    if event.type == pg.KEYDOWN and event.key == pg.K_e or (pg.key.get_pressed()[pg.K_e]):
      jogador1.poder.lancar(jogador1)
    if event.type == pg.KEYDOWN and event.key == pg.K_q or (pg.key.get_pressed()[pg.K_q]):
      jogador1.poder.lancar(jogador1)
    if event.type == pg.KEYDOWN and event.key == pg.K_o or (pg.key.get_pressed()[pg.K_o]):
      jogador2.poder.lancar(jogador2)
    if event.type == pg.KEYDOWN and event.key == pg.K_u or (pg.key.get_pressed()[pg.K_u]):
      jogador2.poder.lancar(jogador2)

    if jogador1.poder.valor == True: 
        jogador1.poder.movimento()
        jogador1.poder.desenha(tela)
    if jogador2.poder.valor == True:
        jogador2.poder.movimento()
        jogador2.poder.desenha(tela)

    if (jogador1.poder.px+jogador1.poder.largura>=minion.px and jogador1.poder.px<=minion.px+minion.largura) and (jogador1.poder.py+jogador1.poder.altura>=minion.py and jogador1.poder.py<=minion.py+minion.altura):
        minion.valor = False
        tempo_referencia = time.time()
    
    if (jogador2.poder.px+jogador2.poder.largura>=minion.px and jogador2.poder.px<=minion.px+minion.largura) and (jogador2.poder.py+jogador2.poder.altura>=minion.py and jogador2.poder.py<=minion.py+minion.altura):
        minion.valor = False
        tempo_referencia = time.time()

    tempo_atual = time.time()
    agora = time.time()
    if tempo_referencia>0:
        tempo_passado = tempo_atual - tempo_referencia
    if tempo_referencia>0 and tempo_passado > 2:
        minion.valor = True
        
    cronometro = pg.font.SysFont(None, Configuracoes.FONTE_MAIOR)
    Cronometro = cronometro.render(f'{tempo[0]}:{tempo[1]:02d}',True,(0,0,0))
    tamanho_cronometro = Cronometro.get_size()
    largura_cronometro = tamanho_cronometro[0]
    tela.blit(Cronometro, (Configuracoes.LARGURA_TELA//2 - largura_cronometro//2,0.1*Configuracoes.ALTURA_TELA))
    
    if (agora-comeco>1):
        tempo[1]-=1
        if tempo[1]<0:
            tempo[1]=59
            tempo[0]-=1
        comeco = time.time()
    
    if(tempo[0] == 0 and tempo[1] == 0):
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
        Subtitulo = subtitulo.render(f'Obrigado por Jogar!', True, (0,0,0))
        tela.fill((255, 255, 255))
        PX = Configuracoes.LARGURA_TELA // 2 - Titulo.get_size()[0] // 2
        PY = Configuracoes.ALTURA_TELA //2 - Titulo.get_size()[1]
        px = Configuracoes.LARGURA_TELA // 2 - Subtitulo.get_size()[0] // 2
        py = (PY) + (Subtitulo.get_size()[1] * 2)
        tela.blit(Titulo, (PX,PY))
        tela.blit(Subtitulo, (px, py))
        pg.display.flip()

if __name__ == "__main__":
   main() 
