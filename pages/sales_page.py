from selenium.webdriver.common.by import By
from pages.excert_base_page import ExcertBasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class SalesPage(ExcertBasePage):

    # Sales Sub-Tabs
    CUSTOMERS_TAB = (By.XPATH, "//a[@href='/ExCert/Customer']")

    def navigate_to_sales(self):
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.SALES_TAB)).click()
        time.sleep(1)

    def navigate_to_customers(self):
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.CUSTOMERS_TAB)).click()
        time.sleep(1)