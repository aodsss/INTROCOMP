import random

# BIBLIOTECA DOS PERSONAGENS
class Personagem():
    
    def __init__(self, NOME, PDV, ATK, DEF, VEL):

        self.nome = NOME
        self.vida = PDV
        self.ataque = ATK
        self.defesa = DEF  
        self.velocidade = VEL
        self.mod = [0, 0, 0] # MODIFICADORES DOS ATRIBUTOS ATK, DEF E VEL DOS PERSONAGENS

    def atacar(self, target):
        dano = round((self.ataque + self.mod[0]) * (50 / (50 + target.defesa + target.mod[1])))
        target.mudar_pv(dano)
        self.mod_clear

    def defender(self): # FUNÇÃO PARA DEIXAR O PERSONAGEM SE DEFENDENDO
        self.mod_clear
        self.mod[1] += self.defesa * 0.1

    def mudar_pv(self, dano): # MUDANÇA NA VIDA DOS PERSONAGENS
        self.vida -= dano

    def mod_clear(self):
        for modificador in self.mod:
            modificador = 0


class Guerreiro(Personagem):

    def __init__(self):
        super().__init__(NOME='GUERREIRO', PDV=10 , ATK=5, DEF=3, VEL=1)
        self.charging = False # BOOLEAN DE CARREGAMENTO DO Guerreiro
        self.lastVida = 0


    def ataque_carregado(self, target): # ATAQUE CARREGADO: ADICIONA AO ATK METADE DO DANO SOFRIDO ATÉ DESCARREGAR
        if not self.charging:
            self.charging = True
            self.lastVida = self.vida
            print('CARREGANDO ATAQUE')
            return None

        if self.charging:
            self.mod[0] = self.lastVida - self.vida
            self.charging = False
            dano = self.atacar(target)
            print(dano)
            target.mudar_pv(dano)

class Assasino(Personagem):

    def __init__(self):
        super().__init__(NOME='ASSASSINO', PDV=10 , ATK=5, DEF=1, VEL=3)

class Tanque(Personagem):

    def __init__(self):
        super().__init__(NOME='TANQUE', PDV=10 , ATK=3, DEF=5, VEL=1)

class Curandeiro(Personagem):

    def __init__(self):
        super().__init__(NOME='CURANDEIRO', PDV=10 , ATK=1, DEF=5, VEL=3)

class Mago(Personagem):

    def __init__(self):
        super().__init__(NOME='MAGO', PDV=10 , ATK=3, DEF=1, VEL=5)

    def incendio(self, inimigos):
        for inimigo in inimigos:
            dano = (self.ataque + self.mod[0]) * ((self.velocidade + self.mod[2]) + 1 - (inimigo.velocidade + inimigo.mod[2]))
            if dano > 0:
                inimigo.mudar_pv(dano)
                print(f'{inimigo.nome} tomou {dano} de dano!')
            else:
                print(f'{inimigo.nome} não tomou dano!')
        self.mudar_pv(self.ataque + self.velocidade)
        print(f'{self.nome} se queimou com sua magia, tomando {self.ataque + self.velocidade} de dano!!')

class Bardo(Personagem):

    def __init__(self):
        super().__init__(NOME='BARDO', PDV=10 , ATK=1, DEF=3, VEL=5)

    def inspiration(self, target): # INSPIRAÇÃO: ADICIONA 5 DE MOD EM UM STAT ALEATÓRIO EM UM ALIADO
        #stat = random.randint(0,2)
        stat = 2
        target.mod[stat] += 3
        stats = ['ATAQUE', 'DEFESA', 'VELOCIDADE']
        print(f'{target.nome} GANHOU +5 EM {stats[stat]}')    

class Inimigo(Personagem):

    def __init__(self):
        super().__init__(NOME='INIMIGO', PDV=6, ATK= 2, DEF=2, VEL=3)

    def insanidade(self): # INSANIDADE: A CADA RODADA OS INIMIGOS GANHAM MODIFICADORES NOVOS NOS STATS DELES
        regulador = 0
        for i in range(len(self.mod)):
            modificador = random.randint(0, 3)
            self.mod[i] = regulador + modificador
            regulador = modificador * -1 

bardo = Bardo()
guerreiro = Guerreiro()
mago = Mago()

ruim1 = Inimigo()
ruim2 = Inimigo()
ruim3 = Inimigo()

Inimigos = [ruim1, ruim2, ruim3]

for inimigo in Inimigos:
    print(f'o {inimigo.nome} tem {inimigo.vida} de vida')
    inimigo.insanidade()
    print(f'stats de {inimigo.nome}: {inimigo.ataque + inimigo.mod[0]}, {inimigo.defesa + inimigo.mod[1]}, {inimigo.velocidade + inimigo.mod[2]}')

bardo.inspiration(mago)
mago.incendio(Inimigos)

for inimigo in Inimigos:
    print(f'o {inimigo.nome} tem {inimigo.vida} de vida')