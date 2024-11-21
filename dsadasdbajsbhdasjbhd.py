import personagens as pers
import random

def criar_aliado(): # CRIADOR DE HERÓI
    print('DE QUAL CLASSE SEU PERSONAGEM SERÁ?')
    print('''          [1] GUERREIRO
          [2] ASSASSINO
          [3] TANQUE
          [4] CURANDEIRO
          [5] MAGO
          [6] BARDO''')
    
    classes = [pers.Guerreiro, pers.Assassino, pers.Tanque, pers.Curandeiro, pers.Mago, pers.Bardo]
    
    while True:
        escolha = int(input("ESCOLHA UMA CLASSE: ")) - 1
        if 0 <= escolha <= 5:
            classe = classes[escolha]
            break
        else:
            print("ESCOLHA INVÁLIDA. TENTE NOVAMENTE. ")
    
    nome = input("ESCOLHA O NOME DO PERSONAGEM: ")

    return classe(nome)

def criar_aliados(): # GERADOR DO TIME DE HERÓIS

    Aliados = []

    for i in range(3):
        print('CRIE O ALIADO ' + str(i + 1))
        Aliados.append(criar_aliado())
        Aliados[i].mostrarStats()
        input('APERTE QUALQUER BOTÃO...')

    return Aliados

def criar_inimigos(): # GERADOR DOS INIMIGOS

    Inimigos = []

    for i in range(3):
        Nome = 'Inimigo ' + str(i + 1)
        Inimigos.append(pers.Inimigo(Nome))

    return Inimigos

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

def alvoAtaqueInimigo(): # ESCOLHE QUAL ALVO ALIADO OS INIMIGOS ATACARÃO
    alvos_validos = []
    for i in Personagens:
        if i in Aliados:
            alvos_validos.append(i)
            return alvos_validos
    return random.choice(alvos_validos)

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
            
#fazendo codigo sistema de batalha

            if indiceAtual in Aliados: # SE O PERSONAGEM DA RODADA POR UM ALIADO
            
                entrada_usuario = input("Pressione A para atacar, D para defender, ou X para usar a habilidade: ").lower() # ESCOLHA DA AÇÃO DO PERSONAGEM ATUAL

                if entrada_usuario == 'x':
                        habilidade()
                        indiceAtual = mudarIndice(indiceAtual, Personagens)
                        personagemAtual = Personagens[indiceAtual]

                elif entrada_usuario == 'a':
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

#termino codigo sistema de batalha

            if verificar(Personagens):
                break

        else: 
            continue

        break

    return None

simular()
