import pytest
import exrex
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker


url = 'http://localhost/litecart/en/'


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd

# Create user
def create_user(drv):
    # Find and click to "New customers click here" link
    drv.find_element(By.LINK_TEXT, 'New customers click here').click()
    # Create Faker object and set Location = USA
    fake = Faker('en_US')

    first_name, last_name = fake.name().split()
    # Set fieds
    drv.find_element(By.NAME, 'firstname').send_keys(first_name)
    drv.find_element(By.NAME, 'lastname').send_keys(last_name)
    drv.find_element(By.NAME, 'address1').send_keys(fake.street_address())
    drv.find_element(By.NAME, 'address2').send_keys(fake.street_address())
    drv.find_element(By.NAME, 'postcode').send_keys(fake.postalcode())
    drv.find_element(By.NAME, 'city').send_keys(fake.city())

    country = 'United States'
    # find 'United States' and select it in the list of countries
    for el in drv.find_element(By.NAME, 'country_code').find_elements(By.TAG_NAME, 'option'):
        if country in el.text:
            print(el.text)
            el.click()
            break

    state = fake.state()
    # Should wait before zone selector became click able. Alabama will be always selected without that.
    zone_code_selector = WebDriverWait(drv, 10).\
        until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'select[name=zone_code]')))

    # find fake state and select it in the list of countries
    for el in zone_code_selector.find_elements(By.TAG_NAME, 'option'):
        if state in el.text:
            print(el.text)
            el.click()
            break

    email = fake.safe_email()
    drv.find_element(By.NAME, 'email').send_keys(email)

    # create phone by "+1" + pattern/reg exp
    phone_element = drv.find_element(By.NAME, 'phone')
    phone_element.send_keys(Keys.HOME + '+1 ' + exrex.getone('^(\d{3})-(\d{3})-(\d{4})$'))

    # create/confirm password
    pwd = fake.credit_card_number(card_type=None)
    drv.find_element(By.NAME, 'password').send_keys(pwd)
    drv.find_element(By.NAME, 'confirmed_password').send_keys(pwd)

    # Create user by button click
    drv.find_element(By.NAME, 'create_account').click()

    # return email, pwd for next login
    return email, pwd


# login
def login(drv, email, password):
    drv.find_element(By.NAME, 'email').send_keys(email)
    drv.find_element(By.NAME, 'password').send_keys(password)
    drv.find_element(By.NAME, 'login').click()


# logout
def logout(drv):
    drv.find_element(By.LINK_TEXT, 'Logout').click()


# Test user creation
def test_login_logout(driver):
    # login
    driver.get(url)
    email, pwd = create_user(driver)
    # logout after user creation
    logout(driver)
    # login/logout again
    login(driver, email, pwd)
    logout(driver)
    # login/logout one more time
    login(driver, email, pwd)
    logout(driver)
