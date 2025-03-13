import random
import math


def ler_tsplib(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    pontos = []
    start_reading = False

    for line in lines:
        if line.startswith("NODE_COORD_SECTION"):
            start_reading = True
            continue
        if line.startswith("EOF"):
            break
        if start_reading:
            parts = line.strip().split()
            pontos.append((float(parts[1]), float(parts[2])))

    return pontos


def calcular_distancia(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def matriz_distancia(pontos):
    tamanho = len(pontos)
    distancias = [[0 for _ in range(tamanho)] for _ in range(tamanho)]

    for i in range(tamanho):
        for j in range(tamanho):
            if i != j:
                distancias[i][j] = calcular_distancia(pontos[i], pontos[j])

    return distancias


def inicializar_feromonios(tamanho):
    return [[random.uniform(0.1, 1) for _ in range(tamanho)] for _ in range(tamanho)]


def calcular_visibilidade(matriz_distancia):
    tamanho = len(matriz_distancia)
    visibilidade = [[0 for _ in range(tamanho)] for _ in range(tamanho)]

    for i in range(tamanho):
        for j in range(tamanho):
            if i != j and matriz_distancia[i][j] != 0:
                visibilidade[i][j] = 1 / matriz_distancia[i][j]

    return visibilidade


def escolher_proximo(atual, nao_visitados, feromonios, visibilidade, alpha=1, beta=2):
    probabilidades = []
    soma = 0

    for j in nao_visitados:
        valor = (feromonios[atual][j] ** alpha) * (visibilidade[atual][j] ** beta)
        probabilidades.append((j, valor))
        soma += valor

    if soma == 0:
        return random.choice(list(nao_visitados))  # Evita erro escolhendo aleatório

    probabilidades = [(j, valor / soma) for j, valor in probabilidades]
    return random.choices([p[0] for p in probabilidades], weights=[p[1] for p in probabilidades])[0]


def construir_caminho(num_cidades, feromonios, visibilidade):
    caminho = [random.randint(0, num_cidades - 1)]
    nao_visitados = set(range(num_cidades)) - {caminho[0]}

    while nao_visitados:
        proximo_no = escolher_proximo(caminho[-1], nao_visitados, feromonios, visibilidade)
        caminho.append(proximo_no)
        nao_visitados.remove(proximo_no)

    caminho.append(caminho[0])
    return caminho


def calcular_comprimento_caminho(caminho, matriz_distancia):
    total_distancia = 0
    for i in range(len(caminho) - 1):
        cidade_atual = caminho[i]
        proxima_cidade = caminho[i + 1]
        total_distancia += matriz_distancia[cidade_atual][proxima_cidade]
    return total_distancia


def atualizar_feromonios(feromonios, caminhos, matriz_distancia, taxa_evaporacao=0.5, deposito=1.0):
    tamanho = len(feromonios)

    for i in range(tamanho):
        for j in range(tamanho):
            feromonios[i][j] *= (1 - taxa_evaporacao)

    for caminho in caminhos:
        comprimento = calcular_comprimento_caminho(caminho, matriz_distancia)
        if comprimento == 0:
            continue
        feromonio_adicionado = deposito / comprimento

        for i in range(len(caminho) - 1):
            a, b = caminho[i], caminho[i + 1]
            feromonios[a][b] += feromonio_adicionado
            feromonios[b][a] += feromonio_adicionado


def algoritmo_colonia_formigas(arquivo, num_formigas=100, num_iteracoes=500, taxa_evaporacao=0.3):
    pontos = ler_tsplib(arquivo)
    matriz_dist = matriz_distancia(pontos)
    feromonios = inicializar_feromonios(len(pontos))
    visibilidade = calcular_visibilidade(matriz_dist)

    melhor_caminho = None
    melhor_distancia = float('inf')

    for iteracao in range(num_iteracoes):
        # um caminho é construido para cada formiga
        caminhos = [construir_caminho(len(pontos), feromonios, visibilidade) for _ in range(num_formigas)]
        # calcula a distancia utilizando a matriz de distancia para cada caminho construido
        distancias = [calcular_comprimento_caminho(caminho, matriz_dist) for caminho in caminhos]

        # atualiza o as variaveis de melhor distancia e caminho com base nas distancia calculadas
        for i in range(num_formigas):
            if distancias[i] < melhor_distancia:
                melhor_distancia = distancias[i]
                melhor_caminho = caminhos[i]

        atualizar_feromonios(feromonios, caminhos, matriz_dist, taxa_evaporacao)
        print(f"Iteração {iteracao + 1}/{num_iteracoes} - Melhor distância: {round(melhor_distancia)}")

    return melhor_caminho, melhor_distancia


arquivo_tsp = "berlin52.tsp"
melhor_caminho, melhor_distancia = algoritmo_colonia_formigas(arquivo_tsp)

print("\nMelhor caminho encontrado:", melhor_caminho)
print("Distância do melhor caminho:", round(melhor_distancia))
