import pytest
from .data_providers import valid_products, partially_invalid_products, invalid_products
# Use https://habrahabr.ru/post/269759/ for more info
# valid_products = all tests should be passed
# partially_invalid_products = 1 test should be passed, 1 test should be failed
# invalid_products = all tests should be failed, BUT according to @pytest.mark.xfail() this should be ignored
""" According to those DataSets we should have next results: Tests Failed: 4 passed, 1 failed, 2 ignored"""


# https://habrahabr.ru/post/269759/
# pass data set with all valid products
# all tests should be passed
@pytest.mark.parametrize("products", valid_products, ids=[repr(x) for x in valid_products])
def test_cart_workflow_all_test_passed(app, products):
    old_size = app.get_current_cart_size()
    diff = 0
    expected = []
    for p in products:
        expected.append(p.name)
        app.add_product_to_cart(p)
        diff += p.amount
    new_size = app.get_current_cart_size()
    assert new_size == old_size + diff
    assert sorted(app.get_products_in_cart()) == sorted(expected)
    app.clear_cart()
    assert app.get_products_in_cart() == []
    assert app.get_current_cart_size() == 0


# https://habrahabr.ru/post/269759/
# data set with partially valid products
# 1 test should be passed
# 1 test should be failed
@pytest.mark.parametrize("products", partially_invalid_products, ids=[repr(x) for x in partially_invalid_products])
def test_cart_workflow_all_tests_partially_passed(app, products):
    old_size = app.get_current_cart_size()
    diff = 0
    expected = []
    for p in products:
        expected.append(p.name)
        app.add_product_to_cart(p)
        diff += p.amount
    new_size = app.get_current_cart_size()
    assert new_size == old_size + diff
    assert sorted(app.get_products_in_cart()) == sorted(expected)
    app.clear_cart()
    assert app.get_products_in_cart() == []
    assert app.get_current_cart_size() == 0


# https://habrahabr.ru/post/269759/
# data set with all invalid/not exists products
# all tests should be failed
# but according to @pytest.mark.xfail() this should be ignored by pytest
@pytest.mark.xfail()
@pytest.mark.parametrize("products", invalid_products, ids=[repr(x) for x in invalid_products])
def test_cart_workflow_all_tests_failed_but_ignored(app, products):
    old_size = app.get_current_cart_size()
    diff = 0
    expected = []
    for p in products:
        expected.append(p.name)
        app.add_product_to_cart(p)
        diff += p.amount
    new_size = app.get_current_cart_size()
    assert new_size == old_size + diff
    assert sorted(app.get_products_in_cart()) == sorted(expected)
    app.clear_cart()
    assert app.get_products_in_cart() == []
    assert app.get_current_cart_size() == 0
