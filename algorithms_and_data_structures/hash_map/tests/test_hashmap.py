import random
import pytest
from typing import Any
from algorithms_and_data_structures.hash_map.hash_map import HashMap

class CollisionKey:
    def __init__(self, name: str, force_hash: int):
        self.name = name
        self.force_hash = force_hash

    def __hash__(self) -> int:
        return self.force_hash

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CollisionKey):
            return False
        return self.name == other.name

    def __repr__(self):
        return f"K({self.name})"

@pytest.fixture
def empty_map():
    return HashMap()

@pytest.fixture
def populated_map():
    h = HashMap()
    h["a"] = 1
    h["b"] = 2
    h["c"] = 3
    return h

def test_init_defaults(empty_map):
    assert len(empty_map) == 0

def test_init_custom_params():
    h = HashMap(initial_capacity=16, load_factor=0.5, resize_multiplier=3)
    assert len(h) == 0

def test_invalid_arg_types():
    with pytest.raises(TypeError):
        HashMap(initial_capacity="8")
    with pytest.raises(TypeError):
        HashMap(load_factor="0.5")
    with pytest.raises(TypeError):
        HashMap(resize_multiplier="2")

def test_invalid_arg_values():
    with pytest.raises(ValueError, match="initial_capacity"):
        HashMap(initial_capacity=0)
    with pytest.raises(ValueError, match="load_factor"):
        HashMap(load_factor=1.5)
    with pytest.raises(ValueError, match="resize_multiplier"):
        HashMap(resize_multiplier=1.0)

def test_setitem_and_getitem(empty_map):
    empty_map["key1"] = "value1"
    empty_map["key2"] = "value2"

    assert empty_map["key1"] == "value1"
    assert empty_map["key2"] == "value2"
    assert len(empty_map) == 2

def test_setitem_overwrite(populated_map):
    populated_map["a"] = 100
    assert populated_map["a"] == 100
    assert len(populated_map) == 3

def test_overwrite_does_not_grow(empty_map):
    for i in range(100):
        empty_map["same"] = i
    assert len(empty_map) == 1
    assert empty_map["same"] == 99

def test_getitem_missing(empty_map):
    with pytest.raises(KeyError, match="was not found"):
        _ = empty_map["missing_key"]

def test_delitem(populated_map):
    del populated_map["b"]
    assert len(populated_map) == 2
    assert "b" not in populated_map

    with pytest.raises(KeyError):
        _ = populated_map["b"]

def test_delitem_missing(empty_map):
    with pytest.raises(KeyError, match="was not found"):
        del empty_map["missing_key"]

def test_reinsert_after_delete(populated_map):
    del populated_map["a"]
    populated_map["a"] = 42
    assert populated_map["a"] == 42
    assert len(populated_map) == 3

def test_delete_everything_then_reuse(empty_map):
    for i in range(50):
        empty_map[i] = i
    for i in range(50):
        del empty_map[i]
    assert len(empty_map) == 0
    assert empty_map.keys() == []

    empty_map["x"] = 1
    assert empty_map["x"] == 1

def test_put_and_get(empty_map):
    empty_map.put("x", 10)
    assert empty_map.get("x") == 10
    assert empty_map.get("y") is None
    assert empty_map.get("y", "default_val") == "default_val"

def test_pop(populated_map):
    val = populated_map.pop("b")
    assert val == 2
    assert len(populated_map) == 2
    assert "b" not in populated_map

def test_pop_existing_key_ignores_default(populated_map):
    assert populated_map.pop("a", 999) == 1
    assert "a" not in populated_map

def test_pop_missing_with_default(empty_map):
    assert empty_map.pop("missing", 999) == 999
    assert len(empty_map) == 0

def test_pop_missing_without_default(empty_map):
    with pytest.raises(KeyError):
        empty_map.pop("missing")

def test_contains(populated_map, empty_map):
    assert "a" in populated_map
    assert "z" not in populated_map
    assert "a" not in empty_map

def test_len(empty_map, populated_map):
    assert len(empty_map) == 0
    assert len(populated_map) == 3
    empty_map["x"] = 1
    assert len(empty_map) == 1
    del empty_map["x"]
    assert len(empty_map) == 0

def test_keys_values_items(populated_map):
    keys = populated_map.keys()
    values = populated_map.values()
    items = populated_map.items()

    assert set(keys) == {"a", "b", "c"}
    assert set(values) == {1, 2, 3}
    assert set(items) == {("a", 1), ("b", 2), ("c", 3)}

def test_iter(populated_map):
    keys_from_iter = list(populated_map)
    assert set(keys_from_iter) == {"a", "b", "c"}

def test_str_and_repr():
    h = HashMap()
    h["a"] = 1
    assert str(h) == "{'a': 1}"
    assert repr(h) == "HashMap(size=1, capacity=8, data={'a': 1})"
    assert str(HashMap()) == "{}"

def test_resize_and_rehash():
    h = HashMap(initial_capacity=4, load_factor=0.75)

    for i in range(1, 11):
        h[f"key_{i}"] = i * 10

    assert len(h) == 10

    for i in range(1, 11):
        assert h[f"key_{i}"] == i * 10

