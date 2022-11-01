import PODERES

class Personagens():
  def__init__(self, nikola_tesla, poderes, imagem)
  self.nikola_tesla = nikola_tesla
  self.poderes = poderes
  self.imagem = imagem
  def load_image(nikola_tesla, colorkey=None, scale=1.0):
    image = pg.image.load(nikola_tesla)
    size = image.get_size()
    size = (int(size[0] * scale), int(size[1] * scale))
    image = pg.transform.scale(image, size)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image

