from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DetailPage(BasePage):

    ADD_TASK = (By.XPATH, "//a[contains(text(),'Add Task')]")
    ADD_ACTIVITY = (By.XPATH, "//a[contains(text(),'Add Activity')]")

    def add_task(self):
        self.click(self.ADD_TASK)

    def add_activity(self):
        self.click(self.ADD_ACTIVITY)
