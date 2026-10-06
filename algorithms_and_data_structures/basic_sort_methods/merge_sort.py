def merge_sort(arr: list[int|float]) -> list[int|float]:
    
    if arr is None or len(arr) <= 1:
        return arr
    
    sorted_arr = arr[:]

    def merge(left: list[int|float]|None, right: list[int|float]|None) -> list[int|float]:
        
        res = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
        
            if left[i] <= right[j]:
                res.append(left[i])
                i += 1
            else:
                res.append(right[j])
                j += 1

        res.extend(left[i:])
        res.extend(right[j:])

        return res
    
    middle = len(sorted_arr) // 2

    left = merge_sort(sorted_arr[:middle])
    right = merge_sort(sorted_arr[middle:])

    return merge(left, right)