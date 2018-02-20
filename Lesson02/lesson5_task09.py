import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


login, pwd = 'admin', 'admin'
countries_url = 'http://localhost/litecart/admin/?app=countries&doc=countries'
zones_url = 'http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones'


class Locators(object):
    LOGIN = By.NAME, 'username'
    PWD = By.NAME, 'password'
    LOGIN_BUTTON = By.NAME, 'login'
    LOGOUT_BUTTON = By.CSS_SELECTOR, 'i.fa.fa-sign-out.fa-lg'

    TABLE = By.CLASS_NAME, 'dataTable'
    TABLE_ZONES = By.ID, 'table-zones'

    CANCEL = By.CSS_SELECTOR, '.button-set button[name="cancel"]'



@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def login_admin(drv, url):
    drv.get(url)
    drv.find_element(*Locators.LOGIN).send_keys(login)
    drv.find_element(*Locators.PWD).send_keys(pwd)
    drv.find_element(*Locators.LOGIN_BUTTON).click()


def logout_admin(drv):
    drv.find_element(*Locators.LOGOUT_BUTTON).click()
    WebDriverWait(drv, 10).until(EC.title_is("My Store"))


def find_column_index(table, column_name):
    locator = './/th[contains(.,"{column_name}")]'
    list_values = table.find_elements(By.XPATH, locator.format(column_name=column_name))
    return (int((list_values[0]).get_attribute('cellIndex')))+1


def get_column_values(table, column, child=None):
    index = find_column_index(table, column)
    locator = 'td:nth-of-type({index})'.format(index=index) + ((' ' + child) if child else '')
    # print(locator)
    # print('Column Values for Column Name = ', column)
    list_values = []
    for el in table.find_elements(By.CSS_SELECTOR, locator):
        try:
            input = el.find_element(By.CSS_SELECTOR, 'input')
            # if unput and type<>hidden then do not add empty input in list_values
            if input.get_attribute("type") == 'hidden':
                list_values.append(el.text)
                # print(el.text)
                continue
        except:
            list_values.append(el.text)
            # print(el.text)
    return list_values


def verify_zone_sorting(drv, zone_column_name, child=None):
    table_zones = drv.find_element(*Locators.TABLE_ZONES)
    zones = get_column_values(table_zones, zone_column_name, child)
    assert zones == sorted(zones), "SubZones have to be displayed sorted"


# Test Countries sorting
# Use countries_url = 'http://localhost/litecart/admin/?app=countries&doc=countries'
def test_countries_sorting(driver):
    login_admin(driver, countries_url)
    table = driver.find_element(*Locators.TABLE)
    countries = get_column_values(table, 'Name')
    assert countries == sorted(countries)


# Test sorting of zones for countries were amount of zones>0
# Use countries_url = 'http://localhost/litecart/admin/?app=countries&doc=countries'
def test_not_empty_zones_sorting(driver):
    # login
    login_admin(driver, countries_url)
    # shorter code
    find_element, find_elements = driver.find_element, driver.find_elements
    table = find_element(*Locators.TABLE)
    # add to non_empty_zones index(=1 from for) from enumerate where value!=0 (countries with amount of zone>0)
    non_empty_zones = [i for i, v in enumerate(get_column_values(table, 'Zones')) if int(v) != 0]
    country_name_index = str(find_column_index(table, 'Name'))
    # rows with countries started from 2 that's why +2
    for rowId in (str(x+2) for x in non_empty_zones):
        # find country.row[i] with amount of zone>0
        row = find_element(By.CSS_SELECTOR, 'tr.row:nth-of-type(' + rowId + ')')
        # find link(in Name column) to zones in country.row[i] with amount of zone>0 and click on it.
        row.find_element(By.CSS_SELECTOR, 'td:nth-of-type(' + country_name_index + ') a').click()
        try:
            verify_zone_sorting(driver, 'Name')
        finally:
            # Return to Countries page
            find_element(*Locators.CANCEL).click()


# Test sorting of zones for
# Use zones_url = 'http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones'
def test_geo_zones_sorting(driver):
    # login
    login_admin(driver, zones_url)
    # shorter code
    find_element, find_elements = driver.find_element, driver.find_elements
    table = find_element(*Locators.TABLE)
    # find Name column's index in table Geo Zones
    country_name_index = str(find_column_index(table, 'Name'))
    # find amount of rows in table Geo Zones
    rows_count = len(table.find_elements(By.CSS_SELECTOR, 'tr.row'))
    # row index started from 2
    for rowId in (str(x) for x in range(2, rows_count + 2)):
        # find country.row[i]
        row = find_element(By.CSS_SELECTOR, 'tr.row:nth-of-type(' + rowId + ')')
        # find link(in Name column) and click on it.
        row.find_element(By.CSS_SELECTOR, 'td:nth-of-type(' + country_name_index + ') a').click()
        try:
            verify_zone_sorting(driver, "Zone", 'select[name$="][zone_code]"] option[selected=selected]')
        finally:
            # Return to Geo Zones page
            find_element(*Locators.CANCEL).click()
