# Implement a custom Stack class supporting push, pop, top, get_min, clear and is_empty, with all operations running in constant O(1) time complexity.

from typing import Any

class Stack:
    
    def __init__(self) -> None:
        self._stack = []
        self._min_el = []

    def push(self, item: int | float) -> None:
        if not isinstance(item, (int, float)): raise TypeError("This stack only supports int and float elements")
        if not self._stack:
            self._min_el.append(item)
        else:
            if item <= self._min_el[-1]: self._min_el.append(item)
        self._stack.append(item)

    def top(self) -> int | float:
        if self._stack: return self._stack[-1]
        else: raise IndexError("This stack is empty")

    def get_min(self) -> int | float:
        if self._stack: return self._min_el[-1]
        else: raise IndexError("This stack is empty")

    def pop(self) -> int | float:
        if not self._stack: raise IndexError("This stack is empty")
        if self._min_el[-1] == self._stack[-1]:
            self._min_el.pop()
        return self._stack.pop()

    def is_empty(self) -> bool:
        return len(self._stack) == 0

    def clear(self) -> None:
        self._stack.clear()
        self._min_el.clear()