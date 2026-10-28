import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pages.excert_base_page import ExcertBasePage

class VendorPage(ExcertBasePage):

    PROCUREMENT_MENU = (By.XPATH, "//a[@href='/ExCert/Procurement']")
    VENDORS_LINK = (By.XPATH, "//a[contains(., 'Vendors') or contains(@href, 'Vendor')]")

    ADD_VENDOR_BTN = (By.XPATH, "//a[contains(text(), 'Add Vendor')] | //button[contains(text(), 'Add Vendor')]")
    LEGAL_ENTITY = (By.ID, "EntityId") 
    VENDOR_CODE = (By.ID, "VendorCode")
    VENDOR_NAME = (By.ID, "VendorName")
    IS_BUSINESS = (By.ID, "IsBusiness") 
    COUNTRY = (By.ID, "ddlCountry")
    ADDRESS = (By.ID, "AddressLine1")
    CITY = (By.ID, "City")
    REGION = (By.ID, "SubdivisionCode")
    POSTAL_CODE = (By.ID, "PostalCode")

    MODULE_CONTACT_NAME = (By.ID, "ModuleContactName")
    MODULE_CONTACT_EMAIL = (By.ID, "ModuleEmailAddress")
    MODULE_CONTACT_PHONE = (By.ID, "ModuleTelephoneNumber")

    PRIMARY_CONTACT_NAME = (By.ID, "ContactName")
    PRIMARY_CONTACT_EMAIL = (By.ID, "EmailAddress")
    PRIMARY_CONTACT_PHONE = (By.ID, "TelephoneNumber")

    SUBMIT_BTN = (By.XPATH, "//button[text()='Add Vendor'] | //input[@value='Add Vendor']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def click_element(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def enter_text(self, locator, text):
        if text and str(text).lower() != "none":
            element = self.wait.until(EC.presence_of_element_located(locator))
            element.send_keys(str(text).strip())

    def select_by_value(self, locator, value):
        if value and str(value).lower() != "none":
            element = self.wait.until(EC.presence_of_element_located(locator))
            Select(element).select_by_value(str(value).strip())

    def select_by_text(self, locator, text):
        if text and str(text).lower() != "none":
            element = self.wait.until(EC.presence_of_element_located(locator))
            Select(element).select_by_visible_text(str(text).strip())

    def navigate_to_procurement(self):
        self.click_element(self.PROCUREMENT_MENU)

    def navigate_to_vendors(self):
        self.click_element(self.VENDORS_LINK)

    def click_add_vendor(self):
        self.click_element(self.ADD_VENDOR_BTN)

    def fill_vendor_form(self, row):
        self.select_by_text(self.LEGAL_ENTITY, row.get("LegalEntity"))
        self.enter_text(self.VENDOR_CODE, row.get("VendorCode"))
        self.enter_text(self.VENDOR_NAME, row.get("VendorName"))
        
        is_business = str(row.get("IsBusiness", "")).strip().lower()
        if is_business in ['true', 'yes', '1']:
            checkbox = self.driver.find_element(*self.IS_BUSINESS)
            if not checkbox.is_selected():
                checkbox.click()

        self.select_by_value(self.COUNTRY, row.get("Country"))
        self.enter_text(self.ADDRESS, row.get("AddressLine1"))
        self.enter_text(self.CITY, row.get("City"))
        self.select_by_text(self.REGION, row.get("Region"))
        self.enter_text(self.POSTAL_CODE, row.get("PostalCode"))

        self.enter_text(self.MODULE_CONTACT_NAME, row.get("ModuleContactName"))
        self.enter_text(self.MODULE_CONTACT_EMAIL, row.get("ModuleContactEmail"))
        self.enter_text(self.MODULE_CONTACT_PHONE, row.get("ModuleContactPhone"))
    
        self.enter_text(self.PRIMARY_CONTACT_NAME, row.get("PrimaryContactName"))
        self.enter_text(self.PRIMARY_CONTACT_EMAIL, row.get("PrimaryContactEmail"))
        self.enter_text(self.PRIMARY_CONTACT_PHONE, row.get("PrimaryContactPhone"))

    def submit_form(self):
        btn = self.wait.until(EC.presence_of_element_located(self.SUBMIT_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        time.sleep(1)
        btn.click()
        time.sleep(3)