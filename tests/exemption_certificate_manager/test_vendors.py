import os
import time
from utils.excel_helper import update_excel_status
from pages.vendor_page import VendorPage

def test_add_vendor_flow(driver, excel_data):
    excel_file = r"D:\Virtual Tax Office_Automation\test_data\Workflow_Manager.xlsx"
    sheet_name = "Vendors" 
    
    data_rows = excel_data.get_sheet_data(sheet_name)
    vendor_page = VendorPage(driver)

    for index, row in enumerate(data_rows, start=2):
        vendor_code = str(row.get("VendorCode", "")).strip()
        
        if not vendor_code or vendor_code.lower() == "none":
            continue

        try:
            vendor_page.navigate_to_excert_manager()
            vendor_page.navigate_to_procurement()
            vendor_page.navigate_to_vendors()

            vendor_page.click_add_vendor()
            time.sleep(2)
            vendor_page.fill_vendor_form(row)
            vendor_page.submit_form()

            update_excel_status(excel_file, sheet_name, index, column_name="Status", status="Passed")
            print(f"Successfully added vendor: {vendor_code}")

        except Exception as e:
            screenshot_dir = r"D:\Virtual Tax Office_Automation\Failed_Images\Procurement"
            os.makedirs(screenshot_dir, exist_ok=True) 
            
            screenshot_path = os.path.join(screenshot_dir, f"failed_vendor_row_{index}.png")
            driver.save_screenshot(screenshot_path)
            
            update_excel_status(excel_file, sheet_name, index, column_name="Status", status="Failed")
            print(f"Failed at row {index}. Screenshot saved at {screenshot_path}")
            
            raise e