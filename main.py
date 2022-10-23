import pygame as pg 
import sys 

#Definindo as Configuracoes do jogo
LARGURA_TELA = 1200 
ALTURA_TELA = 600

def main():
   #Inicializando o pygame
   pg.init()
   
   #Criando a tela 
   tela = pg.display.set_mode((LARGURA_TELA, ALTURA_TELA))

   #Análise de eventos
   while True:
    for event in pg.event.get():
        #Evento de fechar a janela
        if event.type == pg.QUIT: 
            print("Encerrando o programa.")
            sys.exit()
            
    #Desenhar a tela
    tela.fill((0, 122, 0))
    #Atualizar a tela
    pg.display.flip()


if __name__ == "__main__":
   main() 
