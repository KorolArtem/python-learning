from stack import Stack

def validate_palindrome(word: str | list[str]):

    if not word: raise ValueError("The word must have at least one symbol")
    
    if isinstance(word, str):
        word = list(word)

    stack = Stack()
    mid = len(word) // 2
    
    for i in range(mid):
            stack.push(word[i])

    start_second_half = mid + 1 if len(word) % 2 != 0 else mid

    for i in range(start_second_half, len(word)):
        if stack.pop() != word[i]:
            return False

    return True