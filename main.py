import pygame as pg 
import sys 

#Definindo as Configuracoes do jogo
LARGURA_TELA = 1200 
ALTURA_TELA = 600
ALTURA_JOGADOR = 50
LARGURA_JOGADOR = 10
VELOCIDADE = 1 

def main():
   #Dados dos jogadores
   P1_X = 0.1*LARGURA_TELA
   P1_Y = ALTURA_TELA//2 - ALTURA_JOGADOR//2
   P2_X = 0.9*LARGURA_TELA-LARGURA_JOGADOR
   P2_Y = ALTURA_TELA//2 - ALTURA_JOGADOR//2

   #Inicializando o pygame
   pg.init()
   
   #Criando a tela 
   tela = pg.display.set_mode((LARGURA_TELA, ALTURA_TELA))

   #Análise de eventos
   while True:
    for event in pg.event.get():
        #Evento de fechar a janela
        if event.type == (pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or (pg.key.get_pressed()[pg.K_ESCAPE]): 
            print("Encerrando o programa.")
            sys.exit()
            
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
    if (Novo_P1_X<=(LARGURA_TELA-LARGURA_JOGADOR)) and (Novo_P1_X>=0):
      P1_X = Novo_P1_X
    Novo_P2_X = P2_X + P2_VX
    if (Novo_P2_X<=(LARGURA_TELA-LARGURA_JOGADOR)) and (Novo_P2_X>=0):
      P2_X = Novo_P2_X
    Novo_P1_Y = P1_Y + P1_VY
    if (Novo_P1_Y<=(ALTURA_TELA-ALTURA_JOGADOR)) and (Novo_P1_Y>=0):
      P1_Y = Novo_P1_Y
    Novo_P2_Y = P2_Y + P2_VY
    if (Novo_P2_Y<=(ALTURA_TELA-ALTURA_JOGADOR)) and (Novo_P2_Y>=0):
      P2_Y = Novo_P2_Y
    
    #Desenhar a tela
    tela.fill((0, 122, 0))
    #Desenha os jogadores
    pg.draw.rect(tela,(0, 0, 0),(P1_X, P1_Y, 10, 50),0)
    pg.draw.rect(tela,(0, 0, 0),(P2_X,P2_Y, 10, 50),0)
    #Atualizar a tela
    pg.display.flip()


if __name__ == "__main__":
   main() 
