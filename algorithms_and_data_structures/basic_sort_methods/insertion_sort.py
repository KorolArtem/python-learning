def insertion_sort(arr: list[int|float]) -> list[int|float]:

    if arr is None or len(arr) <= 1:
            return arr

    sorted_arr = arr[:]

    for i in range(1, len(sorted_arr)):
        key = sorted_arr[i]
        j = i - 1

        while j >= 0 and sorted_arr[j] > key:
            sorted_arr[j+1] = sorted_arr[j]
            j -= 1

        sorted_arr[j+1] = key
    
    return sorted_arr