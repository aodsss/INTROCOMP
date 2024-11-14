import pygame
import random

pygame.init()

class Atacante:
    def _init_(self):
        self.nome = "Kael, o Guardião das Sombras"
        self.ataque = 100
        self.vida = 1000
        self.defesa = 50
        self.velocidade = 2

class Defensor:
    def _init_(self):
        self.nome = "Lyra, a Arqueira da Aurora"
        self.ataque = 50
        self.vida = 1000
        self.defesa = 300
        self.velocidade = 1

class Flash:
    def _init_(self):
        self.nome = "Finn, o Mago das Chamas"
        self.ataque = 60
        self.vida = 1000
        self.defesa = 50
        self.velocidade = 3

class AtacanteInimigo:
    def _init_(self):
        self.nome = "Malakar, o Ceifador Sombrio"
        self.ataque = 100
        self.vida = 1000
        self.defesa = 50
        self.velocidade = 2

class DefensorInimigo:
    def _init_(self):
        self.nome = "Thorne, o Brutamontes das Trevas"
        self.ataque = 50
        self.vida = 1000
        self.defesa = 300
        self.velocidade = 1

class FlashInimigo:
    def _init_(self):
        self.nome = "Voss, o Mestre das Poções"
        self.ataque = 60
        self.vida = 1000
        self.defesa = 50
        self.velocidade = 3


jogador_personagens = [Atacante(), Defensor(), Flash()]
inimigo_personagens = [AtacanteInimigo(), DefensorInimigo(), FlashInimigo()]


def calcular_dano(atacante, defensor):
    dano = atacante.ataque * (50/(50+defensor.defesa))
    defensor.vida -= dano 
    return max(dano,0)

def ordenar_personagens(personagens):
    return sorted(personagens, key=lambda x: x.velocidade, reverse=True)

running=True
personagens_ordenados = ordenar_personagens(jogador_personagens + inimigo_personagens)
indice_turno=0


while running:
    for event in pygame.event.get():
        if event.type
