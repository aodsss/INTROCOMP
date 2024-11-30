##################################################################################################

# FIZEMOS AS PARTES EM ARQUIVOS SEPARADOS, ENTÃO PODEM TER PARTES RELACIONADAS DE FORMA ERRADA OU COM ALGO REPETIDO
# AINDA NÃO TERMINAMOS TUDO, ENTÃO AINDA TEM PARTES ERRADAS E INCOMPLETAS

##################################################################################################

# PARTE DOS PERSONAGENS
import pygame
import random
import math

# BIBLIOTECA DOS PERSONAGENS
class Personagem():
    
    def __init__(self, nome, ATK, DEF, VEL):

    # ATRIBUTOS BÁSICOS DOS PERSONAGENS

        self.nome = nome
        self.vida = 30 + (DEF - 1) * 5
        self.baseAtaque = ATK
        self.baseDefesa = DEF  
        self.baseVelocidade = VEL
        
        self.vulneravel = True # VULNERÁVEL: CONDIÇÃO DAQUELE QUE PODE PERDER VIDA
        self.quebrado = False # QUEBRADO: CONDIÇÃO QUE FAZ O PERSONAGEM TOMAR O DOBRO DE DANO E NÃO CONSEGUIR ATACAR. SÓ É TRATÁVEL COM CURA. 

        self.modificador = [0, 0, 0] # MODIFICADORES DOS ATRIBUTOS BASE

        def habilidade(self): # TODOS OS PERSONAGENS TERÃO UMA HABILIDADE ÚNICA PARA ELES
            raise NotImplementedError

    # AS PROPRIEDADES SERVEM PARA RESUMIR OS VALORES BASE COM OS MODIFICADORES EM UM LUGAR SÓ, FACILITANDO A SUA UTILIZAÇÃO NO CÓDIGO

    def __str__(self):
        return self.nome

    @property
    def ataque(self):
        return self.baseAtaque + self.modificador[0]
    
    @property
    def defesa(self):
        return self.baseDefesa + self.modificador[1]
    
    @property
    def velocidade(self):
        return self.baseVelocidade + self.modificador[2]
    
    @property
    def danoRatio(self):
        if self.quebrado:
            return 2
        return 1

    # LIMPADOR DOS MODIFICADORES

    def modClear(self):
        self.modificador = [0, 0, 0]

    # FUNÇÃO USADA PARA FACILIDADE A VISUALIZAÇÃO DE ATRIBUTOS. MOSTRA OS ATRIBUTOS BASE MAIS SEUS MODIFICADORES

    def mostrarStats(self):
        print(f'''{self.nome} 
        PV: {self.vida} 
        ATK: {self.baseAtaque} + {self.modificador[0]}
        DEF: {self.baseDefesa} + {self.modificador[1]} 
        VEL: {self.baseVelocidade} + {self.modificador[2]}''')

class Guerreiro(Personagem):

    def __init__(self, nome):
        super().__init__(nome, ATK=5, DEF=3, VEL=1)

    def habilidade(self, alvo): # PANCADA: ATAQUE DESCONSIDERA DEFESA, CAUSANDO 3x SEU ATAQUE, MAS DEIXA QUEBRADO
        if not self.quebrado:
            dano = round(self.ataque * 3)
            alvo.mudar_pv(dano) 
            print(f'{self.nome} DEU UMA PANCADA EM {alvo.nome}, CAUSANDO {dano} DE DANO!')
            self.quebrado = True
        else:
            print(f'O {self.nome} ESTÁ QUEBRADO!')

class Assassino(Personagem):

    def __init__(self, nome):
        super().__init__(nome, ATK=5, DEF=1, VEL=3)
        self.espreita = False

    def habilidade(self): # ESPREITAR: FICA INVULNERÁVEL E GANHA 2 DE ATAQUE A CADA RODADA INVULNERÁVEL, MAS DEIXA QUEBRADO
        if not self.quebrado:
            if self.vulneravel:
                self.vulneravel = False
                print(f'{self.nome} SE ESCONDE E SE PREPARA!')
            else:
                self.modificador[0] += 2
                print(f'{self.nome} ESTÁ FICANDO MAIS FORTE!')
        else:
            print(f'O {self.nome} ESTÁ QUEBRADO!')