def test_collisions():
    h = HashMap(initial_capacity=8)

    k1 = CollisionKey("first", 42)
    k2 = CollisionKey("second", 42)
    k3 = CollisionKey("third", 42)

    h[k1] = "val1"
    h[k2] = "val2"
    h[k3] = "val3"

    assert len(h) == 3
    assert h[k1] == "val1"
    assert h[k2] == "val2"
    assert h[k3] == "val3"

    h[k2] = "new_val2"
    assert h[k2] == "new_val2"

    del h[k2]
    assert len(h) == 2
    assert k2 not in h
    assert h[k1] == "val1"
    assert h[k3] == "val3"

    del h[k1]
    assert len(h) == 1
    assert h[k3] == "val3"

    del h[k3]
    assert len(h) == 0

def test_collisions_survive_resize():
    h = HashMap(initial_capacity=2)
    colliding = [CollisionKey(f"k{i}", 7) for i in range(5)]

    for i, key in enumerate(colliding):
        h[key] = i
    for i in range(50):
        h[f"other_{i}"] = i

    assert len(h) == 55
    for i, key in enumerate(colliding):
        assert h[key] == i

def test_multiple_types_as_keys(empty_map):
    empty_map[1] = "int"
    empty_map["string"] = "str"
    empty_map[(1, 2)] = "tuple"
    empty_map[3.14] = "float"

    assert empty_map[1] == "int"
    assert empty_map["string"] == "str"
    assert empty_map[(1, 2)] == "tuple"
    assert empty_map[3.14] == "float"
    assert len(empty_map) == 4

def test_unhashable_key_raises_type_error(empty_map):
    with pytest.raises(TypeError):
        empty_map[[1, 2]] = 1
    with pytest.raises(TypeError):
        _ = empty_map[[1, 2]]
    with pytest.raises(TypeError):
        _ = [1, 2] in empty_map
    with pytest.raises(TypeError):
        empty_map.get([1, 2])
    with pytest.raises(TypeError):
        del empty_map[[1, 2]]
    assert len(empty_map) == 0

def test_falsy_keys_and_values(empty_map):
    empty_map[0] = 0
    empty_map[""] = ""
    empty_map[None] = None

    assert empty_map[0] == 0
    assert empty_map[""] == ""
    assert empty_map[None] is None
    assert len(empty_map) == 3
    assert 0 in empty_map and "" in empty_map and None in empty_map

def test_stored_none_differs_from_missing(empty_map):
    empty_map["k"] = None
    assert "k" in empty_map
    assert empty_map.get("k", "default") is None
    assert empty_map.get("other", "default") == "default"

def test_matches_dict_on_random_operations():
    rng = random.Random(1)
    h = HashMap(initial_capacity=1, load_factor=0.5, resize_multiplier=1.5)
    ref = {}
    key_pool = [0, 1, 2, 3, "a", "b", (1, 2), 1.5, None, 8, 16, 1024, 2048]

    for _ in range(5000):
        op = rng.choice(["set", "set", "del", "pop", "get"])
        key = rng.choice(key_pool)

        if op == "set":
            value = rng.randint(0, 99)
            h[key] = value
            ref[key] = value
        elif op == "del":
            if key in ref:
                del h[key]
                del ref[key]
            else:
                with pytest.raises(KeyError):
                    del h[key]
        elif op == "pop":
            assert h.pop(key, "no") == ref.pop(key, "no")
        else:
            assert h.get(key, "no") == ref.get(key, "no")

        assert len(h) == len(ref)

    assert dict(h.items()) == ref

def test_invalid_shrink_params():
    
    with pytest.raises(ValueError, match="shrink_factor"):
        HashMap(shrink_factor=0.5)
    
    with pytest.raises(ValueError, match="shrink_factor"):
        HashMap(shrink_factor=0.01)

    with pytest.raises(ValueError, match="resize_divider"):
        HashMap(resize_divider=1.0)

def test_capacity_expands_and_shrinks():
    
    h = HashMap(initial_capacity=8, load_factor=0.75, resize_multiplier=2.0, resize_divider=2.0)
    
    assert len(h._buckets) == 8
    
    for i in range(100):
        h[i] = i
        
    assert len(h) == 100
    assert len(h._buckets) >= 128
    max_capacity = len(h._buckets)
    
    for i in range(98):
        del h[i]
        
    assert len(h) == 2
    
    assert len(h._buckets) < max_capacity
    assert len(h._buckets) == 8

def test_never_shrinks_below_initial_capacity():
    
    h = HashMap(initial_capacity=64)
    assert len(h._buckets) == 64
    
    for i in range(10):
        h[i] = i
        
    for i in range(10):
        del h[i]
        
    assert len(h) == 0
    
    assert len(h._buckets) == 64

def test_custom_shrink_and_divider():
    
    h = HashMap(
        initial_capacity=10, 
        load_factor=0.8, 
        shrink_factor=0.2, 
        resize_multiplier=2, 
        resize_divider=3
    )
    
    for i in range(25):
        h[i] = str(i)
        
    expanded_capacity = len(h._buckets)
    assert expanded_capacity >= 40 
    
    for i in range(18):
        del h[i]
        
    assert len(h) == 7
    
    assert len(h._buckets) == 13

def test_params_that_would_rebuild_on_every_operation_are_rejected():
    with pytest.raises(ValueError, match="shrink_factor"):
        HashMap(load_factor=0.4, shrink_factor=0.24)

def test_dynamic_fuzz_resizing():
    h = HashMap(initial_capacity=4)
    
    for i in range(50):
        h[i] = i
    assert len(h._buckets) > 4
    
    for i in range(0, 50, 2):
        del h[i]
    
    for i in range(1, 50, 2):
        assert h[i] == i

    for i in range(50, 100):
        h[i] = i
        
    for i in range(1, 100, 2):
        del h[i]
        
    assert len(h) == 25