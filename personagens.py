import PODERES

class Personagens():
  def__init__(self, nome, poderes, imagem)
  self.nome = nikola_tesla
  self.poderes = poderes
  self.imagem = imagem
  def load_image(nome, colorkey=None, scale=1.0):
    image = pg.image.load(nome)
    size = image.get_size()
    size = (int(size[0] * scale), int(size[1] * scale))
    image = pg.transform.scale(image, size)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image
