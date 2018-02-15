import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'http://localhost/litecart/en/'


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd


def test_stickers_availability(driver):
    driver.get(url)
    print('')
    # Find and print ALL products
    # Select all products by CSS_selector
    for product in driver.find_elements(By.CSS_SELECTOR, 'li.product'):
        # We should check that amount of stickers should be == 1
        # that's why we use find_elements
        stickers = product.find_elements(By.CSS_SELECTOR, 'div.sticker')
        # EXAMPLE: assert len(stickers) == 2, "Only two sticker should be displayed for each product!"
        # len() should return the length (the number of items) of an object.
        # if length != 1 then test should be failed.
        assert len(stickers) == 1, "Only one sticker should be displayed for each product!"
        name = product.find_element(By.CSS_SELECTOR, '.name').text
        manufacturer = product.find_element(By.CSS_SELECTOR, '.manufacturer').text
        sticker = stickers[0].text
        print('Product Name: {name}, Manufacturer: {manufacturer}, Sticker: {sticker}'.format(**locals()))


def test_boxed_stickers(driver):
    driver.get(url)
    print('')
    # find and print ProductGroup name Most Popular, Campaigns, Latest Products
    for productGroupLocator in ('box-most-popular', 'box-campaigns', 'box-latest-products'):
        product_group = driver.find_element(By.ID, productGroupLocator)
        product_group_header = product_group.find_element(By.CSS_SELECTOR, 'h3').text
        print('')
        print('Product Group: "{product_group_header}"'.format(**locals()))
        # find and print products contain in each box
        for product in product_group.find_elements(By.CSS_SELECTOR, 'li.product'):
            # We should check that amount of stickers should be == 1
            # that's why we use find_elements
            stickers = product.find_elements(By.CSS_SELECTOR, 'div.sticker')
            # EXAMPLE: assert len(stickers) == 2, "Only two sticker should be displayed for each product!"
            # len() should return the length (the number of items) of an object.
            # if length != 1 then test should be failed.
            assert len(stickers) == 1, "Only one sticker should be displayed for each product!"
            name = product.find_element(By.CSS_SELECTOR, '.name').text
            manufacturer = product.find_element(By.CSS_SELECTOR, '.manufacturer').text
            # stickers = product.find_elements(By.CSS_SELECTOR, 'div.sticker') return array
            # that's why we use = stickers[0].text
            sticker = stickers[0].text
            print('Product Name: {name}, Manufacturer: {manufacturer}, Sticker: {sticker}'.format(**locals()))