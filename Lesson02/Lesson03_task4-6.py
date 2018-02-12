import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = 'http://localhost/litecart/admin'
login, pwd = 'admin', 'admin'


class Locators(object):
    LOGIN = 'username'
    PWD = 'password'
    LOGIN_BUTTON = 'login'
    REMEMBER = 'remember_me'
    LOGOUT_BUTTON = 'i.fa.fa-sign-out.fa-lg'


@pytest.fixture
def driver(request):
    # Web Browser = Chrome
    # wd = webdriver.Chrome()
    wd = webdriver.Chrome(desired_capabilities={'chromeOptions': {'args': ["--start-fullscreen"]}})

    # Web Browser = IE
    # wd = webdriver.Ie()
    # wd = webdriver.Ie()#capabilities={'proxy': {'proxyType': 'manual', 'httpProxy': 'http://10.6.0.1:3128',
    #           'sslProxy': 'http://10.6.0.1:3128', 'socksProxy': 'http://10.6.0.1:3128'},
    # 'ie.usePerProcessProxy': True})
    # wd = webdriver.Ie(capabilities={"requireWindowFocus": True})

    # Web Browser = MicroSoft Edge
    #wd = webdriver.Edge()

    # Web Browser = Mozilla Firefox
    # New schema
    # wd = webdriver.Firefox()
    # New strong schema
    #wd = webdriver.Firefox(capabilities={"marionette": True})

    # OLD schema
    #wd = webdriver.Firefox(capabilities={"marionette": False})

    # OLD schema + binary path
    # wd = webdriver.Firefox(firefox_binary=r'c:\Program Files\Firefox Nightly\firefox.exe');
    #wd = webdriver.Firefox(capabilities={"marionette": False},
     #                     firefox_binary=r'c:\Program Files\Mozilla Firefox ESR2\firefox.exe')


    # wd.implicitly_wait(10)
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def configure(drv, login_value=None, pwd_value=None, remember=None):
    WebDriverWait(drv, 10).until(EC.title_is("My Store"))
    if login_value is not None:
        drv.find_element_by_name(Locators.LOGIN).send_keys(login_value)
    if pwd_value is not None:
        drv.find_element_by_name(Locators.PWD).send_keys(pwd_value)
    if remember:
        drv.find_element_by_name(Locators.REMEMBER).click()
    drv.find_element_by_name(Locators.LOGIN_BUTTON).click()
    WebDriverWait(drv, 10).until(EC.title_is("My Store"))



def test_login_logout(driver):
    # login
    driver.get(url)
    configure(driver, login_value=login, pwd_value=pwd)
    # logout
    driver.find_element_by_css_selector(Locators.LOGOUT_BUTTON).click()
    WebDriverWait(driver, 10).until(EC.title_is("My Store"))


def test_remember_me(driver):
    # Open login form
    driver.get(url)
    configure(driver, login_value=login, pwd_value=pwd, remember=True)
    driver.find_element_by_css_selector(Locators.LOGOUT_BUTTON).click()
    WebDriverWait(driver, 10).until(EC.title_is("My Store"))


def test_logo_click(driver):
    # Open login form
    driver.get(url)
    # Click Logo to open Online Store
    driver.find_element_by_tag_name('a').click()
    WebDriverWait(driver, 10).until(EC.title_is("Online Store | My Store"))
