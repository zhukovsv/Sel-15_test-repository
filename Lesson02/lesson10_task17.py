import logging
import pytest
from hamcrest import assert_that, empty
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)

URL = 'http://localhost/litecart/admin/'
PRODUCT_URL = 'http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1'


class Helper(object):
    def __init__(self, drv):
        self._wd = drv
        self._wd.maximize_window()
        self._wait = WebDriverWait(drv, 20)

    @property
    def wd(self):
        return self._wd

    @property
    def wait(self):
        return self._wait


class Locators(object):
    LOGIN = By.NAME, 'username'
    PWD = By.NAME, 'password'
    LOGIN_BUTTON = By.NAME, 'login'


@pytest.fixture
def driver(request):
    helper = Helper(webdriver.Chrome())
    request.addfinalizer(helper.wd.quit)
    return helper


def test_browser_logs_on_product_opening_step_by_step(driver):
    print('')
    init(driver)
    logger.debug('Available log types: {}'.format(driver.wd.log_types))
    open_product_page(driver)
    links = get_products_links(driver)
    for href in links:
        open_product_page(driver)
        init_product_edit_by_href(driver, href)
        assert_that(driver.wd.get_log("browser"), empty(), "Browser log should be empty")


def test_browser_logs_on_product_opening(driver):
    print('')
    init(driver)
    logger.debug('Available log types: {}'.format(driver.wd.log_types))
    open_product_page(driver)
    links = get_products_links(driver)
    browser_logs = {}
    for href in links:
        open_product_page(driver)
        init_product_edit_by_href(driver, href=href)
        logs = driver.wd.get_log("browser")
        if logs:
            browser_logs[href] = logs
    assert_that(browser_logs.keys(), empty(), "Logs should be empty. Current: {}".format(browser_logs))


def init(drv):
    drv.wd.get(URL)
    email, password = 'admin', 'admin'
    drv.wd.find_element(*Locators.LOGIN).send_keys(email)
    drv.wd.find_element(*Locators.PWD).send_keys(password)
    drv.wd.find_element(*Locators.LOGIN_BUTTON).click()


def get_products_links(drv):
    # not(i) to skip 'Edit' link
    locator = By.XPATH, '//a[contains(@href, "product_id") and not(i)]'
    # return list of links (attribute = href)
    return [el.get_attribute('href') for el in drv.wd.find_elements(*locator)]


def open_product_page(drv):
    drv.wd.get(PRODUCT_URL)


def init_product_edit_by_href(drv, href):
    # not(i) to skip 'Edit' link
    product = drv.wd.find_element(By.XPATH, '//a[@href="' + href + '" and not(i)]')
    # Product.text, Link
    logger.info("Open next product: '{}' href: {}".format(product.text, href))
    product.click()
