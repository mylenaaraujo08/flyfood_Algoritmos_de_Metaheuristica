# busca tabu - flyfood (algoritmo de busca local) - O(iteracoes * qtd_viz * qtd_pts)

import random
import time

# lê o arquivo do tsplib e retorna uma lista com todos os pontos
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

# calculando a distância do percurso, na primeira ocorrência será os pontos na ordem do arquivo
def calc_dist_2a2(pt1, pt2):    
    calculo = (((pt1[0]-pt2[0])**2)+((pt1[1]-pt2[1])**2))**(1/2)
    return calculo

def calc_dist_total(pontos):
    dist_total = 0
    for i in range(len(pontos)-1):
        pt1 = pontos[i]
        pt2 = pontos[i+1]
        dist_total += calc_dist_2a2(pt1, pt2)
    pt_origem = pontos[0]
    pt_final = pontos[-1]
    volta = calc_dist_2a2(pt_origem, pt_final)
    dist_total += volta
    return dist_total

# comparação
def idx_menor_custo(lista_custos):
    idx_menor_c = -1
    menor_custo = float('inf')
    for i, custo in enumerate(lista_custos):
        if custo < menor_custo:
            menor_custo = custo
            idx_menor_c = i
    return idx_menor_c

# gerando uma solução "vizinha" trocando 2 pontos aleatórios da solução atual
def gerar_vizinhanca(solucao):
    nova_sol = solucao[:]
    idx_1, idx_2 = random.sample(range(len(solucao)), 2)
    nova_sol[idx_1], nova_sol[idx_2] = nova_sol[idx_2], nova_sol[idx_1]
    return nova_sol

# realizando a busca tabu
def busca_tabu(pontos, iteracoes, tam_tabu, qtd_viz):
    qtd_pts = len(pontos)

    # solução inicial
    melhor_sol = pontos
    melhor_custo = calc_dist_total(pontos)

    # solução atual
    sol_atual = melhor_sol[:]
    custo_atual = melhor_custo

    # lista tabu
    tabu = [None]*tam_tabu
    idx_tabu = 0

    # vizinhos
    vizinhos = [None]*qtd_viz
    custos_viz = [float('inf')]*qtd_viz

    for iteracao in range(iteracoes):
        # reiniciando listas
        for i in range(qtd_viz):
            vizinhos[i] = None
            custos_viz[i] = float('inf')
        
        # gerar vizinhos
        for v in range(qtd_viz):
            vizinho = gerar_vizinhanca(sol_atual)
            if vizinho not in tabu:
                custos_viz[v] = calc_dist_total(vizinho)
                vizinhos[v] = vizinho
        
        # vizinho c/ menor custo
        idx_melhor = idx_menor_custo(custos_viz)
        nova_sol = vizinhos[idx_melhor]
        novo_custo = custos_viz[idx_melhor]

        # atualizando solução atual
        sol_atual = nova_sol
        custo_atual = novo_custo

        # comparação com o melhor até agora
        if custo_atual < melhor_custo:
            melhor_sol = sol_atual
            melhor_custo = custo_atual

        # atualizando lista tabu
        tabu[idx_tabu] = sol_atual
        idx_tabu = (idx_tabu+1)%tam_tabu # rotação p/ sobrescrever valores na lista tabu
    return melhor_sol, melhor_custo



def principal():
    pontos = ler_tsplib('berlin52.tsp')
    t_inicial = time.time()
    m_sol, m_custo = busca_tabu(pontos, 100000, 10, 100)
    t_final = time.time()

    m_sol = [pontos.index(city) + 1 for city in m_sol]
    print(f'A melhor solução é: {m_sol}')
    print(f'Com o custo de {m_custo} Km')
    print(f'Executado em {t_final - t_inicial} segundos')
    

if __name__ == '__main__':
    principal()