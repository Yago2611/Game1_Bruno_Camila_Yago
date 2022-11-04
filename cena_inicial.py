import pygame as pg
import sys 
import jogador
import configuracoes

class Cena_Inicial:
  def __init__(self,tela):
    self.tela = tela
    font_titulo = pg.font.SysFont(None, 12)
    self.titulo = font_titulo.render(f'Escolha um personagem', True, (0,0,0))
    self.encerrar = False
    self.escolha_jog1 = False
    self.escolha_jog2 = False 
 
def rodar(self):
  while not self.encerrar:
    self.tratamento_de_eventos()
    self.atualiza_estado()
    self.desenha()

def tratamento_de_eventos(self):
  for event in pg.event.get():
        #Evento de fechar a janela
        if event.type == (pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or (pg.key.get_pressed()[pg.K_ESCAPE]): 
          sys.exit()
        if (event.type == pg.KEYDOWN and event.key == pg.K_DOWN):
          if posicao>=0 and posicao<Configuracoes.NUM_PERSONAGENS-1:
            posicao+=1
            time.sleep(0.1)
        elif (event.type == pg.KEYDOWN and event.key == pg.K_UP):
          if posicao>0 and posicao<=Configuracoes.NUM_PERSONAGENS:
            posicao-=1
            time.sleep(0.1)

    if escolha_jog1 == False and event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
        escolha_jog1 = True
        time.sleep(0.2)
    elif escolha_jog1 and event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
        escolha_jog2 = True
        time.sleep(0.2)

def atualiza_estado(self):
  pass

def desenha(self):
  pass

  
    
   
