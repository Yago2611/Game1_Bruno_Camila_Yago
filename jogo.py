import pygame as pg
from cena_inicial import Cena_inicial
from cena_principal import Cena_principal
from cena_final import Cena_final

class Jogo:
  def __init__(self):
        pg.init()
  def rodar(self):
   cena_inicial = Cena_inicial()
   cena_inicial.rodar()
   cena_principal = Cena_principal(cena_inicial)
   cena_principal.rodar()
   cena_final = Cena_final(cena_principal)
   cena_final.rodar()
