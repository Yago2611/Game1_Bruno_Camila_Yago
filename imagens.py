import pygame as pg

def load_image(name, colorkey=None, scale=1.0):
    image = pg.image.load(name)
    size = image.get_size()
    size = (int(size[0] * scale), int(size[1] * scale))
    image = pg.transform.scale(image, size)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image

def animacao_movimento(imagem):
  lista = []
  px = 14
  py = 515
  largura = 43
  altura = 62
  for i in range(4):
    sublista=[]
    for j in range(9):
      subimagem = imagem.subsurface(pg.Rect(px,py,largura,altura))
      sublista.append(subimagem)
      px+=64
    lista.append(sublista)
    px = 14
    py+=64
  return lista

def animacao_morte(imagem):
  lista = []
  px = 14
  py = 1291
  largura = 55
  altura = 53
  for j in range(6):
      subimagem = imagem.subsurface(pg.Rect(px,py,largura,altura))
      lista.append(subimagem)
      px+=63
  return lista

def animacao_ataque(imagem):
  lista = []
  px = 14
  py = 775
  largura = 54
  altura = 62
  for i in range(4):
    sublista=[]
    for j in range(6):
      subimagem = imagem.subsurface(pg.Rect(px,py,largura,altura))
      sublista.append(subimagem)
      px+=62
    lista.append(sublista)
    px = 14
    py+=64
  return lista

class Imagens:
  MINIONS_ANIMACAO_MOVIMENTO = animacao_movimento(load_image("minions.png",scale=1))
  MINIONS_ANIMACAO_MORTE = animacao_morte(load_image("minions.png",scale=1))
  MINIONS_ANIMACAO_ATAQUE = animacao_ataque(load_image("minions.png",scale=1))
  GRAMA = load_image("grama.png",scale=1)
  AGUA = load_image("agua.png",scale=1)
  TIJOLO = load_image("tijolo.png",scale=1)
  MADEIRA = load_image("madeira.png",scale=1)