class Tanque(Personagem):

    def __init__(self, nome):
        super().__init__(nome, ATK=3, DEF=5, VEL=1)

    def habilidade(self, alvo): # SENTINELA: AUMENTA A PRÓPRIA DEFESA E A DE UM ALIADO
        self.modificador[1] += self.defesa + 3
        alvo.modificador[1] += alvo.defesa + 3
        print(f'{self.nome} SE FORTIFICA, PROTEGENDO {alvo.nome}')
 
class Curandeiro(Personagem):

    def __init__(self, nome):
        super().__init__(nome, ATK=1, DEF=5, VEL=3)

    def habilidade(self, alvo): # CURA: REGENERA VIDA E LIMPA A CONDIÇÃO "QUEBRADO"
        cura = (3 + alvo.defesa) * -1
        if cura > -3:
            cura = -3
        alvo.mudar_pv(cura)
        print(f'{self.nome} RECUPERA {cura} DE VIDA DE {alvo.nome}', end=" ")
        if alvo.quebrado:
            alvo.quebrado = False
            print('E ELE DEIXA DE ESTAR QUEBRADO', end=" ")
        print('!')
        
class Mago(Personagem):

    def __init__(self, nome):
        super().__init__(nome, ATK=3, DEF=1, VEL=5)

    def habilidade(self, inimigos): # FOGO: CAUSA DANO A TODOS OS INIMIGOS, MAS TOMA DANO DO PRÓPRIO ATAQUE
        for inimigo in inimigos:
            dano = (self.ataque) * ((self.velocidade) + 1 - (inimigo.velocidade))
            if dano > 0:
                inimigo.mudar_pv(dano)
                print(f'{inimigo.nome} TOMOU {dano} DE DANO!')
            else:
                print(f'{inimigo.nome} NÃO TOMOU DANO!')

        self.mudar_pv(self.ataque + self.velocidade)
        print(f'{self.nome} SE QUEIMOU COM SUA MAGIA, TOMANDO {self.ataque + self.velocidade} DE DANO!')

class Bardo(Personagem):

    def __init__(self, nome):
        super().__init__(nome, ATK=1, DEF=3, VEL=5)

    def habilidade(self, alvo): # INSPIRAR: ADICIONA 5 DE MOD EM UM STAT ALEATÓRIO DE UM ALIADO
        stat = random.randint(0,2)
        alvo.modificador[stat] += 5
        stats = ['ATAQUE', 'DEFESA', 'VELOCIDADE']
        print(f'{alvo.nome} GANHOU +5 EM {stats[stat]}')    

class Inimigo(Personagem):

    def __init__(self, nome):
        super().__init__(nome, ATK= 2, DEF=2, VEL=3)
        self.insanidadeModificador = [0, 0, 0]
        self.ehInimigo = True

    def habilidade(self): # INSANIDADE: A CADA RODADA OS INIMIGOS GANHAM MODIFICADORES NOVOS NOS STATS DELES
        regulador = 6
        for mod in range(3):
            self.modificador[mod] -= self.insanidadeModificador[mod]

            i = random.randint(1, 3)
            if regulador < i:
                i = regulador
            self.insanidadeModificador[mod] += i
            regulador -= i

            self.modificador[mod] += self.insanidadeModificador[mod]
        
def criar_aliado():
    print('DE QUAL CLASSE SEU PERSONAGEM SERÁ?')
    print('''          [1] GUERREIRO
          [2] ASSASSINO
          [3] TANQUE
          [4] CURANDEIRO
          [5] MAGO
          [6] BARDO''')
    
    classes = [Guerreiro, Assassino, Tanque, Curandeiro, Mago, Bardo]
    
    while True:
        escolha = int(input("ESCOLHA UMA CLASSE: ")) - 1
        if 0 <= escolha <= 5:
            classe = classes[escolha]
            break
        else:
            print("ESCOLHA INVÁLIDA. TENTE NOVAMENTE. ")
    
    nome = input("ESCOLHA O NOME DO PERSONAGEM: ")

    return classe(nome)

