def bubble_sort(arr: list[int|float]) -> list[int|float]:
    
    if arr is None or len(arr) <= 1:
        return arr
    
    sorted_arr = arr[:]

    for step in range(len(sorted_arr)-1):
        swapped = False
        for i in range(len(sorted_arr)-1-step):
            if sorted_arr[i] > sorted_arr[i+1]:
                sorted_arr[i], sorted_arr[i+1] = sorted_arr[i+1], sorted_arr[i]
                swapped = True
        if not swapped:
            break

    return sorted_arr