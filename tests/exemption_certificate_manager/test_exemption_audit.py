import os
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from utils.excel_helper import update_excel_status
from pages.customer_page import CustomerPage

def test_exemption_audit_flow(driver, excel_data):
    excel_file = r"D:\Virtual Tax Office_Automation\test_data\Workflow_Manager.xlsx"
    sheet_name = "Exemption_Audit" 
    
    data_rows = excel_data.get_sheet_data(sheet_name)
    wait = WebDriverWait(driver, 15)
    

    customer_page = CustomerPage(driver)

    for index, row in enumerate(data_rows, start=2):
        file_path_value = str(row.get("FilePath", "")).strip()
        
        if not file_path_value or file_path_value.lower() == "none":
            continue

        try:
            customer_page.navigate_to_excert_manager()
            customer_page.navigate_to_sales()

            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/ExCert/Exemption']"))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Exemption Audit')]"))).click()

            file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            file_input.send_keys(file_path_value)
            
            tax_dropdown = Select(wait.until(EC.presence_of_element_located((By.XPATH, "//select[ancestor::div[contains(., 'Tax Type')] or @id='TaxType']"))))
            tax_dropdown.select_by_visible_text(str(row['TaxType']))
            
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Upload Exempt Customers')] | //a[contains(text(), 'Upload Exempt Customers')] | //input[@value='Upload Exempt Customers']"))).click()
            
            send_requests_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Send Requests')] | //button[contains(text(), 'Send Requests')]")))
            send_requests_btn.click()
            time.sleep(2)
            
            req_template = Select(wait.until(EC.presence_of_element_located((By.ID, 'Common_Email_Request_Temp'))))
            req_template.select_by_visible_text(str(row['Email Request Template']).strip())

            ren_template = Select(driver.find_element(By.ID, 'Common_Email_Renewal_Temp'))
            ren_template.select_by_visible_text(str(row['Email Renewal Template']).strip())

            rem_template = Select(driver.find_element(By.ID, 'Common_Email_Reminder_Temp'))
            rem_template.select_by_visible_text(str(row['Email Reminder Template']).strip())
            time.sleep(2)

            language = Select(driver.find_element(By.ID, 'StockTemplateLanguageSelect'))
            language.select_by_value(str(row['Language']).strip())

            select_all_checkbox = wait.until(EC.element_to_be_clickable((By.ID, 'example-select-all')))
            if not select_all_checkbox.is_selected():
                select_all_checkbox.click()
                
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Send Selected')] | //input[@value='Send Selected']"))).click()
            
            ok_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]")))
            ok_button.click()
            
            update_excel_status(excel_file, sheet_name, index, column_name="Status", status="Passed")
            print(f"Successfully processed Exemption Audit for row {index}")

        except Exception as e:
            screenshot_dir = r"D:\Virtual Tax Office_Automation\Failed_Images\Exemption Certificate Manager"
            os.makedirs(screenshot_dir, exist_ok=True) 
            
            screenshot_name = f"failed_audit_flow_row_{index}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_name)
            
            driver.save_screenshot(screenshot_path)
            
            update_excel_status(excel_file, sheet_name, index, column_name="Status", status="Failed")
            print(f"Failed at row {index}. Screenshot saved at {screenshot_path}")
            
            raise e