def criar_aliados():

    Aliados = []

    for i in range(3):
        print('CRIE O ALIADO ' + str(i + 1))
        Aliados.append(criar_aliado())
        Aliados[i].mostrarStats()
        input('APERTE QUALQUER BOTÃO...')

    return Aliados

def criar_inimigos():

    Inimigos = []

    for i in range(3):
        Nome = 'Inimigo ' + str(i + 1)
        Inimigos.append(Inimigo(Nome))

    return Inimigos

##################################################################################################

# PARTE DO SISTEMA DE BATALHA

# import personagens as pers

def ordenaVelocidade(personagens): # ORDENADOR DA ORDEM DA BATALHA
    personagens.sort(reverse = True, key= lambda p: p.velocidade)
    print([str(personagem) for personagem in personagens])

def verificaVivos(personagens): # VERIFICA QUAIS PERSONAGENS ESTÃO VIVOS
    for i in personagens[:]:
        if i.vida <= 0:
            print(f'{i.nome} MORREU')
            personagens.remove(i)

def verificar(personagens): # VERIFICAÇÃO DE VIVOS E DA SITUAÇÃO DA BATALHA. USADO PARA DEFINIR A VITÓRIA/DERROTA
    
    verificaVivos(personagens)

    AliadosVivos = 0
    InimigosVivos = 0
    Resultado = 0

    for i in personagens:
        if i.ehInimigo == False:
            AliadosVivos += 1
        else:
            InimigosVivos += 1
    
    if AliadosVivos == 0:
        Resultado = 1
    if InimigosVivos == 0:
        Resultado = 2

    if Resultado == 1 or 2:
        fimBatalha(Resultado)
        return True
    else:
        return False

def mudar_pv(self, dano): # ALTERADOR DA VIDA DOS PERSONAGENS
    self.vida -= dano

    print(f"Vida atual de {self.nome}: {self.vidaAtual}")

def estarSeDefendendo(self): # INSPECIONA SE O PERSONAGEM ATUAL ESTÁ SE DEFENDENDO
    return self.defendendo

def defender(self): # QUANDO É ESCOLHIDA A OPÇÃO DEFESA
    self.modClear()
    self.mod[1] += self.baseDefesa

def pararDeDefender(self): # QUANDO O PERSONAGEM PARA DE SE DEFENDER
    if self.estarSeDefendendo(self):
        self.DEF = int (self.DEF * 0.5)
        self.defendendo = False

def atacar(self, alvo): # QUANDO É ESCOLHIDA A OPÇÃO ATAQUE
        if self.quebrado:
            return print(f'O {self.nome} ESTÁ QUEBRADO E NÃO CONSEGUE ATACAR') # PERSONAGENS QUEBRADOS NÃO ATACAM

        if alvo.vulneravel:
            dano = round((self.ataque) * (10 / (10 + alvo.defesa)) * alvo.danoRatio)  # DANO BASE DECIDIDO VEZES UMA RAZÃO 
            print(f'{self.nome} ATACOU {alvo.nome}, CAUSANDO {dano} DE DANO!')
            alvo.mudar_pv(dano)
        else:   # ALVOS INVULNERÁVEIS NÃO PODEM SER ATACADOS E FAZEM O ATACANTE PERDER SEU ATAQUE (na vdd o atacante não poderia atacá-lo, mas ok)
            print(f'O {alvo.nome} ESTÁ INVULNERÁVEL!')

        if not self.vulneravel: # TODOS QUE ATACAM PERDEM INVULNERABILIDADE. PERDER INVULNERABILIDADE TE DEIXA QUEBRADO. 
            self.vulneravel = True
            self.quebrado = True

        self.modClear()

