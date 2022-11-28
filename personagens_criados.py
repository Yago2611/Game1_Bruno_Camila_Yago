from poder import Poder
from personagem import Personagem

class Personagens_criados:
    def __init__(self):
        pass
    def cria_lista(self):
        Raio = Poder("raio.png","Projetil")
        Nuvem = Poder("nuvem.png","Área")
        Cura = Poder("cura.png","Cura")
        Gato = Poder("gato.png","Projetil")
        Nikola = Personagem("Nikola Tesla","nikola.png",Raio) 
        Marie = Personagem("Marie Curie","marie.png",Nuvem)
        Darwin = Personagem("Charles Darwin", "darwin.png", Cura)
        Darwin.vida_maxima = 400 #Vantagem
        Darwin.velocidade *= 0.5 #Desvantagem
        Erwin = Personagem("Erwin Schrodinger","erwin.png",Gato)
        return [Nikola,Marie,Darwin,Erwin]
