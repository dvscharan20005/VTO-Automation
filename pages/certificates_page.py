import os
from random import random
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time  
from pages.sales_page import SalesPage



class CertificatesPage(SalesPage):

    CERTIFICATES_TAB = (By.XPATH, "//a[@href='/ExCert/Certificate']") 
    CREATE_CERTIFICATE_BTN = (By.XPATH, "//a[contains(text(), 'Create Certificate')]")
    NEXT_BTN = (By.XPATH, "//button[contains(text(), 'Next')] | //input[@value='Next']")
    ENTITY_DROPDOWN = (By.XPATH, "//span[@role='combobox' and @aria-labelledby='select2-EntitySelect-container']")            
    ADDRESS_1 = (By.ID, "Address1Id")          
    ADDRESS_2 = (By.ID, "Address2Id")          
    CITY = (By.ID, "CityId")                   
    REGION = (By.ID, "RegionId")               
    POSTAL_CODE = (By.ID, "PostalCodeId")
    
    # --- Step 2: Select Issuer ---
    ISSUER_CUSTOMER_BOX = (By.XPATH, "//span[contains(@aria-labelledby, 'Customer')]")
    BUSINESS_ACTIVITY = (By.ID, "BusinessActivityDescription")
    PROPERTY_PURCHASED = (By.ID, "PropertyPurchased")
    SIGNER_NAME = (By.ID, "SignerName")
    SIGNER_TITLE = (By.ID, "SignerTitle")
    SIGNER_EMAIL = (By.ID, "SignerEmail")
    SIGNER_PHONE = (By.ID, "SignerPhone")
    SIGNER_DATE = (By.ID, "SignatureDate")

    # --- Step 3: Exemption Form Selection ---
    COUNTRY = (By.XPATH, "//span[@role='combobox' and @aria-labelledby='select2-CountryCodeAlpha3Filter-container']")
    TAX_TYPE = (By.ID, "TaxTypeId")
    AVAILABLE_CERTIFICATE_LIST = (By.ID, "CertificateFormSelect")
    
    # --- Step 4: Add Taxpayer Registrations ---
    REGISTRATION = (By.ID, "JurisdictionId_939")
    EXPIRATION = (By.ID, "ExpirationId_939")
    
    # --- Step 5: Add Attachment ---
    FILE_UPLOAD_INPUT = (By.ID, "UploadedFiles")
    FINAL_CREATE_CERT_BTN = (By.ID, "Submit")

    def navigate_to_certificates(self):
        wait = WebDriverWait(self.driver, 15)
        tab = wait.until(EC.element_to_be_clickable(self.CERTIFICATES_TAB))
        tab.click()
        time.sleep(2)

    def click_create_certificate(self):
        wait = WebDriverWait(self.driver, 15)
        btn = wait.until(EC.element_to_be_clickable(self.CREATE_CERTIFICATE_BTN))
        btn.click()
        time.sleep(2)


    def _click_next(self):
        wait = WebDriverWait(self.driver, 10)
        btn = wait.until(EC.element_to_be_clickable(self.NEXT_BTN))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(2)

    def _fill_select2(self, container_locator, text_to_select):
        wait = WebDriverWait(self.driver, 10)
        container = wait.until(EC.element_to_be_clickable(container_locator))
        container.click()
        time.sleep(1)
        search_box_locator = (By.XPATH, "//input[@type='search' or contains(@class, 'select2-search__field')]")
        search_box = wait.until(EC.visibility_of_element_located(search_box_locator))
        search_box.send_keys(text_to_select)
        time.sleep(1)
        search_box.send_keys(Keys.ENTER)
        time.sleep(1)

    def fill_step_1_entity(self, data):
        wait = WebDriverWait(self.driver, 15)
        entity_name = str(data['EntityName']).strip()
        self._fill_select2(self.ENTITY_DROPDOWN, entity_name)
        time.sleep(3)
        self._click_next()

    def fill_step_2_issuer(self, data):
        wait = WebDriverWait(self.driver, 15)      
        self._fill_select2(self.ISSUER_CUSTOMER_BOX, data['CustomerName'])       
        self.driver.find_element(*self.BUSINESS_ACTIVITY).send_keys(str(data['BusinessActivity']))
        self.driver.find_element(*self.PROPERTY_PURCHASED).send_keys(str(data['PropertyPurchased']))
        self.driver.find_element(*self.SIGNER_NAME).send_keys(str(data['SignerName']))
        self.driver.find_element(*self.SIGNER_TITLE).send_keys(str(data['SignerTitle']))
        self.driver.find_element(*self.SIGNER_EMAIL).send_keys(str(data['SignerEmail']))
        self.driver.find_element(*self.SIGNER_PHONE).send_keys(str(data['SignerPhone']))
        self.driver.find_element(*self.SIGNER_DATE).send_keys(str(data['SignatureDate']))
        self._click_next()

    def fill_step_3_form_selection(self, data):
        wait = WebDriverWait(self.driver, 15)
        self._fill_select2(self.COUNTRY, str(data['Country']))
        tax_dropdown = wait.until(EC.element_to_be_clickable(self.TAX_TYPE))
        Select(tax_dropdown).select_by_visible_text(str(data['TaxType']))
        time.sleep(1) 
        cert_list = wait.until(EC.element_to_be_clickable(self.AVAILABLE_CERTIFICATE_LIST))
        Select(cert_list).select_by_visible_text(str(data['CertificateName']))
        self._click_next()

    def fill_step_4_registrations(self, data):
        wait = WebDriverWait(self.driver, 10)
        reg_input = wait.until(EC.visibility_of_element_located(self.REGISTRATION))
        reg_input.send_keys(str(data.get('RegistrationNumber', '')))
        expiration_input = self.driver.find_element(*self.EXPIRATION)
        expiration_input.send_keys(str(data.get('ExpirationDate', '')))
        self._click_next()

    def fill_step_5_attachment_and_submit(self, data):
        wait = WebDriverWait(self.driver, 10)
        excel_file_path = str(data['AttachmentPath']).strip()
        absolute_file_path = os.path.abspath(excel_file_path)
        upload_input = wait.until(EC.presence_of_element_located(self.FILE_UPLOAD_INPUT))
        upload_input.send_keys(absolute_file_path)
        time.sleep(1)
        final_btn = wait.until(EC.element_to_be_clickable(self.FINAL_CREATE_CERT_BTN))
        try:
            final_btn.click()
        except:
            self.driver.execute_script("arguments[0].click();", final_btn)






