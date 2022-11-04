import PERSONAGENS

class Cena_Principal:
  def __init__(self, tela):
    self.tela = tela
  
  def rodar(self):
    while True:
      self.load_image()
