from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class ExcertBasePage(BasePage):
    
    SUBSCRIPTIONS_MENU = (By.ID, "navbarModules")
    EXCERT_MANAGER_LINK = (By.XPATH, "//a[contains(text(), 'Exemption Certificate Manager')]")

    # Main ExCert Tabs
    SALES_TAB = (By.XPATH, "//a[@href='/ExCert/Sales']")
    PROCUREMENT_TAB = (By.XPATH, "//a[@href='/ExCert/Procurement']")
    OPTIONS_TAB = (By.XPATH, "//a[contains(text(), 'Options')]")

    def navigate_to_excert_manager(self):
        self.click(self.SUBSCRIPTIONS_MENU)
        self.click(self.EXCERT_MANAGER_LINK)
        time.sleep(1)