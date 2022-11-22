import pygame as pg
import time
from configuracoes import Configuracoes

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