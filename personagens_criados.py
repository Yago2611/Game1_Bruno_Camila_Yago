from poder import Poder
from personagem import Personagem

class Personagens_criados:
    def __init__(self):
        pass
    def cria_lista(self):
        Raio = Poder("raio.png","Projetil")
        Nuvem = Poder("nuvem.png","Área")
        Cura = Poder("cura.png","Cura")
        Teletransporte = Poder("tunel.png","Teletransporte")
        Nikola = Personagem("Nikola Tesla","nikola.png",Raio) 
        Nikola.dano_dado = 20 #Vantagem
        Nikola.reconhecimento = 3 #Desvantagem (Apenas um a cada três ataques são reconhecidos pela comunidade científica)
        Marie = Personagem("Marie Curie","marie.png",Nuvem)
        Marie.dano_dado = 5 #Vantagem
        Marie.dano_recebido = 1/2 #Desvantagem
        Darwin = Personagem("Charles Darwin", "darwin.png", Cura)
        Darwin.vida_maxima = 400 #Vantagem
        Darwin.velocidade *= 0.5 #Desvantagem
        Erwin = Personagem("Erwin Schrodinger","erwin.png",Teletransporte)
        Erwin.probabilidade = 2 #Vantagem (Só recebe um dano a cada dois)
        Erwin.tempo_parado = 10 #Desvantagem (Para a cada 10 segundos para tossir e perde vida)
        return [Nikola,Marie,Darwin,Erwin]
