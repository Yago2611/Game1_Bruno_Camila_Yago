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

class Personagem:
   def __init__(self, nome, imagem, poder):
    self.nome = nome
    self.imagem = imagem
    self.poder = poder

class Configuracoes:   
    #Definindo as Configuracoes do jogo
    TELA = pg.display.set_mode()  
    LARGURA_TELA,ALTURA_TELA = TELA.get_size()
    FONTE_TITULO = 96
    FONTE_MAIOR = 48
    FONTE_MENOR = 48
    VELOCIDADE = 5
    nikola_tesla = Personagem("Nikola Tesla", "nikola.png", raios)
    marie_curie = Personagem("Marie Curie", "marie.png", nuvem)

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
          jogador1 = Jogador(0.1*LARGURA_TELA,ALTURA_TELA//2,nikola_tesla)
        if posicao == 1:
          jogador1 = Jogador(0.1*LARGURA_TELA,ALTURA_TELA//2,marie_curie)
        escolha_jog1 = True
        time.sleep(0.2)
    elif escolha_jog1 and event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
        if posicao == 0:
          jogador2 = Jogador(0.9*LARGURA_TELA,ALTURA_TELA//2,nikola_tesla)
        if posicao == 1:
          jogador2 = Jogador(0.9*LARGURA_TELA,ALTURA_TELA//2,marie_curie)
        escolha_jog2 = True
        time.sleep(0.2)

    

def main():

   #Inicializando o pygame
   pg.init()
    
   cena_inicial = True
   cena_principal = False
   cena_final = False

   #Dados dos jogadores
   P1_X = 0.1*LARGURA_TELA
   P1_Y = ALTURA_TELA//2 
   P2_X = 0.9*LARGURA_TELA
   P2_Y = ALTURA_TELA//2 
   px_raio = LARGURA_TELA
   py_raio = ALTURA_TELA
   v_raio = 0 
   px_nuvem = LARGURA_TELA
   py_nuvem = ALTURA_TELA
   v_nuvem = 0 
    
   #Dados dos minions
   px_minion = LARGURA_TELA//2
   py_minion = ALTURA_TELA//2
   minion = True
   largura_minion = 20
   altura_minion = 50
   tempo_referencia = 0
   
   #Criando a tela 
   tela = pg.display.set_mode((LARGURA_TELA, ALTURA_TELA)pg.FULLSCREEN)

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
    titulo = pg.font.SysFont(None,FONTE_TITULO)
    escolha = pg.font.SysFont(None, FONTE_MAIOR)
    personagens = pg.font.SysFont(None, FONTE_MENOR)
    Titulo = titulo.render(f'Guerra de Cientistas',True,(0,0,0))
    Escolha = escolha.render(f'Escolha um personagem:', True, (0,0,0))
    Personagem1 = personagens.render(f'1) Nikola Tesla', True, (0,0,0))
    Personagem2 = personagens.render(f'2) Marie Curie', True, (0,0,0))
    tela.fill((255, 255, 255))
    PX = LARGURA_TELA // 2 - Titulo.get_size()[0] // 2
    PY = 0.01 * ALTURA_TELA
    px = LARGURA_TELA // 2 - Escolha.get_size()[0] // 2
    py = (0.2 * ALTURA_TELA // 2) + (Escolha.get_size()[1] * 1.5)
    px_personagens = 0.05*LARGURA_TELA 
    py1 = (ALTURA_TELA*0.3) + (Personagem1.get_size()[1] * 1.5)
    py2 = (ALTURA_TELA*0.4) + (Personagem1.get_size()[1] * 1.5)
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
        escolha_jog1 = True
        time.sleep(0.2)
    elif escolha_jog1 and event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
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
   comeco = time.time()
   while cena_principal:
    for event in pg.event.get():
        #Evento de fechar a janela
        if event.type == (pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or (pg.key.get_pressed()[pg.K_ESCAPE]): 
            print("Encerrando o programa.")
            sys.exit()
    imagem1 = load_image('nikola.png', scale=1)
    imagem2 = load_image('marie.png', scale=1)
    imagem_minion = load_image('minion.png', scale=1)
    imagem_raio = load_image('raio.png',scale=0.1)
    imagem_nuvem = load_image('nuvem.png',scale=0.1)
    rect = imagem1.get_rect()
    LARGURA_JOGADOR = rect.width
    ALTURA_JOGADOR = rect.height
            
    #Mudar a velocidade dos jogadores
    if (event.type == pg.KEYDOWN and event.key == pg.K_d) or (pg.key.get_pressed()[pg.K_d]):
      P1_VX = VELOCIDADE
    elif (event.type == pg.KEYDOWN and event.key == pg.K_a) or (pg.key.get_pressed()[pg.K_a]):
      P1_VX = -VELOCIDADE
    else:
      P1_VX = 0 
    if (event.type == pg.KEYDOWN and event.key == pg.K_l) or (pg.key.get_pressed()[pg.K_l]):
      P2_VX = VELOCIDADE
    elif (event.type == pg.KEYDOWN and event.key == pg.K_j) or (pg.key.get_pressed()[pg.K_j]):
      P2_VX = -VELOCIDADE
    else:
      P2_VX = 0 
    if (event.type == pg.KEYDOWN and event.key == pg.K_s) or (pg.key.get_pressed()[pg.K_s]):
      P1_VY = VELOCIDADE
    elif (event.type == pg.KEYDOWN and event.key == pg.K_w) or (pg.key.get_pressed()[pg.K_w]):
      P1_VY = -VELOCIDADE
    else:
      P1_VY = 0 
    if (event.type == pg.KEYDOWN and event.key == pg.K_k) or (pg.key.get_pressed()[pg.K_k]):
      P2_VY = VELOCIDADE
    elif (event.type == pg.KEYDOWN and event.key == pg.K_i) or (pg.key.get_pressed()[pg.K_i]):
      P2_VY = -VELOCIDADE
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
    if (Novo_P1_X<=(0.95*(LARGURA_TELA)-LARGURA_JOGADOR)) and (Novo_P1_X>=0.05*LARGURA_TELA):
      P1_X = Novo_P1_X
    Novo_P2_X = P2_X + P2_VX
    if (Novo_P2_X<=(0.95*(LARGURA_TELA)-LARGURA_JOGADOR)) and (Novo_P2_X>=0.05*LARGURA_TELA):
      P2_X = Novo_P2_X
    Novo_P1_Y = P1_Y + P1_VY
    if (Novo_P1_Y<=(0.9*(ALTURA_TELA)-ALTURA_JOGADOR)) and (Novo_P1_Y>=0.1*ALTURA_TELA):
      P1_Y = Novo_P1_Y
    Novo_P2_Y = P2_Y + P2_VY
    if (Novo_P2_Y<=(0.9*(ALTURA_TELA)-ALTURA_JOGADOR)) and (Novo_P2_Y>=0.1*ALTURA_TELA):
      P2_Y = Novo_P2_Y
    
    #Desenhar a tela
    tela.fill((0, 0, 255))
    pg.draw.rect(tela,(0, 255, 0),(0.05*LARGURA_TELA, 0.1*ALTURA_TELA, 0.9*LARGURA_TELA, 0.8*ALTURA_TELA),0)
    #Pegar uma imagem
    tela.blit(imagem1, (P1_X,P1_Y))
    tela.blit(imagem2, (P2_X,P2_Y))
    #Desenha os jogadores
    
    #Minions
    if minion:
        tela.blit(imagem_minion, (px_minion,py_minion))
    
    #Velocidade
    vx_minion = P1_X - px_minion
    vy_minion = P1_Y - py_minion 
    velocidade_minion = ((vx_minion**2 + vy_minion**2)**0.5)/2
    if (velocidade_minion!=0):
        vx_minion/=velocidade_minion
        vy_minion/=velocidade_minion
    px_minion += vx_minion
    py_minion += vy_minion


    #Poder
    if event.type == pg.KEYDOWN and event.key == pg.K_e or (pg.key.get_pressed()[pg.K_e]):
      px_raio = P1_X
      py_raio = P1_Y
      v_raio = VELOCIDADE
    if event.type == pg.KEYDOWN and event.key == pg.K_q or (pg.key.get_pressed()[pg.K_q]):
      px_raio = P1_X
      py_raio = P1_Y
      v_raio = -VELOCIDADE

    if event.type == pg.KEYDOWN and event.key == pg.K_o or (pg.key.get_pressed()[pg.K_o]):
      px_nuvem = P2_X
      py_nuvem = P2_Y
      v_nuvem = VELOCIDADE
    if event.type == pg.KEYDOWN and event.key == pg.K_u or (pg.key.get_pressed()[pg.K_u]):
      px_nuvem = P2_X
      py_nuvem = P2_Y
      v_nuvem = -VELOCIDADE

    tela.blit(imagem_raio, (px_raio,py_raio))
    px_raio += v_raio
    px_raio += v_raio

    tamanho = imagem_raio.get_rect()
    largura_raio = tamanho.width
    altura_raio = tamanho.height

    tela.blit(imagem_nuvem, (px_nuvem,py_nuvem))
    px_nuvem += v_nuvem
    px_nuvem += v_nuvem

    tamanho2 = imagem_nuvem.get_rect()
    largura_nuvem = tamanho2.width
    altura_nuvem = tamanho2.height

    if (px_raio+altura_raio>=px_minion and px_raio<=px_minion+largura_minion) and (py_raio+largura_raio>=py_minion and py_raio<=py_minion+altura_minion):
        minion = False
        tempo_referencia = time.time()
    
    if (px_nuvem+altura_nuvem>=px_minion and px_nuvem<=px_minion+largura_minion) and (py_nuvem+largura_nuvem>=py_minion and py_nuvem<=py_minion+altura_minion):
        minion = False
        tempo_referencia = time.time()

    tempo_atual = time.time()
    agora = time.time()
    if tempo_referencia>0:
        tempo_passado = tempo_atual - tempo_referencia
    if tempo_referencia>0 and tempo_passado > 2:
        minion = True
        
    cronometro = pg.font.SysFont(None, FONTE_MAIOR)
    Cronometro = cronometro.render(f'{tempo[0]}:{tempo[1]:02d}',True,(0,0,0))
    tamanho_cronometro = Cronometro.get_size()
    largura_cronometro = tamanho_cronometro[0]
    tela.blit(Cronometro, (LARGURA_TELA//2 - largura_cronometro//2,0.1*ALTURA_TELA))
    
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
        titulo = pg.font.SysFont(None,FONTE_TITULO)
        subtitulo = pg.font.SysFont(None,FONTE_MENOR)
        Titulo = titulo.render(f'Guerra de Cientistas',True,(0,0,0))
        Subtitulo = subtitulo.render(f'Obrigado por Jogar!', True, (0,0,0))
        tela.fill((255, 255, 255))
        PX = LARGURA_TELA // 2 - Titulo.get_size()[0] // 2
        PY = ALTURA_TELA //2 - Titulo.get_size()[1]
        px = LARGURA_TELA // 2 - Subtitulo.get_size()[0] // 2
        py = (PY) + (Subtitulo.get_size()[1] * 2)
        tela.blit(Titulo, (PX,PY))
        tela.blit(Subtitulo, (px, py))
        pg.display.flip()

if __name__ == "__main__":
   main() 
