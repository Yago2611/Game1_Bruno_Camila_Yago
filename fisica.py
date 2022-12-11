from mapa import Mapa

class Fisica:
    def __init__(self):
      pass
    def contato(self,corpo1,corpo2):
      return (corpo1.px+corpo1.largura>=corpo2.px and corpo1.px<=corpo2.px+corpo2.largura) and (corpo1.py+corpo1.altura>=corpo2.py and corpo1.py<=corpo2.py+corpo2.altura)
    def distancia(self,corpo1,corpo2):
      return (((((corpo1.px+corpo1.largura)//2)-((corpo2.px+corpo2.largura)//2))**2 + ((((corpo1.py+corpo1.altura)//2))-((corpo2.py+corpo2.altura)//2))**2)**0.5)
    def movimento(self,novo_corpo,corpos):
      mapa = Mapa()
      valor = 0 
      for corpo in corpos:
          for ente in corpo:
            if self.contato(novo_corpo,ente):
              valor = True
              break
            else:
              valor = False 
          if valor:
            break
      if not mapa.limite(novo_corpo) and not valor:
          return True
      else:
          return False
