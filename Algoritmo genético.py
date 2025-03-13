import math
import random
import time

def ler_tsplib(arquivo):
    with open(arquivo, "r") as arquivo:
        linhas = arquivo.readlines()

    pontos = []
    ler_coordenadas = False

    for linha in linhas:
        linha = linha.strip()
        if linha == "NODE_COORD_SECTION":
            ler_coordenadas = True
            continue
        elif linha == "EOF":
            break

        if ler_coordenadas:
            partes = linha.split()
            if len(partes) == 3:
                _, x, y = partes
                pontos.append((float(x), float(y)))

    return pontos


def gerar_populacao(cromossomo, tamanho):
    populacao = set()

    while len(populacao) < tamanho:
        individuo = tuple(random.sample(cromossomo, len(cromossomo)))
        populacao.add(individuo)

    return [list(individuo) for individuo in populacao]


def calcular_distancia(p1, p2, registro):
    x1, y1 = p1
    x2, y2 = p2

    if (p1, p2) in registro:
        return registro[(p1, p2)]
    elif (p2, p1) in registro:
        return registro[(p2, p1)]
    else:
        distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        registro[(p1, p2)] = distancia
        registro[(p2, p1)] = distancia
        return distancia


def fitness(populacao, registrar):
    custos = []

    for individuo in populacao:
        custo = 0
        individuo_completo = individuo + [individuo[0]]
        for i in range(len(individuo_completo) - 1):
            p1 = individuo_completo[i]
            p2 = individuo_completo[i + 1]
            custo += calcular_distancia(p1, p2, registrar)
        custos.append(custo)

    return custos


def selecionar_elite(populacao, custos, n_elite):
    populacao_custo = zip(populacao, custos)

    ordenado = sorted(populacao_custo, key=lambda x: x[1])

    elite = [individuo[0] for individuo in ordenado[:n_elite]]
    return elite


def selecionar_roleta(populacao, custos, n_selecionados):
    total_custo = sum(1 / (c + 1) for c in custos)
    probabilidades = [(1 / (c + 1)) / total_custo for c in custos]

    selecionados = random.choices(populacao, weights=probabilidades, k=n_selecionados)
    return selecionados


def selecionar(populacao, custos, quantidade):
    n_elite = round(0.2 * quantidade)
    elite = selecionar_elite(populacao, custos, n_elite)
    n_roleta = quantidade - n_elite
    roleta = selecionar_roleta(populacao, custos, n_roleta)
    return elite + roleta


def crossover(aptos):
    pai1, pai2 = random.sample(aptos, 2)
    filho = [None] * len(pai1)

    p1, p2 = sorted(random.sample(range(len(pai1)), 2))

    filho[p1:p2] = pai1[p1:p2]

    restantes = [gene for gene in pai2 if gene not in filho]

    indice = 0
    for i in range(len(filho)):
        if filho[i] is None:
            filho[i] = restantes[indice]
            indice += 1

    return filho


def mutacao(cromossomo, taxa_mutacao):
    if random.random() < taxa_mutacao:
        p1, p2 = sorted(random.sample(range(len(cromossomo)), 2))
        cromossomo[p1:p2+1] = reversed(cromossomo[p1:p2+1])
    return cromossomo


def algoritmo_genetico(arquivo, geracoes=3761, max_estagnado=33, tamanho_populacao=1566):

    start_time = time.time()
    pontos = ler_tsplib(arquivo)
    populacao = gerar_populacao(pontos, tamanho_populacao)
    n_selecao = round(0.17   * tamanho_populacao)
    registrar_distancias = {}
    geracao = 0
    estagnado = 0
    melhor_custo = float('inf') 
    melhor_solucao = None
    taxa_mutacao = 0.42

    while geracao < geracoes and estagnado < max_estagnado:
        custos = fitness(populacao, registrar_distancias)
        novo_melhor = min(custos)
        melhor_indice = custos.index(novo_melhor)
        melhor_atual = populacao[melhor_indice]

        if novo_melhor < melhor_custo:
            melhor_custo = novo_melhor
            melhor_solucao = melhor_atual
            estagnado = 0
        else:
            estagnado += 1

        if novo_melhor < melhor_custo:
            taxa_mutacao = max(0.01, taxa_mutacao - 0.01)
        else:
            taxa_mutacao = min(0.8, taxa_mutacao + 0.01)

        aptos = selecionar(populacao, custos, n_selecao)
        nova_populacao = aptos[:]

        while len(nova_populacao) < tamanho_populacao:
            filho = crossover(aptos)
            mutado = mutacao(filho, taxa_mutacao)
            nova_populacao.append(mutado)

        populacao = nova_populacao
        geracao += 1

        if geracao % 10 == 0:
            print(f"Geração {geracao}: Melhor custo = {round(novo_melhor)}")

    print(f"Melhor solução encontrada com custo {round(melhor_custo)}")
    print("Sequência das cidades visitadas:", [pontos.index(city) + 1 for city in melhor_solucao])

    end_time = time.time()
    duration = end_time - start_time
    print(f"O tempo de execução foi de {duration:.2f} segundos")

algoritmo_genetico('pr124.tsp')
