import pygame as pg

class Configuracoes:
  TELA = pg.display.set_mode((1280,768),pg.FULLSCREEN)  
  LARGURA_TELA,ALTURA_TELA = TELA.get_size()
  FONTE_TITULO = 96
  FONTE_MENOR = 48
  VELOCIDADE = 1
  P1X,P1Y = (0.3*LARGURA_TELA,ALTURA_TELA//2 - 20)
  P2X,P2Y = (0.7*LARGURA_TELA,ALTURA_TELA//2 - 20)
