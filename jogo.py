from cena_principal import Cena_principal
from configuracoes import Configuracoes
from jogador import Jogador

class Jogo:
  def __init__(self):
        pg.init()
        self.tela = pg.display.set_mode(     
            (Configuracao.LARGURA_TELA, Configuracao.ALTURA_TELA))
