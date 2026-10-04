from typing import Any
from collections.abc import Iterator

_MISSING = object()

class _HashNode[K,V]:
    
    def __init__(self, key: K, value: V, next_node: "_HashNode[K,V]" | None = None) -> None:
        self.key: K = key
        self.value: V = value
        self.next: _HashNode[K,V] | None = next_node

class HashMap[K,V]:

    def _check_arg_types(self, *args: tuple[Any, tuple[type, ...]]) -> None:
        
        for value, expected_types in args:
            if not isinstance(value, expected_types):
                expected_names = " or ".join(t.__name__ for t in expected_types)
                actual_name = type(value).__name__
                
                raise TypeError(f"Invalid argument type. Expected: {expected_names}, got: {actual_name} (value={value})")

    def __init__(self, initial_capacity: int = 8, load_factor: float = 0.75, shrink_factor: float = -1, resize_multiplier: float | int = 2.0, resize_divider: float | int = 2) -> None:

        self._check_arg_types(
            (initial_capacity, (int,)), 
            (load_factor, (float,)), 
            (resize_multiplier, (int, float)))

        if initial_capacity <= 0:
            raise ValueError(f"Invalid initial_capacity ({initial_capacity}). initial_capacity must be greater than 0")
        if not (0.1 < load_factor < 1):
            raise ValueError(f"Invalid load_factor ({load_factor}). load_factor must be strictly between 0.1 and 1")
        if not (1.1 < resize_multiplier):
            raise ValueError(f"Invalid resize_multiplier ({resize_multiplier}). resize_multiplier must be greater than 1.1")
        if shrink_factor < 0:
            self.__shrink_factor = load_factor / 4
        elif not (0.025 < shrink_factor < 0.25):
            raise ValueError(f"Invalid shrink_factor ({shrink_factor}). shrink_factor must be strictly between 0.025 and 0.25")
        else:
            self.__shrink_factor = shrink_factor
        if not (1.1 < resize_divider):
            raise ValueError(f"Invalid resize_divider ({resize_divider}). resize_divider must be greater than 1.1")

        if self.__shrink_factor * resize_divider >= load_factor:
            raise ValueError("(shrink_factor * resize_divider) must be less than load_factor, otherwise the map would rebuild itself on almost every operation")

        self.__load_factor = load_factor
        self.__resize_multiplier = resize_multiplier
        self.__resize_divider = resize_divider
        self._size = 0
        self.__initial_capacity = initial_capacity

        self._buckets: list[_HashNode[K, V] | None] = [None] * initial_capacity

        self.__expand_threshold = int(initial_capacity * load_factor)
        self.__shrink_threshold = -1

    def _find_bucket_index(self, key: K, buckets: list[_HashNode[K, V] | None] | None = None) -> int:

        if buckets is None:
            buckets = self._buckets

        if not isinstance(buckets, list):
            raise TypeError("buckets must be a list")
        
        return hash(key) % len(buckets) # could have tweaked it slightly by incorporating bitwise explosions based on the golden ratio into the formula to prevent the clustering of multiples of 2, but that would be overkill and unnecessary math (found it in the internet and dont want to get with it)
       
    def _find_node_in_bucket(self, key: K, bucket_head: _HashNode[K, V] | None) -> _HashNode[K, V] | None:

        if not bucket_head:
            return None

        current_node = bucket_head
        while current_node:
            if current_node.key == key:
                return current_node
            current_node = current_node.next
        
        return None

    def __insert(self, key: K, value: V, buckets: list[_HashNode[K, V] | None] | None = None) -> bool:

        if buckets is None:
            buckets = self._buckets
    
        bucket_index = self._find_bucket_index(key=key, buckets=buckets)

        if buckets[bucket_index]:

            current_node = buckets[bucket_index]
            while current_node:
                if current_node.key == key:
                    current_node.value = value
                    return False
                if current_node.next is None:
                    break
                current_node = current_node.next

            current_node.next = _HashNode(key=key, value=value)
            return True

        else:
            buckets[bucket_index] = _HashNode(key=key, value=value)
            return True

    def _resize_and_rehash(self, elements_count_delta: int) -> None:

        if not isinstance(elements_count_delta, int):
            raise TypeError(f"elements_count_delta must be an int, got {type(elements_count_delta)}")

        self._size += elements_count_delta

        current_capacity = len(self._buckets)
        new_capacity = current_capacity

        if self._size >= self.__expand_threshold:
            new_capacity = max( (current_capacity + 1), (int(current_capacity * self.__resize_multiplier)) ) 

        elif self._size <= self.__shrink_threshold and current_capacity > self.__initial_capacity:
            new_capacity = max(self.__initial_capacity, int(current_capacity / self.__resize_divider))

        if new_capacity == current_capacity:
            return

        self.__expand_threshold = int(new_capacity * self.__load_factor)

        if new_capacity > self.__initial_capacity:
            self.__shrink_threshold = int(new_capacity * self.__shrink_factor)
        else:
            self.__shrink_threshold = -1

        new_buckets = [None] * new_capacity

        for head in self._buckets:
            if head is None:
                continue
            current = head
            while current:
                self.__insert(key=current.key, value=current.value, buckets=new_buckets)
                current = current.next

        self._buckets = new_buckets

    def __setitem__(self, key: K, value: V) -> None:

        if self.__insert(key=key, value=value):
            self._resize_and_rehash(1)

    def __getitem__(self, key: K) -> V:

        bucket_index = self._find_bucket_index(key)
        node = self._find_node_in_bucket(key, self._buckets[bucket_index])

        if node:
            return node.value

        raise KeyError(f"Key ({key}) was not found in HashMap")

    def __delitem__(self, key: K) -> None:

        bucket_index = self._find_bucket_index(key=key)
        current_node = self._buckets[bucket_index]

        if current_node:
            if current_node.key == key:
                self._buckets[bucket_index] = current_node.next
                self._resize_and_rehash(-1)
                return

            while current_node.next:
                if current_node.next.key == key:
                    current_node.next = current_node.next.next
                    self._resize_and_rehash(-1)
                    return
                current_node = current_node.next

        raise KeyError(f"Key ({key}) was not found in HashMap")

    def put(self, key: K, value: V) -> None:
        
        self[key] = value

    def get(self, key: K, default: Any = None) -> Any:

        bucket_index = self._find_bucket_index(key)
        node = self._find_node_in_bucket(key, self._buckets[bucket_index])

        if node is None:
            return default
        return node.value 

    def pop(self, key: K, default: Any = _MISSING) -> Any:

        try:
            value = self[key]
            del self[key]
            return value
        
        except KeyError:
            if default is not _MISSING:
                return default
            raise

    def __len__(self) -> int:
        
        return self._size

    def __contains__(self, key: K) -> bool:

        bucket_index = self._find_bucket_index(key)
        return self._find_node_in_bucket(key, self._buckets[bucket_index]) is not None

    def _get_nodes(self) -> Iterator[_HashNode[K, V]]:

        for bucket_head in self._buckets:
            current_node = bucket_head

            while current_node:
                yield current_node
                current_node = current_node.next

    def keys(self) -> list[K]:

        return [node.key for node in self._get_nodes()]


    def values(self) -> list[V]:

        return [node.value for node in self._get_nodes()]

    def items(self) -> list[tuple[K, V]]:

        return [(node.key, node.value) for node in self._get_nodes()]

    def __iter__(self) -> Iterator[K]:

        for node in self._get_nodes():
            yield node.key

    def __str__(self) -> str:
    
        pairs = [f"{repr(node.key)}: {repr(node.value)}" for node in self._get_nodes()]
        return "{" + ", ".join(pairs) + "}"
    
    def __repr__(self) -> str:
        
        return f"HashMap(size={self._size}, capacity={len(self._buckets)}, data={str(self)})"