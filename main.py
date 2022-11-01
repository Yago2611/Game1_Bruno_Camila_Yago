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

#Definindo as Configuracoes do jogo
LARGURA_TELA = 1200 
ALTURA_TELA = 600
FONTE_TITULO = 96
FONTE_MAIOR = 48
FONTE_MENOR = 48
VELOCIDADE = 3

def main():

   #Inicializando o pygame
   pg.init()
    
   cena_inicial = True
   cena_principal = False 

   #Dados dos jogadores
   P1_X = 0.1*LARGURA_TELA
   P1_Y = ALTURA_TELA//2 
   P2_X = 0.9*LARGURA_TELA
   P2_Y = ALTURA_TELA//2 
   px_bloco = LARGURA_TELA
   py_bloco = ALTURA_TELA
   v_bloco = 0 
    
   #Dados dos minions
   px_minion = LARGURA_TELA//2
   py_minion = ALTURA_TELA//2
   minion = True
   largura_minion = 20
   altura_minion = 50
   tempo_referencia = 0
   
   #Criando a tela 
   tela = pg.display.set_mode((LARGURA_TELA, ALTURA_TELA))

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
   while cena_principal:
    for event in pg.event.get():
        #Evento de fechar a janela
        if event.type == (pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or (pg.key.get_pressed()[pg.K_ESCAPE]): 
            print("Encerrando o programa.")
            sys.exit()

    imagem = load_image('nikola1.png', scale=1)
    imagem2 = load_image('marie1.png', scale=1)
    imagem_raio = load_image('raio.png',scale=0.1)
    rect = imagem.get_rect()
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
    """tela.fill((255, 255, 255))
    pg.draw.rect(tela,(0, 0, 255),(0.025*LARGURA_TELA, 0.05*ALTURA_TELA, 0.95*LARGURA_TELA, 0.9*ALTURA_TELA),0)"""
    tela.fill((0, 0, 255))
    pg.draw.rect(tela,(0, 255, 0),(0.05*LARGURA_TELA, 0.1*ALTURA_TELA, 0.9*LARGURA_TELA, 0.8*ALTURA_TELA),0)
    #Pegar uma imagem
    tela.blit(imagem, (P1_X,P1_Y))
    tela.blit(imagem2, (P2_X,P2_Y))
    #Desenha os jogadores
    
    #Minions
    if minion:
        tela.blit(imagem, (px_minion,py_minion))
    
    #Velocidade
    vx_minion = P1_X - px_minion
    vy_minion = P1_Y - py_minion 
    velocidade_minion = ((vx_minion**2 + vy_minion**2)**0.5)*4
    if (velocidade_minion!=0):
        vx_minion/=velocidade_minion
        vy_minion/=velocidade_minion
    px_minion += vx_minion
    py_minion += vy_minion


    #Poder
    if event.type == pg.KEYDOWN and event.key == pg.K_e or (pg.key.get_pressed()[pg.K_e]):
      px_bloco = P1_X
      py_bloco = P1_Y
      v_bloco = 1
    if event.type == pg.KEYDOWN and event.key == pg.K_q or (pg.key.get_pressed()[pg.K_q]):
      px_bloco = P1_X
      py_bloco = P1_Y
      v_bloco = -1

    tela.blit(imagem_raio, (px_bloco,py_bloco))
    px_bloco += v_bloco
    px_bloco += v_bloco

    tamanho = imagem_raio.get_rect()
    largura_bloco = tamanho.width
    altura_bloco = tamanho.height

    if (px_bloco+altura_bloco>=px_minion and px_bloco<=px_minion+largura_minion) and (py_bloco+largura_bloco>=py_minion and py_bloco<=py_minion+altura_minion):
        minion = False
        tempo_referencia = time.localtime()[5]

    tempo_atual = time.localtime()[5]
    if tempo_referencia>0:
        tempo_passado = tempo_atual - tempo_referencia
    if tempo_referencia>0 and tempo_passado > 2:
        minion = True

    #Atualizar a tela
    pg.display.flip()


if __name__ == "__main__":
   main() 
