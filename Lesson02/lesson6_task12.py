import os
import random
import pytest
import logging
from datetime import date, timedelta
from faker import Faker
from functools import wraps
from hamcrest import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


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


fake = Faker('en_US')
url = 'http://localhost/litecart/admin/'
login, pwd = 'admin', 'admin'


class Locators(object):
    LOGIN = By.NAME, 'username'
    PWD = By.NAME, 'password'
    SUBMIT = By.NAME, 'login'


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


# Click on tab
def switch_tab(drv, tab_name):
    drv.find_element(By.CLASS_NAME, 'tabs').find_element_by_partial_link_text(tab_name).click()


# send_keys to the element
def type_in(element, value):
    element.clear()
    element.send_keys(value)


# Select item in the list by text
def select_from(element, value):
    select = Select(element)
    return select.select_by_visible_text(value)


# Add product to Subcategory
def include_table_rows_by_value(drv, header, items):
    t_locator = "//td/strong[contains(.,'{header}')]/following-sibling::div[@class='input-wrapper']".format(header=header)
    table = drv.find_element_by_xpath(t_locator)
    for item in items:
        locator = ".//td[contains(.,'{text}')]/preceding-sibling::td/input[@type='checkbox']".format(text=item)
        table.find_element_by_xpath(locator).click()


def find_column_index(table, column_name):
    locator = './/th[contains(., "{column_name}")]/preceding-sibling::th'
    return len(table.find_elements(By.XPATH, locator.format(column_name=column_name))) + 1


def get_column_values(table, column_name, child=None):
    index = find_column_index(table, column_name)
    assert index != -1, '{column_name} column was not found!'.format(column_name=column_name)
    locator = 'tr.row td:nth-of-type({index})'.format(index=index) + ((' ' + child) if child else '')
    return [el.text for el in table.find_elements(By.CSS_SELECTOR, locator)]


def init(drv, email, password):
    drv.get(url)
    drv.find_element(By.NAME, 'username').send_keys(email)
    drv.find_element(By.NAME, 'password').send_keys(password)
    drv.find_element(By.NAME, 'login').click()


def init_product_creation(drv):
    drv.find_element_by_partial_link_text('Add New Product').click()


def select_menu(drv, text):
    for el in drv.find_elements(By.CSS_SELECTOR, 'li#app-'):
        if el.text == text:
            el.click()
            break


# Find files in folder=import and select 1 of them by random
def choose_image():
    path = os.path.join(os.getcwd(), 'import')
    file_list = []
    for root, dirs, files in os.walk(path, topdown=False):
        for file_name in files:
            file_list.append(os.path.join(root, file_name))
    return random.choice(file_list)


@log
def fill_general_info(drv, enabled, name, code, quantity, img_path, date_valid_from, date_valid_to):
    switch_tab(drv, 'General')
    value = '1' if enabled else '0'
    drv.find_element_by_css_selector("input[type='radio'][value='{value}']".format(value=value)).click()
    type_in(drv.find_element_by_name('name[en]'), name)
    type_in(drv.find_element_by_name('code'), code)
    include_table_rows_by_value(drv, 'Categories', ['Subcategory'])
    include_table_rows_by_value(drv, 'Product Groups', ['Male', 'Female'])
    type_in(drv.find_element_by_name('quantity'), quantity)
    drv.find_element_by_name("new_images[]").send_keys(img_path)
    drv.find_element_by_name('date_valid_from').send_keys(date_valid_from)
    drv.find_element_by_name('date_valid_to').send_keys(date_valid_to)


@log
def fill_information(drv, manufacturer, keywords, short_description, description, title):
    switch_tab(drv, 'Information')
    select_from(drv.find_element_by_name('manufacturer_id'), manufacturer)
    type_in(drv.find_element_by_name('keywords'), keywords)
    type_in(drv.find_element_by_name('short_description[en]'), short_description)
    type_in(drv.find_element_by_class_name('trumbowyg-editor'), description)
    type_in(drv.find_element_by_name('head_title[en]'), title)


@log
def fill_prices(drv, purchase_price, ccy, usd_price):
    switch_tab(drv, 'Prices')
    type_in(drv.find_element_by_name('purchase_price'), purchase_price)
    select_from(drv.find_element_by_name('purchase_price_currency_code'), ccy)
    type_in(drv.find_element_by_name('prices[USD]'), usd_price)


def save_changes(drv):
    drv.find_element_by_name('save').click()
    # if drv.find_elements_by_css_selector('notice-wrapper .error') not found then value = []
    # if []==[] then true
    # else false
    return drv.find_elements_by_css_selector('notice-wrapper .error') == []


def test_add_product(driver):
    init(driver, login, pwd)
    select_menu(driver, 'Catalog')
    print('')
    before = get_column_values(driver.find_element_by_class_name('dataTable'), 'Name')
    logger.debug('Products before: {before}'.format(before=before))

    init_product_creation(driver)

    name = fake.name()
    logger.debug("adding product with name: {name}".format(name=name))

    # class datetime.timedelta([days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]])
    # use format strftime('%m%d%Y')
    fill_general_info(driver, True, name=name, code=fake.ean8(), quantity=random.randint(1, 100),
                      date_valid_from=(date.today() + timedelta(days=random.randint(1, 10))).strftime('%m%d%Y'),
                      date_valid_to=(date.today() + timedelta(days=random.randint(20, 100))).strftime('%m%d%Y'),
                      img_path=choose_image())

    fill_information(driver, manufacturer='ACME Corp.', keywords=fake.words(nb=3),
                     short_description=fake.text(max_nb_chars=50),
                     description=fake.paragraphs(nb=3), title=fake.word() + ' Duck')

    usd_price = random.randint(1, 100)

    fill_prices(driver, purchase_price=random.randint(1, 100), ccy='US Dollars', usd_price=usd_price)

    success = save_changes(driver)
    assert success, "No any errors notifications should be visible!"
    products = get_column_values(driver.find_element_by_class_name('dataTable'), 'Name')
    logger.debug('Products after: {products}'.format(products=products))
    assert_that(products, has_item(name), "Added product should be visible")
