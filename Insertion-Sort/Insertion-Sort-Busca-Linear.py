def acharElem(vetor, valor, fim): 
    
    for i in range(fim): 
        if valor < vetor[i]:
            return i
    
    return fim 

def inserirElem(vetor, valor_pos, nova_pos): 
    aux = vetor[valor_pos]

    for i in range(valor_pos,nova_pos,-1):
        vetor[i] = vetor[i-1]
    
    vetor[nova_pos] = aux

def insertionSort(vetor):
    indice_ordenados = 1 

    for i in range(1, len(vetor)): 
        nova_pos = acharElem(vetor, vetor[i], indice_ordenados)
        inserirElem(vetor, i, nova_pos)     
        indice_ordenados += 1
