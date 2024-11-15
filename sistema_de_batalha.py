import personagens as pers

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

def atualizaVida(self, dano): # ATUALIZA A VIDA DO PERSONAGEM APÓS UM CONFRONTO
    if dano > 0 and self.vidaAtual + dano > self.vidaMaxima:
        self.vidaAtual = self.vidaMaxima
    elif dano < 0 and self.vidaAtual + dano <= 0:
        self.vidaAtual = 0
    else:
        self.vidaAtual += dano

    print(f"Vida atual de {self.nome}: {self.vidaAtual}")

def estarSeDefendendo(self): # INSPECIONA SE O PERSONAGEM ATUAL ESTÁ SE DEFENDENDO
    return self.defendendo

def defesa(self): # QUANDO É ESCOLHIDA A OPÇÃO DEFESA
    if not self.estarSeDefendendo():
        self.DEF *= 2
        self.defendendo = True

def pararDeDefender(self): # QUANDO O PERSONAGEM PARA DE SE DEFENDER
    if self.estarSeDefendendo():
        self.DEF = int (self.DEF * 0.5)
        self.defendendo = False

def calculaDano (): # CÁLCULO DO DANO QUE O PERSONAGEM RECEBEU DO OPONENTE
        
def ataque(personagemAtual, Aliados, Inimigos): # QUANDO É ESCOLHIDA A OPÇÃO ATAQUE
    selecaoInimigo = 0

    while True:
        print("Selecione o inimigo para atacar:")
        for i in range(len(Inimigos)):
            print(f"[{i} - {Inimigos[i].nome}]")
        print("[-1 - encerrar jogo]")

        selecaoInimigo = int(input())

        if selecaoInimigo == -1:
            return 0
        elif selecaoInimigo == 0 or selecaoInimigo == 1:

            # Complete o código aqui!!!
            calcularDanoAtaqueBasico(personagemAtual, Inimigos[selecaoInimigo])
            return 1
        else:
            print('Opção inválida! Tente novamente')

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

            entrada_usuario = input("Pressione A para atacar, D para defender, ou S para sair: ").lower() # ESCOLHA DA AÇÃO DO PERSONAGEM ATUAL

            if entrada_usuario == 's':
                emExecucao = False
            elif entrada_usuario == 'a':
                entradaAtaque = atacar(personagemAtual, Personagens, Inimigos)

                if entradaAtaque == 1:
                    verificaVivos()

                    if verificaVivos:
                        listaBatalha.remove(verificaVivos)
                        print(f"{verificaVivos.nome} foi derrotado!")

                        if verificaVivos in listaPersonagens:
                            listaPersonagens.remove(verificaVivos)
                        else:
                            listaInimigos.remove(verificaVivos)
                    indiceAtual = proximoIndice(indiceAtual, listaBatalha)
                    personagemAtual = listaBatalha[indiceAtual]

                else:
                    emExecucao = False

            elif entrada_usuario == 'd':
                personagemAtual.defender()
                indiceAtual = proximoIndice(indiceAtual, listaBatalha)
                personagemAtual = listaBatalha[indiceAtual]

#termino codigo sistema de batalha

            if verificar(Personagens):
                break

        else: 
            continue

        break

    return None

simular()
