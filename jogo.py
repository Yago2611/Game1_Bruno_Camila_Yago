from configuracoes import configuracoes
from jogador import jogador

class Jogo:
  def __init__(self):
        pg.init()
        self.tela = pg.display.set_mode(     
            (Configuracao.LARGURA_TELA, Configuracao.ALTURA_TELA))
