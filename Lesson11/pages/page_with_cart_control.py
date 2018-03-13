from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import Base_Page


class Page_With_Cart_Control(Base_Page):

    def get_products_amount(self):
        return int(self.driver.find_element(By.CSS_SELECTOR, '#cart .quantity').text)

    def go_to_checkout_page(self):
        self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Checkout').click()
        self.wait.until(EC.title_is('Checkout | My Store'))
