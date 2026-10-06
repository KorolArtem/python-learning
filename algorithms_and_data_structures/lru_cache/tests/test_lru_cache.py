import pytest
from algorithms_and_data_structures.lru_cache.lru_cache import LRUCache

@pytest.fixture
def cache():
    
    return LRUCache(capacity=3)

def test_init_invalid_capacity():

    with pytest.raises(ValueError):
        LRUCache(0)
    with pytest.raises(ValueError):
        LRUCache(-5)

def test_put_and_get_basic(cache):

    cache.put("a", 1)
    cache.put("b", 2)
    
    assert cache.get("a") == 1
    assert cache.get("b") == 2
    assert cache.get("c") is None
    assert cache.get("c", "default") == "default"
    assert len(cache) == 2

def test_eviction_on_capacity(cache):

    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    
    assert len(cache) == 3
    
    cache.put("d", 4)
    assert len(cache) == 3
    assert cache.get("a") is None
    assert cache.get("b") == 2
    assert cache.get("c") == 3
    assert cache.get("d") == 4

def test_get_updates_mru(cache):

    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    
    assert cache.get("a") == 1
    
    cache.put("d", 4)
    
    assert cache.get("b") is None
    assert cache.get("a") == 1
    assert cache.get("c") == 3
    assert cache.get("d") == 4

def test_put_existing_key_updates_value_and_mru(cache):

    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    
    cache.put("a", 100)
    
    cache.put("d", 4)
    
    assert cache.get("a") == 100
    assert cache.get("b") is None
    assert len(cache) == 3

def test_getitem_and_setitem(cache):

    cache["a"] = 1
    cache["b"] = 2
    cache["c"] = 3
    
    assert cache["a"] == 1
    
    cache["d"] = 4
    
    with pytest.raises(KeyError):
        _ = cache["b"]
        
    assert cache["a"] == 1
    assert cache["c"] == 3
    assert cache["d"] == 4

def test_getitem_missing_raises_keyerror(cache):

    with pytest.raises(KeyError):
        _ = cache["missing"]

def test_contains_does_not_update_mru(cache):

    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    
    assert "a" in cache
    
    cache.put("d", 4)
    
    assert "a" not in cache
    assert "b" in cache
    assert "c" in cache
    assert "d" in cache

def test_clear(cache):

    cache.put("a", 1)
    cache.put("b", 2)
    
    cache.clear()
    
    assert len(cache) == 0
    assert cache.get("a") is None
    
    cache.put("c", 3)
    assert cache.get("c") == 3
    assert len(cache) == 1

def test_repr(cache):

    assert isinstance(repr(cache), str)
    
    cache.put("a", 1)
    r = repr(cache)
    assert "LRUCache" in r
    assert "3" in r 
    assert "a" in r

def test_capacity_one():

    tiny_cache = LRUCache(capacity=1)
    
    tiny_cache.put("a", 1)
    assert tiny_cache.get("a") == 1
    
    tiny_cache.put("b", 2)
    assert tiny_cache.get("a") is None
    assert tiny_cache.get("b") == 2

@pytest.mark.parametrize("bad_capacity", ["3", 3.5, True, None, []])

def test_init_type_error(bad_capacity):
    with pytest.raises(TypeError):
        LRUCache(bad_capacity)

def test_store_none_and_falsy_values(cache):

    cache.put("key_none", None)
    cache.put("key_false", False)
    
    assert cache.get("key_none") is None
    assert "key_none" in cache
    assert cache["key_none"] is None
    assert cache.get("key_false") is False

def test_str(cache):

    cache["a"] = 1
    assert str(cache) == "{'a': 1}"

    cache["b"] = 5
    assert str(cache) == "{'b': 5, 'a': 1}"

    _ = cache["a"]
    assert str(cache) == "{'a': 1, 'b': 5}"