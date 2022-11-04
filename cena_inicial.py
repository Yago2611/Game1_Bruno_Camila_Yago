import pygame as pg
import sys 
import jogador
import configuracoes

class Cena_Inicial:
  def __init__(self,tela):
    self.tela = tela
    #Variaveis booleanas
    self.encerrar = False
    self.escolha_jog1 = False
    self.escolha_jog2 = False         
    #Criando os personagens
    self.personagem_1 = Personagem("Nikola Tesla",Raio,Luz,"Nikola.png",Configuracoes.VIDA)
    font_titulo = pg.font.SysFont(None, 12)
    self.titulo = font_titulo.render(f'Escolha um personagem', True, (0,0,0))
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
  if self.escolha_jog1 and self.escolha_jog2:
    self.encerrar = True 
    
def desenha(self):
  tela.fill((255, 255, 255))
  tela.blit(Titulo, (PX,PY))
    tela.blit(Escolha, (px, py))
    tela.blit(Personagem1, (px_personagens, py1))
    tela.blit(Personagem2, (px_personagens, py2))
  pg.display.flip() 

  
    
   