def alvoAtaqueAliado(): # ESCOLHE QUAL ALVO OS HERÓIS ATACARÃO
    while True:
        escolha = int (input("Pressione '1' para atacar o Inimigo 1, '2' para o Inimigo 2 ou '3' para o Inimigo 3: "))
        
        alvos_validos = []
        for i in Personagens:
            if i in Inimigos:
                alvos_validos.append(i)
            return alvos_validos
        
        if escolha == 1:
            print(f"Você escolheu atacar Inimigo 1")
            return alvos_validos[0]
            break

        elif escolha == 2:
            print(f"Você escolheu atacar Inimigo 2")
            return alvos_validos[1]
            break

        elif escolha == 3:
            print(f"Você escolheu atacar Inimigo 3")
            return alvos_validos[2]
            break

        else:
            print("Escolha inválida. Tente novamente.")

def alvoHabilidadeAliado(): # ESCOLHE QUAL ALVO OS ALIADOS USARÃO A HABILIDADE
    while True:
        escolha = int (input("Pressione '1' para selecionar o Herói 1, '2' para o Herói 2 ou '3' para o Herói 3: "))
        
        alvos_validos = []
        for i in Personagens:
            if i in Aliados:
                alvos_validos.append(i)
            return alvos_validos
        
        if escolha == 1:
            print(f"Você selecionou Herói 1")
            return alvos_validos[0]
            break

        elif escolha == 2:
            print(f"Você selecionou Herói 2")
            return alvos_validos[1]
            break

        elif escolha == 3:
            print(f"Você selecionou Herói 3")
            return alvos_validos[2]
            break

        else:
            print("Escolha inválida. Tente novamente.")

def alvoAtaqueInimigo(): # ESCOLHE QUAL ALVO OS INIMIGOS ATACARÃO
    alvos_validos = []
    for i in Personagens:
        if i in Aliados:
            alvos_validos.append(i)
            return alvos_validos
    return random.choice(alvos_validos)

def escolherAcao (): # PARA OS INIMIGOS ESCOLHEREM SUA AÇÃO
    acoes = ["defender", "atacar", "habilidade"]
    acao_escolhida = random.choice(acoes)

    alvo = alvoAtaqueInimigo()

    if acao_escolhida == "defender":
        defender()
    elif acao_escolhida == "atacar":
        atacar(alvo)
    elif acao_escolhida == "habilidade":
        habilidade()

def mudarIndice(indice, Personagens): # PASSA A VEZ PRO PRÓXIMO PERSONAGEM NA RODADA SEGUINTE
    tamanhoLista = len(Personagens)
    if indice + 1 >= tamanhoLista:
        indice = 0
    else:
        indice += 1

    return indice

def fimBatalha(resultado): # MOSTRA O RESULTADO NO FINAL DA PARTIDA
    if resultado == 1:
        print('INIMIGOS VENCERAM! VOCÊ FOI DERROTADO!')
    elif resultado == 2:
        print('HERÓIS VENCERAM! VOCÊ VENCEU!')
    else:
        return None
    

    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CLASSES ^ ~~~~ CÓDIGO v ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def simular():
    Aliados = criar_aliados()
    Inimigos = criar_inimigos()

    Personagens = Aliados + Inimigos # JUNTA TODOS OS PERSONAGENS EM UMA SÓ LISTA. USADA TAMBÉM PARA SABER QUEM ESTÁ VIVO
    print([str(personagem) for personagem in Personagens])
    ordenaVelocidade(Personagens)

    while True:

        # INÍCIO DE UMA RODADA

        ordenaVelocidade(Personagens)

        for personagem in Personagens: # PARA CADA PERSONAGEM VIVO

            personagem.vida = 0

            if indiceAtual in Aliados: # SE O PERSONAGEM DA RODADA POR UM ALIADO
            
                entrada_usuario = input("Pressione A para atacar, D para defender, ou X para usar a habilidade: ").lower() # ESCOLHA DA AÇÃO DO PERSONAGEM ATUAL

                if entrada_usuario == 'x':
                        if indiceAtual == ("Guerreiro"):
                            alvo = alvoAtaqueAliado
                        
                        if indiceAtual == ("Tanque", "Curandeiro" or "Bardo"):
                            alvo = alvoHabilidadeAliado

                        habilidade()
                        indiceAtual = mudarIndice(indiceAtual, Personagens)
                        personagemAtual = Personagens[indiceAtual]

                elif entrada_usuario == 'a':
                    alvo = alvoAtaqueAliado
                    entradaAtaque = atacar(personagemAtual, Personagens, Inimigos)

                    if entradaAtaque == 1:
                        verificaVivos()

                        if verificaVivos:
                            print(f"{verificaVivos.nome} foi derrotado!")

                            if verificaVivos in Personagens:
                                Personagens.remove(verificaVivos)
                        indiceAtual = mudarIndice(indiceAtual, Personagens)
                        personagemAtual = Personagens[indiceAtual]

                    else:
                        emExecucao = False

                elif entrada_usuario == 'd':
                    personagemAtual.defender()
                    indiceAtual = mudarIndice(indiceAtual, Personagens)
                    personagemAtual = Personagens[indiceAtual]

            elif indiceAtual in Inimigos: # SE O PERSONAGEM DA RODADA FOR UM INIMIGO
                escolherAcao()
                indiceAtual = mudarIndice(indiceAtual, Personagens)
                personagemAtual = Personagens[indiceAtual]

            if verificar(Personagens):
                break

        else: 
            continue

        break

    return None

