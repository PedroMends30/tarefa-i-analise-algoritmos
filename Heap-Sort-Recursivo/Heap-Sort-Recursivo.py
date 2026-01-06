import time
import copy

def heapsort_recursivo(vetor_in):
  # cópia da lista original
  lista = copy.copy(vetor_in)
  n = len(lista)

  # contadores
  comparacoes = 0
  trocas = 0
  inicio = time.perf_counter()

  def max_heap(n, i):
    nonlocal comparacoes, trocas
    maior = i
    esquerda = 2 * i + 1
    direita = 2 * i + 2

    # verificações dos filhos
    if esquerda < n :
      comparacoes += 1
      if lista[esquerda] > lista[maior]:
        maior = esquerda

    if direita < n:
      comparacoes += 1
      if lista[direita] > lista[maior]:
        maior = direita

    # troca se um dos filhos for maior
    if maior != i:
      lista[i], lista[maior] = lista[maior], lista[i]
      trocas += 1

      max_heap(n, maior)
  for i in range(n // 2 -1, -1, -1):
    max_heap(n, i)

  for i in range(n - 1, 0, -1):
    lista[i], lista[0] = lista[0], lista[i]
    trocas += 1

    max_heap(i, 0)
  fim = time.perf_counter()
  return fim - inicio, comparacoes, trocas