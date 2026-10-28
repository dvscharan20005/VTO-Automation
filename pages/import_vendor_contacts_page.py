import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.excert_base_page import ExcertBasePage

class ImportVendorContactsPage(ExcertBasePage):

    PROCUREMENT_MENU = (By.XPATH, "//a[@href='/ExCert/Procurement']")
    VENDORS_LINK = (By.XPATH, "//a[contains(., 'Vendors') or contains(@href, 'Vendor')]")
    IMPORT_CONTACTS_BTN = (By.XPATH, "//a[@href='/ExCert/Vendor/ImportContacts']")
    FILE_INPUT = (By.XPATH, "//input[@type='file']")
    REVIEW_IMPORT_CHK = (By.ID, "ReviewBeforeImport")
    UPLOAD_CONTACTS_BTN = (By.XPATH, "//button[contains(text(), 'Upload Vendor Contacts')] | //input[@value='Upload Vendor Contacts']")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 15)

    def click_element(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def navigate_to_procurement(self):
        self.click_element(self.PROCUREMENT_MENU)

    def navigate_to_vendors(self):
        self.click_element(self.VENDORS_LINK)

    def click_import_contacts(self):
        self.click_element(self.IMPORT_CONTACTS_BTN)

    def upload_contacts_file(self, file_path):
        file_input = self.wait.until(EC.presence_of_element_located(self.FILE_INPUT))
        file_input.send_keys(file_path)

    def select_review_option(self):
        review_check = self.wait.until(EC.presence_of_element_located(self.REVIEW_IMPORT_CHK))
        if not review_check.is_selected():
            self.driver.execute_script("arguments[0].click();", review_check)

    def submit_upload(self):
        self.click_element(self.UPLOAD_CONTACTS_BTN)