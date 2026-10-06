import pytest
import random
from algorithms_and_data_structures.basic_sort_methods.bubble_sort import bubble_sort
from algorithms_and_data_structures.basic_sort_methods.insertion_sort import insertion_sort
from algorithms_and_data_structures.basic_sort_methods.merge_sort import merge_sort
from algorithms_and_data_structures.basic_sort_methods.quick_sort import quick_sort

@pytest.fixture(params=[bubble_sort, insertion_sort, merge_sort, quick_sort])
def sort_func(request):
    return request.param

@pytest.mark.parametrize(
    "input_arr, expected",
    [
        ([], []),                                       
        ([1], [1]),                                     
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),             
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),            
        ([3, 1, 4, 1, 5, 9, 2, 6, 5], [1, 1, 2, 3, 4, 5, 5, 6, 9]), 
        ([-5, 3, -1, 0, 7, -10], [-10, -5, -1, 0, 3, 7]), 
        ([3.14, 2.71, -1.0, 0.0, 1.5], [-1.0, 0.0, 1.5, 2.71, 3.14]),
    ]
)
def test_sort_correctness(sort_func, input_arr, expected):
    assert sort_func(input_arr) == expected

def test_sort_handles_none(sort_func):
    assert sort_func(None) is None

def test_sort_does_not_mutate_original(sort_func):
    original = [5, 2, 9, 1, 5, 6]
    original_copy = original.copy()
    
    sorted_arr = sort_func(original)
    
    assert sorted_arr == [1, 2, 5, 5, 6, 9]
    
    assert original == original_copy
    
    assert id(sorted_arr) != id(original)

def test_sort_large_array(sort_func):
    
    input_arr = [random.randint(-10000, 10000) for _ in range(1000)]
    expected = sorted(input_arr)
    
    assert sort_func(input_arr) == expected

def test_sort_identical_elements(sort_func):

    input_arr = [67] * 100
    expected = [67] * 100

    assert sort_func(input_arr) == expected

def test_sort_zigzag(sort_func):

    input_arr = [1, 100, 2, 99, 3, 98, 4, 97, 5, 96]
    expected = [1, 2, 3, 4, 5, 96, 97, 98, 99, 100]
    
    assert sort_func(input_arr) == expected