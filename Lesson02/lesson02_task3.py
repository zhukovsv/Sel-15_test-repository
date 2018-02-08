import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_login(driver):
    # Open login form
    driver.get("http://localhost/litecart/admin")
    WebDriverWait(driver, 10).until(EC.title_is("My Store"))
    # Set UserName
    driver.find_element_by_name("username").send_keys("admin")
    # Set UserPassword
    driver.find_element_by_name("password").send_keys("admin")
    # Check Remember Me
    driver.find_element_by_name("remember_me").click()
    # UnCheck Remember Me
    driver.find_element_by_name("remember_me").click()
    # Click "Login" button
    driver.find_element_by_name("login").click()
    WebDriverWait(driver, 10).until(EC.title_is("My Store"))
    # Click "Logout" button
    driver.find_element_by_css_selector("i.fa.fa-sign-out.fa-lg").click()
    WebDriverWait(driver, 10).until(EC.title_is("My Store"))


def test_logo_click(driver):
    # Open login form
    driver.get("http://localhost/litecart/admin")
    WebDriverWait(driver, 10).until(EC.title_is("My Store"))
    # Click Logo to open Online Store
    driver.find_element_by_tag_name('a').click()
    WebDriverWait(driver, 10).until(EC.title_is("Online Store | My Store"))
