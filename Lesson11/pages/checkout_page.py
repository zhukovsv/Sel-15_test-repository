from selenium.common.exceptions import NoSuchElementException

from pages.base_page import Base_Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage(Base_Page):

    url = "http://localhost/litecart/en/checkout"
    # url = "http://192.168.1.3/litecart/en/checkout"

    def open(self):
        if not self.is_on_page():
            return super(CheckoutPage, self).open(CheckoutPage.url)

    def is_on_page(self):
        return self.driver.current_url == CheckoutPage.url

    @property
    def Table(self):
        try:
            return self.driver.find_element(By.CSS_SELECTOR, '.dataTable')
        except NoSuchElementException:
            return None

    @property
    def Items(self):
        # Return list of added products in the TOP part of the page
        return self.driver.find_elements(By.CSS_SELECTOR, 'li.item')

    @property
    def ProductsInOrderTable(self):
        # self.Table is None means that No products were added
        if self.Table is None:
            return []
        # Return list of added products in Table from bottom part of the page
        return [x.text for x in self.Table.find_elements(By.CSS_SELECTOR, 'td.item')]

    def remove_first_product_from_cart(self):
        REMOVE_ITEM = By.CSS_SELECTOR, '.item [name="remove_cart_item"]'
        self.wait.until(EC.element_to_be_clickable(REMOVE_ITEM))
        table = self.Table
        remove = self.driver.find_element(*REMOVE_ITEM)
        remove.click()
        self.wait.until(EC.staleness_of(remove))
        self.wait.until(EC.staleness_of(table))
        return self

    def remove_all_products(self):
        while self.Items:
            # Remove first product
            self.remove_first_product_from_cart()
        self.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'em'), 'There are no items in your cart.'))