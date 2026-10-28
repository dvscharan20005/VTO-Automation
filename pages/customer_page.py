from selenium.webdriver.common.by import By
from pages.sales_page import SalesPage
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pages.sales_page import SalesPage
import time


class CustomerPage(SalesPage):

    ADD_CUSTOMER_BTN = (By.XPATH, "//a[@href='/ExCert/Customer/Create']")
    SUBMIT_BTN = (By.XPATH, "//input[@type='submit' and @value='Add Customer']")

    ENTITY = (By.ID, "select2-EntityId-container")
    CUSTOMER_NUMBER = (By.ID, "CustomerNumber")
    CUSTOMER_NAME = (By.ID, "CustomerName")
    
    COUNTRY = (By.ID, "ddlCountry")
    ADDRESS = (By.ID, "AddressLine1")
    CITY = (By.ID, "City")
    REGION = (By.ID, "select2-SubdivisionCode-container")
    POSTAL_CODE = (By.ID, "PostalCode")
    
    PRIMARY_CONTACT_NAME = (By.ID, "ContactName")

    SELECT2_SEARCH_INPUT = (By.XPATH, "//input[@class='select2-search__field']")

    def click_add_customer(self):
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.ADD_CUSTOMER_BTN)).click()
        time.sleep(2)

    def fill_customer_form(self, data):
        """Fills out the Add Customer form using data from the Excel row"""
        wait = WebDriverWait(self.driver, 15)

        # 1. Legal Entity 
        wait.until(EC.element_to_be_clickable(self.ENTITY)).click()
        search_box = wait.until(EC.visibility_of_element_located(self.SELECT2_SEARCH_INPUT))
        search_box.send_keys(str(data['LegalEntity']))
        search_box.send_keys(Keys.ENTER)

        # 2. Customer Details
        wait.until(EC.presence_of_element_located(self.CUSTOMER_NUMBER)).send_keys(str(data['CustomerNumber']))
        self.driver.find_element(*self.CUSTOMER_NAME).send_keys(str(data['CustomerName']))

        # 3. Country (Standard Dropdown)
        Select(self.driver.find_element(*self.COUNTRY)).select_by_value(str(data["Country"]))

        # 4. Address & City
        self.driver.find_element(*self.ADDRESS).send_keys(str(data['Address']))
        self.driver.find_element(*self.CITY).send_keys(str(data['City']))

        # 5. Region
        wait.until(EC.element_to_be_clickable(self.REGION)).click()
        search_box_region = wait.until(EC.visibility_of_element_located(self.SELECT2_SEARCH_INPUT))
        search_box_region.send_keys(str(data['Region']))
        search_box_region.send_keys(Keys.ENTER)

        # 6. Postal Code & Contact
        self.driver.find_element(*self.POSTAL_CODE).send_keys(str(data['PostalCode']))
        self.driver.find_element(*self.PRIMARY_CONTACT_NAME).send_keys(str(data['PrimaryContactName']))

    def submit_form(self):
        submit_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.SUBMIT_BTN))
        self.driver.execute_script("arguments[0].click();", submit_btn)
        time.sleep(3)








