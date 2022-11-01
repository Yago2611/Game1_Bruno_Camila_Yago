import pygame as pg
import sys 

class Cena_Inicial:
  def __init__(self,tela):
    self.tela = tela
    font_titulo = pg.font.SysFont(None, 12)
    self.titulo = font_titulo.render(f'Escolha um personagem', True, (0,0,0))
  def 
