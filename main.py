import pygame as pg 
import sys 
import time
from configuracoes import Configuracoes
from cronometro import Cronometro 
from estado_jogo import Estado_jogo
from fisica import Fisica 
from mapa import Mapa
from poder import Poder
from personagem import Personagem
from jogador import Jogador 
from cena_final import Cena_final
    
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
   estado_jogo = Estado_jogo(time.time())
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
