import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pages.sales_page import SalesPage

class RequestPage(SalesPage):

    # --- Locators ---
    REQUESTS_TAB = (By.XPATH, "//a[contains(text(), 'Requests')] | //a[contains(@href, '/ExCert/Request')]")
    CREATE_REQUEST = (By.XPATH, "//a[@href='/ExCert/Request/Wizard']")
    SUBMIT_BTN = (By.ID, "Submit")
    SELECT2_SEARCH_INPUT = (By.XPATH, "//input[@class='select2-search__field']")

    # Page 1 Locators
    CUSTOMER = (By.XPATH, "//span[@aria-labelledby='select2-CustomerSelect-container']")
    DROP_DOWN= (By.ID, "select2-CustomerSelect-results")
    CONTACT_TYPE = (By.ID, "ContactType")
    FULL_NAME = (By.ID, "FullName")
    EMAIL = (By.ID, "EmailAddress")
    TAX_TYPE = (By.ID, "CertificateTaxTypeId")

    # Page 2 Locators
    TEMPLATE_SELECT = (By.ID, "CustomTemplateSelect")

    # Page 3 Locators
    COUNTRY = (By.ID, "select2-CountryCodeAlpha3-container")
    REGION = (By.ID, "select2-SubdivisionCode-container")
    ADD_JURISDICTION_BTN = (By.ID, "JurisdictionAdd")

    # Page 4 Locators
    FINAL_CREATE_BTN = (By.XPATH, "//input[@id='Submit' and @value='Create Exemption Certificate Request']")

   # --- Helper Method for Select2 Search Boxes ---
    def _fill_select2(self, container_locator, text_value):
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.element_to_be_clickable(container_locator)).click()
        search_box = wait.until(EC.visibility_of_element_located(self.SELECT2_SEARCH_INPUT))
        search_box.send_keys(str(text_value))
        time.sleep(2)
        search_box.send_keys(Keys.ENTER)

    def navigate_to_requests(self):
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.REQUESTS_TAB)).click()
        time.sleep(2)

    def start_wizard(self):
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.CREATE_REQUEST)).click()
        time.sleep(2)

    def fill_step_1_contact(self, data):
        wait = WebDriverWait(self.driver, 15)
        customer_name = str(data['Customer']).strip()
        self._fill_select2(self.CUSTOMER, customer_name)
           
        Select(wait.until(EC.element_to_be_clickable(self.CONTACT_TYPE))).select_by_value(str(data['ContactType']))
        time.sleep(2)
        self.driver.find_element(*self.FULL_NAME).send_keys(str(data['FullName']))
        self.driver.find_element(*self.EMAIL).send_keys(str(data['EmailAddress']))
        Select(self.driver.find_element(*self.TAX_TYPE)).select_by_value(str(data['CertificateTaxTypeId']))
        
        self.driver.find_element(*self.SUBMIT_BTN).click()
        time.sleep(1)

    def fill_step_2_template(self, data):
        wait = WebDriverWait(self.driver, 15)
        template_dropdown = wait.until(EC.presence_of_element_located(self.TEMPLATE_SELECT))
        Select(template_dropdown).select_by_visible_text(str(data['CustomTemplateSelect']))
        time.sleep(2)
        self.driver.find_element(*self.SUBMIT_BTN).click()
        time.sleep(2)

    def fill_step_3_jurisdiction(self, data):
        self._fill_select2(self.COUNTRY, data['Country'])
        self._fill_select2(self.REGION, data['Region'])
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ADD_JURISDICTION_BTN)).click()
        time.sleep(1)
        self.driver.find_element(*self.SUBMIT_BTN).click()
        time.sleep(1)

    def submit_final_wizard(self):
        btn = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.FINAL_CREATE_BTN))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(3)