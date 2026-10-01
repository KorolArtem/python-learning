from algorithms_and_data_structures.stack.stack import Stack
import re

def evaluate_expression(expression: str) -> float:
    if not isinstance(expression, str):
        raise TypeError("This function takes string argument only")

    tokens = re.findall(r"\d+(?:\.\d+)?|\S", expression)

    numbers_stack = Stack()
    operators_stack = Stack()

    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}

    def calc(a: float, b: float, op: str) -> float:
        if op == "+": return a + b
        if op == "-": return a - b
        if op == "*": return a * b
        if op == "/":
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            return a / b
        raise ValueError(f"Unknown operator {op}")

    def apply_operator():
        if operators_stack.is_empty() or numbers_stack.is_empty():
            raise ValueError("Expression is wrong")
        
        op = operators_stack.pop()
        b = numbers_stack.pop()
        
        if numbers_stack.is_empty():
            raise ValueError("Expression is wrong")
        a = numbers_stack.pop()
        
        result = calc(a, b, op)
        numbers_stack.push(result)

    for token in tokens:
        try:
            val = float(token)
            numbers_stack.push(val)
            continue
        except ValueError:
            pass

        if token == "(":
            operators_stack.push(token)

        elif token == ")":
            while not operators_stack.is_empty() and operators_stack.top() != "(":
                apply_operator()
            
            if operators_stack.is_empty():
                raise ValueError("Mismatched brackets")
            operators_stack.pop()

        elif token in precedence:
            while (
                not operators_stack.is_empty()
                and operators_stack.top() in precedence
                and precedence[operators_stack.top()] >= precedence[token]
            ):
                apply_operator()
            operators_stack.push(token)

        else:
            raise ValueError(f"'{token}' is unsupported")

    while not operators_stack.is_empty():
        if operators_stack.top() == "(":
            raise ValueError("Mismatched brackets")
        apply_operator()

    if numbers_stack.is_empty():
        raise ValueError("Expression is empty")

    result = numbers_stack.pop()

    if not numbers_stack.is_empty():
        raise ValueError("Expression is wrong")

    return result