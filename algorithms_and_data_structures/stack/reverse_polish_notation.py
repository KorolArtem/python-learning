from algorithms_and_data_structures.stack.stack import Stack

def calculate_expression(expression: str | list[str]) -> float:
    
    if isinstance(expression, str):
        normalized = expression.replace(",", " ").split()
    elif isinstance(expression, list):
        normalized = expression
    else:
        raise TypeError("The calculate_expression function takes only strings and lists")

    stack = Stack()

    for item in normalized:
        if item in ("+", "-", "*", "/"):
            
            if stack.is_empty():
                raise ValueError(f"The expression is incorrect")
            b = stack.pop()
            
            if stack.is_empty():
                raise ValueError(f"The expression is incorrect")
            a = stack.pop()

            if item == "+": 
                stack.push(a + b)
            elif item == "-": 
                stack.push(a - b)
            elif item == "*": 
                stack.push(a * b)
            elif item == "/": 
                if b == 0: 
                    raise ZeroDivisionError("Division by zero")
                stack.push(int(a / b))

        elif isinstance(item, int) or isinstance(item, str) and item.removeprefix("-").removeprefix("+").isdigit():
            stack.push(int(item))
        else:
            raise TypeError(f"Unexpected element in expression: {item}")

    if stack.is_empty():
        raise ValueError("The expression is empty or incorrect")

    result = stack.pop()

    if not stack.is_empty():
        raise ValueError("The expression is incorrect (too many numbers)")

    return result