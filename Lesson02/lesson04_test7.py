"""
    # wait = WebDriverWait(driver, 10) - укоротить запись кода в дальнейшем, дабы не писать следующее
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located(Locators.SELECTED_MENU_ITEM)
    # find_element  = driver.find_element
    # find_elements = driver.find_elements
    # find_element, find_elements = driver.find_element, driver.find_elements

    # В find_element передается всегда tuple со звездочкой
    # find_element(*Locators.MENU_ITEM)
    # find_elements(*Locators.MENU_ITEM)[i]

    # Для Exception Condition class методов передается  tuple без звездочки
    # EC.presence_of_element_located(Locators.SELECTED_MENU_ITEM)
    # EC.text_to_be_present_in_element(Locators.SELECTED_MENU_ITEM, parent)

    # В цикле пройти по элементам, которые были добавлены в enumerate,
    # в виде элементов for x in find_elements(*Locators.MENU_ITEM)
    # у которых затем взяли текст x.text
    # for i, parent in enumerate([x.text for x in find_elements(*Locators.MENU_ITEM)]):
    #   find_elements(*Locators.MENU_ITEM)[i]
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'http://localhost/litecart/admin/'
login, pwd = 'admin', 'admin'


class Locators(object):
    LOGIN = By.NAME, 'username'
    PWD = By.NAME, 'password'
    REMEMBER = By.NAME, 'remember_me'
    LOGIN_BUTTON = By.NAME, 'login'
    LOGOUT_BUTTON = By.CSS_SELECTOR, 'i.fa.fa-sign-out.fa-lg'
    HEADER = By.TAG_NAME, 'h1'
    PARENT_MENU_ITEM = By.CSS_SELECTOR, 'li#app-'
    SELECTED_PARENT_MENU_ITEM = By.CSS_SELECTOR, 'li#app-.selected'
    CHILD_MENU_ITEM = By.CSS_SELECTOR, 'li#app-.selected li'
    SELECTED_CHILD_MENU_ITEM = By.CSS_SELECTOR, 'li#app-.selected li.selected'


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def login_admin(drv, login_value=None, pwd_value=None, remember=None):
    if login_value is not None:
        drv.find_element(*Locators.LOGIN).send_keys(login_value)
    if pwd_value is not None:
        drv.find_element(*Locators.PWD).send_keys(pwd_value)
    if remember:
        drv.find_element(*Locators.REMEMBER).click()
    drv.find_element(*Locators.LOGIN_BUTTON).click()
    WebDriverWait(drv, 10).until(EC.title_is("My Store"))


def logout_admin(drv):
    # logout
    drv.find_element(*Locators.LOGOUT_BUTTON).click()
    WebDriverWait(drv, 10).until(EC.title_is("My Store"))


def test_menu_activation(driver):
    # wait = WebDriverWait(driver, 10)
    wait = WebDriverWait(driver, 10)

    driver.get(url)
    wait.until(EC.title_is("My Store"))

    # Login to admin page
    login_admin(driver, login_value=login, pwd_value=pwd)
    # find_element  = driver.find_element
    # find_elements = driver.find_elements
    find_element, find_elements = driver.find_element, driver.find_elements

    print('')
    for i, parent in enumerate([x.text for x in find_elements(*Locators.PARENT_MENU_ITEM)]):
        find_elements(*Locators.PARENT_MENU_ITEM)[i].click()
        print('"{parent}":'.format(**locals()))
        # Check that parent menu.Exists() and have text value = parent
        wait.until(EC.presence_of_element_located(Locators.SELECTED_PARENT_MENU_ITEM) and
                   EC.text_to_be_present_in_element(Locators.SELECTED_PARENT_MENU_ITEM, parent))
        # Check that Parent Menu is active/selected
        active = find_element(*Locators.SELECTED_PARENT_MENU_ITEM)
        assert active.text.startswith(parent), 'Parent Menu item should be selected!'

        for j, child in enumerate([x.text for x in find_elements(*Locators.CHILD_MENU_ITEM)]):
            find_elements(*Locators.CHILD_MENU_ITEM)[j].click()
            print('---------"{child}"'.format(**locals()))
            # Check that child menu.Exists() and have text value = child
            wait.until(EC.presence_of_element_located(Locators.SELECTED_CHILD_MENU_ITEM) and
                       EC.text_to_be_present_in_element(Locators.SELECTED_CHILD_MENU_ITEM, child))
            # Check that Child Menu is active/selected
            active_child = find_element(*Locators.SELECTED_CHILD_MENU_ITEM)
            assert active_child.text == child, 'Sub-menu item should be selected!'
            # Check Header for Child
            assert find_elements(*Locators.HEADER) != [], 'Header should exists!'
    else:
        # Check Header Parent
        assert find_elements(*Locators.HEADER) != [], 'Header should exists!'

    # Logout from admin page
    logout_admin(driver)
