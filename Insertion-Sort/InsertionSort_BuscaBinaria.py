def binary_search(arr, val, start, end):
    if start == end:
        if arr[start] > val:
            return start
        else:
            return start+1

    if start > end:
        return start

    mid = (start+end)//2
    if arr[mid] < val:
        return binary_search(arr, val, mid+1, end, comparacao=comparacao, troca=troca)
    elif arr[mid] > val:
        return binary_search(arr, val, start, mid-1, comparacao=comparacao, troca=troca)
    else:
        return mid


def insertion_sort_bin(arr):
    for i in range(1, len(arr)):
        val = arr[i]
        j = binary_search(arr, val, 0, i-1, comparacao=comparacao, troca=troca)

        for k in range(i, j, -1):
          arr[k] = arr[k - 1]

        arr[j] = val
    return arr
