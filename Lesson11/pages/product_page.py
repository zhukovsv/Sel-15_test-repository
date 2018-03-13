from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

from pages.page_with_cart_control import Page_With_Cart_Control


class ProductPage(Page_With_Cart_Control):

    def open(self):
        raise NotImplementedError

    @property
    def ProductSizeSelector(self):
        try:
            return self.driver.find_element(By.NAME, 'options[Size]')
        except NoSuchElementException:
            return None

    @property
    def ProductAmountInput(self):
        return self.driver.find_element(By.NAME, 'quantity')

    @property
    def AddButton(self):
        locator = (By.NAME, 'add_cart_product')
        self.wait.until(EC.element_to_be_clickable(locator))
        return self.driver.find_element(*locator)

    def select_size(self, size):
        element = self.ProductSizeSelector
        if element is None or size is None:
            return self
        select = Select(element)
        select.select_by_visible_text(size)
        return self

    def set_amount(self, amount):
        self.ProductAmountInput.clear()
        self.ProductAmountInput.send_keys(amount)
        return self

    def add_to_cart(self, amount, size):
        # user have ability to set amount <= 0, add assert? or check notification
        self.set_amount(amount).select_size(size).submit_add(amount)
        return self

    def submit_add(self, amount):
        before = self.get_products_amount()
        self.AddButton.click()
        self.wait.until(lambda d: int(self.get_products_amount()) == before + amount)
        return self
