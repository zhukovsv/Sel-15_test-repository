
import pytest
# file->Settings->Project interpreter find and add hamcrest
from hamcrest import *
from selenium import webdriver
from selenium.webdriver.common.by import By



login, pwd = 'admin', 'admin'
URL = 'http://localhost/litecart/en/'


class Locators(object):
    CAMPAIGNS = By.ID, 'box-campaigns'
    PRODUCT = By.ID, 'box-product'
    REGULAR_PRICE = By.CSS_SELECTOR, '.regular-price'
    CAMPAIGN_PRICE = By.CSS_SELECTOR, '.campaign-price'


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


# Get dictionary with list of properties
def get_element_style_attributes(element, props=None):
    css_properties = props if props is not None else ['color', 'text-decoration', 'font-weight', 'font-size']
    return dict((prop, element.value_of_css_property(prop)) for prop in css_properties)


# Test Gray and Red colors
# Test font size
def test_product_attributes_colors_and_fontsize(driver):
    driver.get(URL)

    # check color(RGB) and font-size for Campaign product on Home page.
    box = driver.find_element(*Locators.CAMPAIGNS)
    owner = box.find_element(By.CSS_SELECTOR, '.products .product:nth-of-type({index})'.format(index=1))

    # check that color should be gray = rgbs(x,x,x,Y).
    style = get_element_style_attributes(owner.find_element(*Locators.REGULAR_PRICE), ['color'])
    rgb_color = style['color'].replace("rgba(", "").replace(")", "").split(",")
    assert (int(rgb_color[0]) == int(rgb_color[1])) & (int(rgb_color[1]) == int(rgb_color[2])), \
        "Color isn't gray"

    # check that color should be red = rgbs(Z,x,x,Y). and x = 0
    style = get_element_style_attributes(owner.find_element(*Locators.CAMPAIGN_PRICE), ['color'])
    rgb_color = style['color'].replace("rgba(", "").replace(")", "").split(",")
    assert (int(rgb_color[1]) == 0) & (int(rgb_color[1]) == int(rgb_color[2]))\
           & (int(rgb_color[0]) != int(rgb_color[2])), "Color isn't red"

    # check that Campaign Price > Regular price.
    style = get_element_style_attributes(owner.find_element(*Locators.REGULAR_PRICE), ['font-size'])
    regular_price_font_size = float(style['font-size'].replace("px", ""))
    style = get_element_style_attributes(owner.find_element(*Locators.CAMPAIGN_PRICE), ['font-size'])
    campaign_price_font_size = float(style['font-size'].replace("px", ""))
    assert campaign_price_font_size > regular_price_font_size, \
        "Campaign Price not grater than Regular price"

    # Open Product page
    owner.click()

    # check color(RGB) and font-size for Campaign product on Product page.
    owner = driver.find_element(*Locators.PRODUCT)

    # check that color should be gray = rgbs(x,x,x,Y).
    style = get_element_style_attributes(owner.find_element(*Locators.REGULAR_PRICE), ['color'])
    rgb_color = style['color'].replace("rgba(", "").replace(")", "").split(",")
    assert (int(rgb_color[0]) == int(rgb_color[1])) & (int(rgb_color[1]) == int(rgb_color[2])), \
        "Color isn't gray"

    # check that color should be red = rgbs(Z,x,x,Y).
    style = get_element_style_attributes(owner.find_element(*Locators.CAMPAIGN_PRICE), ['color'])
    rgb_color = style['color'].replace("rgba(", "").replace(")", "").split(",")
    assert (int(rgb_color[1]) == 0) & (int(rgb_color[1]) == int(rgb_color[2]))\
           & (int(rgb_color[0]) != int(rgb_color[2])), "Color isn't red"

    # check that Campaign Price > Regular price.
    style = get_element_style_attributes(owner.find_element(*Locators.REGULAR_PRICE), ['font-size'])
    regular_price_font_size = float(style['font-size'].replace("px", ""))
    style = get_element_style_attributes(owner.find_element(*Locators.CAMPAIGN_PRICE), ['font-size'])
    campaign_price_font_size = float(style['font-size'].replace("px", ""))
    assert campaign_price_font_size > regular_price_font_size, \
        "Campaign Price not grater than Regular price"


# Check that product has the same attributes on Home and Product pages
# Name, Manufacturer, Regular Price, Campaign Price
def test_product_attributes(driver):
    driver.get(URL)
    box = driver.find_element(*Locators.CAMPAIGNS)
    owner = box.find_element(By.CSS_SELECTOR, '.products .product:nth-of-type({index})'.format(index=1))
    # Create dictionary for HomePage with Name, Manufactor, RegPrice, CampignPrice
    home_attribute = {'name': owner.find_element(By.CLASS_NAME, 'name').text,
                   'manufacturer': owner.find_element(By.CSS_SELECTOR, '.manufacturer').text,
                   'regular-price': owner.find_element(*Locators.REGULAR_PRICE).text,
                   'campaign-price': owner.find_element(*Locators.CAMPAIGN_PRICE).text}

    owner.click()

    # Create dictionary for ProductPage with Name, Manufactor, RegPrice, CampignPrice
    owner = driver.find_element(*Locators.PRODUCT)
    product_attribute = {'name': owner.find_element(By.CLASS_NAME, 'title').text,
                      # case when attribute title= property title?
                      'manufacturer': owner.find_element(By.CSS_SELECTOR, '.manufacturer img').get_attribute('title'),
                      'regular-price': owner.find_element(*Locators.REGULAR_PRICE).text,
                      'campaign-price': owner.find_element(*Locators.CAMPAIGN_PRICE).text}
    # Check homeDetails = productDetails
    # assert_that.has_entries
    assert_that(product_attribute, has_entries(home_attribute),
                "Check that product has the same attributes on Home and Product pages")


