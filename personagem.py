from imagens import animacao_movimento,animacao_morte,animacao_ataque,load_image
from configuracoes import Configuracoes

class Personagem:
  def __init__(self, nome, imagem, poder):
    self.nome = nome
    self.velocidade = Configuracoes.VELOCIDADE
    self.vida_maxima = 200
    self.reconhecimento = 0 
    self.dano_recebido = 1
    self.dano_dado = 10
    self.probabilidade = 0
    self.tempo_parado = 0
    self.animacao = animacao_movimento(load_image(imagem,scale=1))
    self.animacao_morte = animacao_morte(load_image(imagem,scale=1))
    self.animacao_ataque = animacao_ataque(load_image(imagem,scale=1))
    self.poder = poder
