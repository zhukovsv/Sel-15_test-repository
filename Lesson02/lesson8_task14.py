import logging
from functools import wraps

import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# https://docs.python.org/3/howto/logging.html
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)

URL = 'http://localhost/litecart/admin/'


class Helper(object):
    def __init__(self, drv):
        self._wd = drv
        # after init browser should be maximized
        self._wd.maximize_window()
        # after init object should have property wait = WebDriverWait(drv, 20)
        self._wait = WebDriverWait(drv, 20)

    @property
    def wd(self):
        return self._wd

    @property
    def wait(self):
        return self._wait


# https://pythonworld.ru/osnovy/dekoratory.html
# https://docs.python.org/3/howto/logging.html
# Function with @log should be logged
def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug('Calling {fName} with {locals}'.format(fName=func.__name__, locals=locals()))
        return func(*args, **kwargs)
    return wrapper


class Locators(object):
    LOGIN = By.NAME, 'username'
    PWD = By.NAME, 'password'
    LOGIN_BUTTON = By.NAME, 'login'
    EXTERNAL_LINK = By.CLASS_NAME, 'fa-external-link'


@pytest.fixture
def driver(request):
    helper = Helper(webdriver.Chrome())
    request.addfinalizer(helper.wd.quit)
    return helper


def test_open_external_links(driver):
    print('')
    init(driver, 'admin', 'admin')
    select_menu(driver, 'Countries')
    init_add_country(driver)
    for link in driver.wd.find_elements(*Locators.EXTERNAL_LINK):
        # remember parent window handle
        parent_window = driver.wd.current_window_handle
        go_to_external_link(driver, link)
        close_active_window(driver)
        # go to parent window
        go_to_window(driver, parent_window)


def init(drv, login_value, psw_value):
    drv.wd.get(URL)
    drv.wd.find_element(*Locators.LOGIN).send_keys(login_value)
    drv.wd.find_element(*Locators.PWD).send_keys(psw_value)
    drv.wd.find_element(*Locators.LOGIN_BUTTON).click()


def select_menu(drv, text):
    xpath = '//*[@class="name" and text()="{text}"]/ancestor::li[@id="app-"]'.format(text=text)
    drv.wd.find_element(By.XPATH, xpath).click()


def init_add_country(drv):
    drv.wd.find_element_by_partial_link_text('Add New Country').click()
    drv.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), 'Add New Country'))


def go_to_external_link(drv, element):
    old_windows = drv.wd.window_handles
    element.click()
    drv.wait.until(EC.new_window_is_opened(old_windows))
    # drv.wd.window_handles returns list
    # that's why we should use list[0] or list.pop() to remove len fron the list
    # new_window = [x for x in drv.wd.window_handles if x not in old_windows].pop()
    new_window = [x for x in drv.wd.window_handles if x not in old_windows][0]
    go_to_window(drv, new_window)


def close_active_window(drv):
    drv.wd.close()


def go_to_window(drv, handle):
    drv.wd.switch_to_window(handle)
    logger.info("Page's title: {}".format(drv.wd.title))




