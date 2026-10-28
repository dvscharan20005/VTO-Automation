from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage

class LoginPage(BasePage):

    # -------- Client Code Page --------
    CLIENT_CODE = (By.ID, "ClientCode")
    CLIENT_SUBMIT = (By.ID, "spinner")

    # -------- Username Password Page --------
    USERNAME = (By.ID, "Username")
    PASSWORD = (By.ID, "password")
    SIGNIN_BUTTON = (By.ID, "SignInBtn1")

    def login(self, client_code, username, password):

        # Step 1: Enter Client Code
        self.type(self.CLIENT_CODE, client_code)
        self.click(self.CLIENT_SUBMIT)

        # Wait for Username field to appear
        self.wait.until(
            EC.visibility_of_element_located(self.USERNAME)
        )

        # Step 2: Enter Username & Password
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.SIGNIN_BUTTON)
