from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
    
        self.driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", element)
    
        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator, value):
        self.wait.until(EC.visibility_of_element_located(locator)).clear()
        self.driver.find_element(*locator).send_keys(value)

    def select_dropdown(self, locator, value):
        element = self.wait.until(EC.presence_of_element_located(locator))
        Select(element).select_by_value(value)


    