# Check that product has the same attributes on Home and Product pages
# Name, Manufacturer, Regular Price, Campaign Price
def test_product_attributes_by_steps(driver):
    driver.get(URL)
    box = driver.find_element(*Locators.CAMPAIGNS)
    owner = box.find_element(By.CSS_SELECTOR, '.products .product:nth-of-type({index})'.format(index=1))
    name = owner.find_element(By.CLASS_NAME, 'name').text
    manufacturer = owner.find_element(By.CSS_SELECTOR, '.manufacturer').text
    regular_price = owner.find_element(*Locators.REGULAR_PRICE).text
    campaign_price = owner.find_element(*Locators.CAMPAIGN_PRICE).text

    owner.click()

    owner = driver.find_element(*Locators.PRODUCT)
    # assert_that.equal_to
    assert_that(owner.find_element(By.CLASS_NAME, 'title').text, equal_to(name), "Product name")
    title = owner.find_element(By.CSS_SELECTOR, '.manufacturer img').get_attribute('title')
    assert_that(title, equal_to(manufacturer), "Manufacturer name")
    assert_that(owner.find_element(*Locators.REGULAR_PRICE).text, equal_to(regular_price), "Regular price")
    assert_that(owner.find_element(*Locators.CAMPAIGN_PRICE).text, equal_to(campaign_price), "Campaign price")


# Check Style:
# color, text-decoration, font-weight, font-size
def test_campaign_styles(driver):
    expected = {'regular-price-home': {'color': 'rgba(119, 119, 119, 1)',
                                       'text-decoration': 'line-through solid rgb(119, 119, 119)',
                                       'font-weight': '400',
                                       'font-size': '14.4px'},
                'campaign-price-home': {'color': 'rgba(204, 0, 0, 1)',
                                        'text-decoration': 'none solid rgb(204, 0, 0)',
                                        'font-weight': '700',
                                        'font-size': '18px'},
                'regular-price-product': {'color': 'rgba(102, 102, 102, 1)',
                                          'text-decoration': 'line-through solid rgb(102, 102, 102)',
                                          'font-weight': '400',
                                          'font-size': '16px'},
                'campaign-price-product': {'color': 'rgba(204, 0, 0, 1)',
                                           'text-decoration': 'none solid rgb(204, 0, 0)',
                                           'font-weight': '700',
                                           'font-size': '22px'}}

    driver.get(URL)
    box = driver.find_element(*Locators.CAMPAIGNS)
    owner = box.find_element(By.CSS_SELECTOR, '.products .product:nth-of-type({index})'.format(index=1))
    displayed = {'regular-price-home': get_element_style_attributes(owner.find_element(*Locators.REGULAR_PRICE)),
                 'campaign-price-home': get_element_style_attributes(owner.find_element(*Locators.CAMPAIGN_PRICE))}
    owner.click()

    owner = driver.find_element(*Locators.PRODUCT)
    displayed['regular-price-product'] = get_element_style_attributes(owner.find_element(*Locators.REGULAR_PRICE))
    displayed['campaign-price-product'] = get_element_style_attributes(owner.find_element(*Locators.CAMPAIGN_PRICE))
    # Print for testing usage
    """
    for itemD in displayed:
        print(itemD)
        sub_displ = displayed[itemD]
        for subitemD in sub_displ:
            print(subitemD, ':', sub_displ[subitemD])
    """

    assert_that(displayed, has_entries(expected), 'Check styles')


def test_campaign_styles_by_steps(driver):
    expected = {'regular-price-home': {'color': 'rgba(119, 119, 119, 1)',
                                       'text-decoration': 'line-through solid rgb(119, 119, 119)',
                                       'font-weight': '400',
                                       'font-size': '14.4px'},
                'campaign-price-home': {'color': 'rgba(204, 0, 0, 1)',
                                        'text-decoration': 'none solid rgb(204, 0, 0)',
                                        'font-weight': '700',
                                        'font-size': '18px'},
                'regular-price-product': {'color': 'rgba(102, 102, 102, 1)',
                                          'text-decoration': 'line-through solid rgb(102, 102, 102)',
                                          'font-weight': '400',
                                          'font-size': '16px'},
                'campaign-price-product': {'color': 'rgba(204, 0, 0, 1)',
                                           'text-decoration': 'none solid rgb(204, 0, 0)',
                                           'font-weight': '700',
                                           'font-size': '22px'}}

    driver.get(URL)
    box = driver.find_element(*Locators.CAMPAIGNS)
    owner = box.find_element(By.CSS_SELECTOR, '.products .product:nth-of-type({index})'.format(index=1))

    style = get_element_style_attributes(owner.find_element(*Locators.REGULAR_PRICE))
    assert_that(style, equal_to(expected['regular-price-home']), 'regular-price-home style')

    style = get_element_style_attributes(owner.find_element(*Locators.CAMPAIGN_PRICE))
    assert_that(style, equal_to(expected['campaign-price-home']), 'campaign-price-home style')

    owner.click()

    owner = driver.find_element(*Locators.PRODUCT)

    style = get_element_style_attributes(owner.find_element(*Locators.REGULAR_PRICE))
    assert_that(style, equal_to(expected['regular-price-product']), 'regular-price-product style')

    style = get_element_style_attributes(owner.find_element(*Locators.CAMPAIGN_PRICE))
    assert_that(style, equal_to(expected['campaign-price-product']), 'campaign-price-product style')
