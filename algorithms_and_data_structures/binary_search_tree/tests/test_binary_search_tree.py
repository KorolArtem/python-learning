import pytest
import random
from algorithms_and_data_structures.binary_search_tree.binary_search_tree import BinarySearchTree

@pytest.fixture
def empty_tree():
    return BinarySearchTree()

@pytest.fixture
def bst():
    tree = BinarySearchTree()
    for val in [10, 5, 15, 3, 7, 12, 18]:
        tree.insert(val)
    return tree

@pytest.fixture
def dup_bst():
    tree = BinarySearchTree()
    for val in [5, 5, 3, 7, 7, 7]:
        tree.insert(val)
    return tree

def test_empty_tree_properties(empty_tree):
    assert len(empty_tree) == 0
    assert empty_tree.is_empty() is True
    assert bool(empty_tree) is False
    assert list(empty_tree) == []

def test_populated_tree_properties(bst):
    assert len(bst) == 7
    assert bst.is_empty() is False
    assert bool(bst) is True
    assert list(bst) == [3, 5, 7, 10, 12, 15, 18]

def test_duplicates_properties(dup_bst):
    assert len(dup_bst) == 6
    assert list(dup_bst) == [3, 5, 5, 7, 7, 7]

def test_contains(empty_tree, bst, dup_bst):
    assert 10 not in empty_tree
    
    assert 10 in bst
    assert 3 in bst
    assert 18 in bst
    assert 99 not in bst

    assert 5 in dup_bst
    assert 7 in dup_bst

def test_find_min(empty_tree, bst, dup_bst):
    assert bst.find_min() == 3
    assert dup_bst.find_min() == 3

    assert empty_tree.find_min(default="empty") == "empty"
    
    with pytest.raises((ValueError, KeyError, IndexError)): 
        empty_tree.find_min()

def test_find_max(empty_tree, bst, dup_bst):
    assert bst.find_max() == 18
    assert dup_bst.find_max() == 7

    assert empty_tree.find_max(default=None) is None

    with pytest.raises((ValueError, KeyError, IndexError)): 
        empty_tree.find_max()

def test_remove_leaf(bst):
    bst.remove(3)
    assert len(bst) == 6
    assert list(bst) == [5, 7, 10, 12, 15, 18]
    
    bst.remove(18)
    assert list(bst) == [5, 7, 10, 12, 15]

def test_remove_node_with_one_child(bst):
    bst.remove(3)
    
    bst.remove(5)
    assert len(bst) == 5
    assert list(bst) == [7, 10, 12, 15, 18]

def test_remove_node_with_two_children(bst):
    bst.remove(5)
    assert len(bst) == 6
    assert list(bst) == [3, 7, 10, 12, 15, 18]

    bst.remove(15)
    assert len(bst) == 5
    assert list(bst) == [3, 7, 10, 12, 18]

def test_remove_root(bst):
    bst.remove(10)
    assert len(bst) == 6
    assert list(bst) == [3, 5, 7, 12, 15, 18]

def test_remove_duplicates(dup_bst):
    dup_bst.remove(7)
    assert len(dup_bst) == 5
    assert list(dup_bst) == [3, 5, 5, 7, 7]

    dup_bst.remove(7)
    dup_bst.remove(7)
    assert len(dup_bst) == 3
    assert list(dup_bst) == [3, 5, 5]
    assert 7 not in dup_bst

def test_remove_missing_raises(bst):
    with pytest.raises((ValueError, KeyError)):
        bst.remove(999)

def test_discard(bst, dup_bst):
    assert bst.discard(999) is False
    assert len(bst) == 7

    assert bst.discard(10) is True
    assert len(bst) == 6
    assert list(bst) == [3, 5, 7, 12, 15, 18]

    assert dup_bst.discard(5) is True
    assert len(dup_bst) == 5
    assert list(dup_bst) == [3, 5, 7, 7, 7]

def test_str_and_repr(bst):
    s = str(bst)
    r = repr(bst)
    
    assert s == "[3, 5, 7, 10, 12, 15, 18]"
    assert r == "BinarySearchTree([3, 5, 7, 10, 12, 15, 18])"

def test_clear_tree_by_removing_all(bst):
    for val in [10, 5, 15, 3, 7, 12, 18]:
        bst.remove(val)
        
    assert len(bst) == 0
    assert bst.is_empty() is True
    assert list(bst) == []
    assert bool(bst) is False

def test_matches_python_list_on_random_operations():
    rng = random.Random(676767)
    
    bst = BinarySearchTree()
    ref_list = []
    
    value_pool = [rng.randint(-676767, 676767) for _ in range(67)]
    
    for _ in range(6767):
        op = rng.choice(["insert", "insert", "insert", "remove", "discard", "contains", "min_max"])
        val = rng.choice(value_pool)
        
        if op == "insert":
            bst.insert(val)
            ref_list.append(val)
            
        elif op == "remove":
            if val in ref_list:
                bst.remove(val)
                ref_list.remove(val)
            else:
                with pytest.raises(KeyError):
                    bst.remove(val)
                    
        elif op == "discard":
            expected_deleted = val in ref_list
            assert bst.discard(val) == expected_deleted
            if expected_deleted:
                ref_list.remove(val)
                
        elif op == "contains":
            assert (val in bst) == (val in ref_list)
            
        elif op == "min_max":
            if not ref_list:
                with pytest.raises(ValueError):
                    bst.find_min()
                with pytest.raises(ValueError):
                    bst.find_max()
            else:
                assert bst.find_min() == min(ref_list)
                assert bst.find_max() == max(ref_list)
        
        assert len(bst) == len(ref_list)

    assert list(bst) == sorted(ref_list)