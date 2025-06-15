import pytest

def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1

def test_is_instance():
    assert isinstance('this is sdfsf', str)
    assert not isinstance('10',int)

def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' == 'wosdfsd') is False

def test_type():
    assert type ('hello' is str)
    assert type('hello' is not int)

def test_greater_and_less_than():
    assert 4<7
    assert 10>5

def test_list():
    num_list = [1,2,34,56,6]
    any_list = [False, False]
    assert 1 in num_list
    assert 10 not in num_list
    assert all(num_list)
    assert not any(any_list)

