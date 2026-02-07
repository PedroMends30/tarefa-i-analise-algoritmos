import random
import time


def heapify(vetor, n, i, metricas):
    while True:
        maior = i
        esquerda = 2 * i + 1
        direita = 2 * i + 2

        if esquerda < n:
            metricas["comparacoes"] += 1
            if vetor[esquerda] > vetor[maior]:
                maior = esquerda

        if direita < n:
            metricas["comparacoes"] += 1
            if vetor[direita] > vetor[maior]:
                maior = direita

        if maior == i:
            break

        vetor[i], vetor[maior] = vetor[maior], vetor[i]
        metricas["trocas"] += 1
        i = maior


def heap_sort(vetor):
    n = len(vetor)
    metricas = {
        "comparacoes": 0,
        "trocas": 0
    }

    # construção do heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(vetor, n, i, metricas)

    # extração
    for i in range(n - 1, 0, -1):
        vetor[0], vetor[i] = vetor[i], vetor[0]
        metricas["trocas"] += 1
        heapify(vetor, i, 0, metricas)

    return metricas

# Testes
tamanhos = [10, 100, 1000, 10000]

print("================================================== Heapsort Iterativo - Máximo =======================================================")
print("Os testes para vetor ordenado, inverso e aleatório serão realizados 5 vezes para cada tamanho de vetor e sua média será contabilizada.")


tamanhos = [10, 100, 1000, 10000]

for n in tamanhos:
#   índice 0 - tempo, índice 1 - comparação, índice 3 - troca
#   listas zeram com o próximo tamanho de vetor
    lista_Ordenada_Metrica = [[], [], []]
    lista_Inversa_Metrica = [[], [], []]
    lista_Aleatoria_Metrica = [[], [], []]

    for _ in range(5):
        # Para a lista ordenada
        vetor = list(range(n))
        inicio = time.perf_counter()
        metricas = heap_sort(vetor)
        fim = time.perf_counter()

        lista_Ordenada_Metrica[0].append(fim - inicio)
        lista_Ordenada_Metrica[1].append(metricas["comparacoes"])
        lista_Ordenada_Metrica[2].append(metricas["trocas"])

        # Para a lista com os valores inversos
        vetor = list(range(n, 0, -1))
        inicio = time.perf_counter()
        metricas = heap_sort(vetor)
        fim = time.perf_counter()

        lista_Inversa_Metrica[0].append(fim - inicio)
        lista_Inversa_Metrica[1].append(metricas["comparacoes"])
        lista_Inversa_Metrica[2].append(metricas["trocas"])

        # Lista com valores aleatórios
        vetor = [random.randint(0, n) for _ in range(n)]
        inicio = time.perf_counter()
        metricas = heap_sort(vetor)
        fim = time.perf_counter()

        lista_Aleatoria_Metrica[0].append(fim - inicio)
        lista_Aleatoria_Metrica[1].append(metricas["comparacoes"])
        lista_Aleatoria_Metrica[2].append(metricas["trocas"])

    # Resultado 
    print(f"\nTamanho do vetor: {n}")
    # tava fazendo média de tudo até perceber que só o tempo q altera nas duas primeiras listas, a aleatoria que muda tudo
    print("Ordenado  | "
          f"Tempo médio: {sum(lista_Ordenada_Metrica[0]) / 5:.6f}s | "
          f"Comparações médias: {(lista_Ordenada_Metrica[1][0]):.0f} | "
          f"Trocas médias: {(lista_Ordenada_Metrica[2][1]):.0f}")

    print("Inverso   | "
          f"Tempo médio: {sum(lista_Inversa_Metrica[0]) / 5:.6f}s | "
          f"Comparações médias: {(lista_Inversa_Metrica[1][0]) :.0f} | "
          f"Trocas médias: {(lista_Inversa_Metrica[2][0]) :.0f}")

    print("Aleatório | "
          f"Tempo médio: {sum(lista_Aleatoria_Metrica[0]) / 5:.6f}s | "
          f"Comparações médias: {sum(lista_Aleatoria_Metrica[1]) / 5:.0f} | "
          f"Trocas médias: {sum(lista_Aleatoria_Metrica[2]) / 5:.0f}")
