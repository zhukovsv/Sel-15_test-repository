
import random
import pytest
import logging
from selenium.webdriver.support import expected_conditions as EC
from functools import wraps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


# https://docs.python.org/3/howto/logging.html
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)


# https://pythonworld.ru/osnovy/dekoratory.html
# https://docs.python.org/3/howto/logging.html
# Function with @log should be logged
def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug('Calling {fName} with {locals}'.format(fName=func.__name__, locals=locals()))
        return func(*args, **kwargs)
    return wrapper


url = 'http://localhost/litecart/en/'


class Locators(object):
    POPULAR_GROUP = By.ID, 'box-most-popular'
    PRODUCT_SIZE = By.NAME, 'options[Size]'
    PRODUCT_AMOUNT = By.CSS_SELECTOR, '#cart .quantity'
    ADD_TO_BASKET_BUTTON = By.NAME, 'add_cart_product'
    CHECKOUT = By.PARTIAL_LINK_TEXT, 'Checkout'
    BACK = By.PARTIAL_LINK_TEXT, '<< Back'
    HOME = By.CLASS_NAME, 'fa-home'
    BASKET_TEXT = By.TAG_NAME, 'em'
    BASKET_TABLE = By.CLASS_NAME, 'dataTable'
    PRODUCTS_TO_REMOVE = By.CSS_SELECTOR, 'li.item'
    REMOVE_FROM_BASKET_BUTTON = By.CSS_SELECTOR, '.item [name="remove_cart_item"]'


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


# Add 3 products to basket
# Go to checkout
# Remove all added product step by step - always remove 1 product from the list
# Check table disappearing and text="There are no items in your cart." appearing
def test_product_basket_workflow(driver):
    print('')
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    for duck in generate_random_product_list(driver):
        add_product_to_basket(driver, duck)

    go_to_checkout(driver)

    # if use there find_element instead Of find_elements then error
    # find_element raise an exception in case of finding nothing
    # in while use find_elements to make your life better :-)
    while driver.find_elements(*Locators.PRODUCTS_TO_REMOVE):
        wait.until(EC.element_to_be_clickable(Locators.PRODUCTS_TO_REMOVE))
        # Stop changing product's items in control by clicking on it
        driver.find_element(*Locators.PRODUCTS_TO_REMOVE).click()
        # Remove first product
        remove_first_product_from_basket(driver)

    wait.until(EC.text_to_be_present_in_element(Locators.BASKET_TEXT, 'There are no items in your cart.'))
    assert wait.until(EC.text_to_be_present_in_element(Locators.BASKET_TEXT, 'There are no items in your cart.')), \
        "Empty cart text missed"

    go_to_back(driver)

    if int(driver.find_element(*Locators.PRODUCT_AMOUNT).text) == 0:
        logger.info("All products were removed from the basket.")


# random.sample(population, k)
# Return a k length list of unique elements
# chosen from the population sequence. Used for random sampling without replacement.
def generate_random_product_list(drv):
    box = drv.find_element(*Locators.POPULAR_GROUP)
    product_list = [el.text for el in box.find_elements(By.CLASS_NAME, 'name')]
    return random.sample(product_list, min(len(product_list), 3))


#@log
def add_product_to_basket(drv, product):
    logger.info("Adding product: {product}".format(product=product))
    before = int(drv.find_element(*Locators.PRODUCT_AMOUNT).text)
    open_product(drv, product)
    if is_element_present(drv, Locators.PRODUCT_SIZE):
        select_from(drv.find_element(*Locators.PRODUCT_SIZE), 'Small')
    wait = WebDriverWait(drv, 10)
    wait.until(EC.element_to_be_clickable(Locators.ADD_TO_BASKET_BUTTON))
    drv.find_element(*Locators.ADD_TO_BASKET_BUTTON).click()
    # wait until PRODUCT_AMOUNT changed to (before + 1))
    wait.until(lambda d: d.find_element(*Locators.PRODUCT_AMOUNT).text == str(before + 1))
    go_to_home(drv)


def open_product(drv, product):
    wait = WebDriverWait(drv, 10)
    box = drv.find_element(*Locators.POPULAR_GROUP)
    box.find_element(By.XPATH, "//li[contains(@class, 'product')]/a/div[contains(., '" + product + "')]").click()
    wait.until(EC.presence_of_element_located((By.ID, 'box-product')))


def go_to_checkout(drv):
    wait = WebDriverWait(drv, 10)
    drv.find_element(*Locators.CHECKOUT).click()
    wait.until(EC.title_is('Checkout | My Store'))


def go_to_back(drv):
    wait = WebDriverWait(drv, 10)
    drv.find_element(*Locators.BACK).click()
    wait.until(EC.title_is('Online Store | My Store'))


def select_from(element, value):
    if value:
        select = Select(element)
        return select.select_by_visible_text(value)


def is_element_present(drv, locator):
    return len(drv.find_elements(*locator)) > 0


def remove_first_product_from_basket(drv):
    wait = WebDriverWait(drv, 10)
    product_to_remove = drv.find_element(By.TAG_NAME, 'strong').get_attribute('textContent')
    logger.info("Removing product: {product_to_remove}".format(product_to_remove=product_to_remove))
    table = drv.find_element(*Locators.BASKET_TABLE)
    remove = drv.find_element(*Locators.REMOVE_FROM_BASKET_BUTTON)
    remove.click()
    wait.until(EC.staleness_of(remove))
    wait.until(EC.staleness_of(table))


def go_to_home(drv):
    wait = WebDriverWait(drv, 10)
    drv.find_element(*Locators.HOME).click()
    wait.until(EC.title_is('Online Store | My Store'))
