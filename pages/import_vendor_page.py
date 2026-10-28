import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.excert_base_page import ExcertBasePage

class ImportVendorPage(ExcertBasePage):
    PROCUREMENT_MENU = (By.XPATH, "//a[@href='/ExCert/Procurement']")
    VENDORS_LINK = (By.XPATH, "//a[contains(., 'Vendors') or contains(@href, 'Vendor')]")
    IMPORT_VENDORS_BTN = (By.XPATH, "//a[@href='/ExCert/Vendor/Import']")

    FILE_INPUT = (By.ID, "UploadedFiles")
    UPDATE_EXISTING_CHK = (By.ID, "UpdateExisting")
    REVIEW_IMPORT_CHK = (By.XPATH, "//label[contains(text(), 'Review Before Import')]/../input[@type='checkbox'] | //input[contains(@id, 'Review')]")
    UPLOAD_VENDORS_BTN = (By.XPATH, "//button[contains(text(), 'Upload Vendors')] | //input[@value='Upload Vendors']")

    IMPORT_VALID_RECORDS_BTN = (By.XPATH, "//a[contains(text(), 'Import Valid Records')] | //a[contains(@href, 'Process')]")
    RETURN_TO_VENDORS_BTN = (By.XPATH, "//a[contains(text(), 'Return to Vendors')] | //a[@href='/ExCert/Vendor']")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 15)

    def click_element(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def navigate_to_procurement(self):
            self.click_element(self.PROCUREMENT_MENU)
    
    def navigate_to_vendors(self):
            self.click_element(self.VENDORS_LINK)

    def navigate_to_import_screen(self):
        self.wait.until(EC.element_to_be_clickable(self.IMPORT_VENDORS_BTN)).click()

    def upload_vendor_file(self, file_path):
        file_input = self.wait.until(EC.presence_of_element_located(self.FILE_INPUT))
        file_input.send_keys(file_path)

    def select_import_options(self):
        update_check = self.wait.until(EC.presence_of_element_located(self.UPDATE_EXISTING_CHK))
        if not update_check.is_selected():
            self.driver.execute_script("arguments[0].click();", update_check)
        review_check = self.wait.until(EC.presence_of_element_located(self.REVIEW_IMPORT_CHK))
        if not review_check.is_selected():
            self.driver.execute_script("arguments[0].click();", review_check)

    def submit_upload(self):
        self.wait.until(EC.element_to_be_clickable(self.UPLOAD_VENDORS_BTN)).click()

    def process_valid_records(self):
        self.wait.until(EC.element_to_be_clickable(self.IMPORT_VALID_RECORDS_BTN)).click()

    def complete_and_return(self):
        self.wait.until(EC.element_to_be_clickable(self.RETURN_TO_VENDORS_BTN)).click()