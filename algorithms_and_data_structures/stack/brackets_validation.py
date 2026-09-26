from stack import Stack

def validate_brackets(brackets_sequence: str | list[str]):

    if isinstance(brackets_sequence, str):
        brackets_sequence = list(brackets_sequence)
    elif isinstance(brackets_sequence, list):
        pass
    else:
        raise TypeError("The validate_brackets function takes only strings and lists")

    if not brackets_sequence: return True

    open_brackets_list = list("({[")
    close_brackets_list = list(")}]")

    stack = Stack()

    for char in brackets_sequence:
        if char in open_brackets_list:
            stack.push(char)
        elif char in close_brackets_list:
            if stack.is_empty():
                return False
            if close_brackets_list.index(char) != open_brackets_list.index(stack.pop()):
                return False
    
    return stack.is_empty()