simular()

##################################################################################################

# PARTE DA INTERFACE

pygame.init() #inicia pygame, informações de janela e fps
largura_tela, altura_tela = 1024, 768
fps = 30

#inicia a tela
screen = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("introbattle")
clock = pygame.time.Clock()

#plano de fundo e ajuste pro tamanho correto
fundo = pygame.image.load('imagens/teste 7.png').convert_alpha()
tamanho_escala = (1024, 768)
fundo = pygame.transform.scale(fundo, tamanho_escala)

def desenha_plano_fundo():
    screen.blit(fundo, (0, 0))
def desenha_guerreiro():
	screen.blit(imagem_guerreiro, (312, 384))
def desenha_assassino():
	screen.blit(imagem_assassino, (202, 234))
def desenha_mago():
	screen.blit(imagem_mago, (182, 484))
def desenha_inimigo1():
	screen.blit(imagem_inimigo1, (812, 234))
def desenha_inimigo2():
	screen.blit(imagem_inimigo2, (690, 350))

#renderizar os personagens e inimigos (escolhi três personagens quaisquer e coloquei dois inimigos só, pra colocar outro só ctrl+c ctrl+v no código)
imagem_mago = pygame.image.load('imagens/wizardfinal.png').convert_alpha()
imagem_mago = pygame.transform.scale(imagem_mago, tamanho_escala)

imagem_assassino = pygame.image.load('imagens/rogue.png').convert_alpha()
imagem_assassino = pygame.transform.scale(imagem_assassino, tamanho_escala)

imagem_guerreiro = pygame.image.load('imagens/Paladino.png').convert_alpha()
tamanho_escala = (200, 200)
imagem_guerreiro = pygame.transform.scale(imagem_guerreiro, tamanho_escala)

imagem_inimigo1 = pygame.image.load('imagens/caveira sprite 2.png').convert_alpha()
imagem_inimigo1 = pygame.transform.scale(imagem_inimigo1, tamanho_escala)

imagem_inimigo2 = pygame.image.load('imagens/caveira sprite 2.png').convert_alpha()
imagem_inimigo2 = pygame.transform.scale(imagem_inimigo2, tamanho_escala)
#loop do jogo
running = True
while running:

    #chama as funções para desenhar os personagens
    desenha_plano_fundo()
    desenha_guerreiro()
    desenha_assassino()
    desenha_mago()
    desenha_inimigo1()
    desenha_inimigo2()

    #identifica eventos 
    for event in pygame.event.get():
        simular()
        if (Personagem).PDV < 0:
            running = False
        elif event.type == pygame.QUIT:
            running = False
        

    # velocidade de atualização
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
