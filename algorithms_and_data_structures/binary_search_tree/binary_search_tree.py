from typing import Any
from collections.abc import Iterator, Iterable

_MISSING = object()

class _TreeNode[T: (int, float)]:

    __slots__ = ('value', 'count', 'left_child', 'right_child')

    def __init__(self, value: T, left_child: "_TreeNode[T]" | None = None, right_child: "_TreeNode[T]" | None = None) -> None:
        self.value: T = value
        self.count: int = 1
        self.left_child: _TreeNode[T] | None = left_child
        self.right_child: _TreeNode[T] | None = right_child 

class BinarySearchTree[T: (int, float)]:
    def __init__(self, iterable: Iterable[T] | None = None) -> None:
        self.root: _TreeNode[T] | None = None
        self._size: int = 0

        if iterable is not None:
            for item in iterable:
                self.insert(item)

    def _validate(self, *values: Any) -> None:
        for val in values:
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                raise TypeError(f"BST value must be int or float, got ({type(val)})")

    def _insert_recursive(self, current_node: _TreeNode[T], value: T) -> _TreeNode[T] | None:
        if current_node is None:
            return _TreeNode(value)

        if value < current_node.value:
            current_node.left_child = self._insert_recursive(current_node.left_child, value)
        elif value > current_node.value:
            current_node.right_child = self._insert_recursive(current_node.right_child, value)
        else:
            current_node.count += 1

        return current_node

    def _get_node_recursive(self, current_node: _TreeNode[T], value: T) -> _TreeNode[T] | None:
        if current_node is None:
            return

        if value == current_node.value:
            return current_node

        if value < current_node.value:
            return self._get_node_recursive(current_node.left_child, value)
        elif value > current_node.value:
            return self._get_node_recursive(current_node.right_child, value)
        
        return

    def _in_order_recursive(self, current_node: _TreeNode[T] | None) -> Iterator[T]:
        if current_node is not None:
            yield from self._in_order_recursive(current_node.left_child)

            for _ in range(current_node.count):
                yield current_node.value
            
            yield from self._in_order_recursive(current_node.right_child)

    def _handle_empty(self, default: Any, error_msg: str) -> Any:
        if default is not _MISSING:
            return default
        raise ValueError(error_msg)

    def _find_min_node(self, current_node: _TreeNode[T]) -> _TreeNode[T] | None:
        if current_node is not None:
            if current_node.left_child is not None:
                return self._find_min_node(current_node.left_child)
            return current_node
        return

    def _find_max_node(self, current_node: _TreeNode[T]) -> _TreeNode[T] | None:
        if current_node is not None:
            if current_node.right_child is not None:
                return self._find_max_node(current_node.right_child)
            return current_node
        return

    def _remove_node_recursive(self, current_node: _TreeNode[T] | None, value: T) -> tuple[_TreeNode[T] | None, bool]:
        if current_node is None:
            return None, False

        if value < current_node.value:
            new_left, deleted_node = self._remove_node_recursive(current_node.left_child, value)
            current_node.left_child = new_left
            return current_node, deleted_node
        
        elif value > current_node.value:
            new_right, deleted_node = self._remove_node_recursive(current_node.right_child, value)
            current_node.right_child = new_right
            return current_node, deleted_node

        else:
            if current_node.count > 1:
                current_node.count -= 1
                return current_node, True

            if current_node.left_child is None and current_node.right_child is None:
                return None, True

            if current_node.left_child is None:
                return current_node.right_child, True
            if current_node.right_child is None:
                return current_node.left_child, True

            successor = self._find_min_node(current_node.right_child)

            current_node.value = successor.value
            current_node.count = successor.count

            successor.count = 1

            new_right, _ = self._remove_node_recursive(current_node.right_child, successor.value)
            current_node.right_child = new_right

            return current_node, True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({list(self)})"

    def __str__(self) -> str:
        return f"{list(self)}"
    
    def __iter__(self) -> Iterator[T]:
        return self._in_order_recursive(self.root)

    def __bool__(self) -> bool:
        return self.root is not None

    def __contains__(self, value: T) -> bool:
        try:
            self._validate(value)
            return self._get_node_recursive(self.root, value) is not None
        except TypeError:
            return False

    def __len__(self) -> int:
        return self._size

    def insert(self, value: T) -> None:
        if value is None:
            raise ValueError("value must not be None")
        self._validate(value)

        self.root = self._insert_recursive(self.root, value)
        self._size += 1

    def is_empty(self) -> bool:
        return not self

    def find_min[D](self, default: D =_MISSING) -> T | D:
        if self.is_empty():
            return self._handle_empty(default, "cannot find minimum in an empty BST")

        return self._find_min_node(self.root).value

    def find_max[D](self, default=_MISSING) -> T | D:
        if self.is_empty():
            return self._handle_empty(default, "cannot find maximum in an empty BST")

        return self._find_max_node(self.root).value

    def remove(self, value: T) -> None:
        self._validate(value)
        self.root, is_deleted = self._remove_node_recursive(self.root, value)
        if not is_deleted:
            raise KeyError(f"{value} was not found in the BST")
        self._size -= 1

    def discard(self, value: T) -> bool:
        self._validate(value)
        self.root, is_deleted = self._remove_node_recursive(self.root, value)
        if is_deleted:
            self._size -= 1
        return is_deleted