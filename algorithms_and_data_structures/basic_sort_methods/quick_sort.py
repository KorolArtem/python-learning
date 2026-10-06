import random

def quick_sort(arr: list[int|float]) -> list[int|float]:
    
    if arr is None or len(arr) <= 1:
        return arr
    
    pivot = random.choice(arr)
    
    left = []
    middle = []
    right = []
    
    for x in arr:
        if x < pivot:
            left.append(x)
        elif x > pivot:
            right.append(x)
        else:
            middle.append(x)
            
    return quick_sort(left) + middle + quick_sort(right)