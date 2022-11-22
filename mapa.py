from configuracoes import Configuracoes
from imagens import Imagens

class Mapa:
    def __init__(self):
      self.terra_plana = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,0,0,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,0,0,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,2,2,2,1,1,1,0,0,1,1,1,2,2,2,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,0,0,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,0,0,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,1,2,2,2,1,1,1,0,0,1,1,1,2,2,2,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,0,0,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,0,0,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    def limite(self,corpo):
      if corpo.px+corpo.largura>Configuracoes.LARGURA_TELA or corpo.py+corpo.altura> Configuracoes.ALTURA_TELA or corpo.px < 0 or corpo.py <0:
        return True
      x = int(corpo.px//32)
      y = int(corpo.py//32) 
      x2 = int((corpo.px + corpo.largura)//32)
      y2 = int((corpo.py + corpo.altura)//32)
      if self.terra_plana[y][x] == 2 or self.terra_plana[y][x2] == 2 or self.terra_plana[y2][x] == 2 or self.terra_plana[y2][x2] == 2:
        return True
      else: 
        return False
    def dano(self,corpo):
      x = int(corpo.px//32)
      y = int(corpo.py//32) 
      x2 = int((corpo.px + corpo.largura)//32)
      y2 = int((corpo.py + corpo.altura)//32)
      if self.terra_plana[y][x] == 0 or self.terra_plana[y][x2] == 0 or self.terra_plana[y2][x] == 0 or self.terra_plana[y2][x2] == 0:
        corpo.vida_atual -= 0.1
    def quebrar(self,corpo):
      x = int(corpo.px//32)
      y = int(corpo.py//32) 
      x2 = int((corpo.px + corpo.largura)//32)
      y2 = int((corpo.py + corpo.altura)//32)
      if self.terra_plana[y][x] == 3 and x in [18,21]:
        self.terra_plana[y][x] = 1
      elif x in [19,20]:
        self.terra_plana[y][x] = 0
      if self.terra_plana[y][x2] == 3 and x2 in [18,21]:
        self.terra_plana[y][x2] = 1
      elif x2 in [19,20]:
        self.terra_plana[y][x2] = 0
      if self.terra_plana[y2][x] == 3 and x in [18,21]:
        self.terra_plana[y2][x] = 1
      elif x in [19,20]:
        self.terra_plana[y2][x] = 0
      if self.terra_plana[y2][x2] == 3 and x2 in [18,21]:
        self.terra_plana[y2][x2] = 1
      elif x2 in [19,20]:
        self.terra_plana[y2][x2] = 0
    def desenha(self,tela):
      for i in range(len(self.terra_plana)):
        for j in range(len(self.terra_plana[i])):
          if self.terra_plana[i][j] == 0:
           tela.blit(Imagens.AGUA, (32*j,32*i))
          elif self.terra_plana[i][j] == 1:
            tela.blit(Imagens.GRAMA, (32*j,32*i))
          elif self.terra_plana[i][j] == 2:
            tela.blit(Imagens.TIJOLO, (32*j,32*i))
          elif self.terra_plana[i][j] == 3:
            tela.blit(Imagens.MADEIRA, (32*j,32*i))