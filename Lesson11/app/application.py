from selenium import webdriver
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.checkout_page import CheckoutPage


class Application:

    def __init__(self):
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.Remote("http://192.168.1.3:4444/wd/hub",
        #                                desired_capabilities={'browserName': 'chrome'})
        self.home_page = HomePage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.checkout_page = CheckoutPage(self.driver)

    def quit(self):
        self.driver.quit()

    def add_product_to_cart(self, product):
        self.home_page.open()
        self.home_page.go_to_product_page(product.category, product.name)
        self.product_page.add_to_cart(product.amount, product.size)

    def get_current_cart_size(self):
        self.home_page.open()
        return self.home_page.get_products_amount()

    def clear_cart(self):
        self.checkout_page.open()
        self.checkout_page.remove_all_products()

    def get_products_in_cart(self):
        self.checkout_page.open()
        # return list of products in checkout_page.table
        return self.checkout_page.ProductsInOrderTable
