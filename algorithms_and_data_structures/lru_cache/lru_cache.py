from algorithms_and_data_structures.doubly_linked_list.doubly_linked_list import DoublyLinkedList
from algorithms_and_data_structures.hash_map.hash_map import HashMap
from functools import wraps
from collections.abc import Callable
from typing import Any

def validate_lru_state[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        
        result = func(*args, **kwargs)

        self = args[0]

        if len(self._map) != len(self._dll):
            raise RuntimeError(
                f"Something went wrong. Doubly Linked List and Hash Map have fallen out of sync.\nDoublyLinkedList: {self._dll}\nHashMap: {self._map}\n"
                f"Last function: {func.__name__}"
            )

        return result
    return wrapper

def check_lru_invariants[T](cls: type[T]) -> type[T]:

    EXCLUDED = {"__init__", "__len__", "__str__", "__repr__", "__contains__"}

    for attr_name, attr_value in list(cls.__dict__.items()):
        if callable(attr_value):
            if (attr_name.startswith("_") and not attr_name.startswith("__")) or attr_name in EXCLUDED:
                continue
            setattr(cls, attr_name, validate_lru_state(attr_value))
    
    return cls

@check_lru_invariants
class LRUCache[K, V]:

    def __init__(self, capacity: int) -> None:
        
        if not isinstance(capacity, int) or isinstance(capacity, bool): # isinstance(True, int) is True :p 
            raise TypeError(f"capacity must be an int, got {type(capacity)}")
        if capacity <= 0:
            raise ValueError(f"capacity must be greater than 0, got ({capacity})")
        self._capacity = capacity

        self._map = HashMap()
        self._dll = DoublyLinkedList()

    def clear(self) -> None:

        self._map = HashMap()
        self._dll = DoublyLinkedList()

    def __getitem__(self, key: K) -> V:

        node = self._map.get(key=key)
        if node is not None:
            k, value = node.value
            self._dll.prepend((k, value)) # perhaps I should add a move_to_front method to DoublyLinkedList, but I dont want to modify the existing class because of the educational cache
            self._dll.remove_node(node=node)
            self._map.put(key=key, value=self._dll.head)
            return value

        raise KeyError(f"There is no {key} in the cache")

    def __setitem__(self, key: K, value: V) -> None:

        existing_node = self._map.get(key, None)

        if existing_node is not None:
            self._dll.remove_node(node=existing_node)

        elif len(self._dll) == self._capacity:
            tail_node = self._dll.tail
            self._map.pop(tail_node.value[0])
            self._dll.remove_node(tail_node)

        self._dll.prepend((key, value))
        self._map.put(key=key, value=self._dll.head)
      
    def put(self, key: K, value: V) -> None:
       
       self[key] = value

    def __contains__(self, key: K) -> bool:

        return key in self._map

    def get(self, key: K, default: Any = None) -> Any:
    
        try:
            return self[key]
        except KeyError:
            return default

    def __len__(self) -> int:

        return len(self._dll)

    def __str__(self) -> str:

        pairs = [f"{repr(k)}: {repr(v)}" for k, v in self._dll]
        return "{" + ", ".join(pairs) + "}"

    def __repr__(self) -> str:
        
        return f"LRUCache(size={len(self)}, capacity={self._capacity}, data={str(self)})"