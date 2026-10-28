import os
import pytest
from pages.import_vendor_page import ImportVendorPage

def test_vendor_import_flow(driver):
    file_to_upload = r"C:\Users\hp\Downloads\VTO_Vendor_Import_Fixed.xlsx"

    import_page = ImportVendorPage(driver)

    try:
        import_page.navigate_to_excert_manager()
        import_page.navigate_to_procurement()
        import_page.navigate_to_vendors()
        import_page.navigate_to_import_screen()
        import_page.upload_vendor_file(file_to_upload)
        import_page.select_import_options()
        import_page.submit_upload()
        import_page.process_valid_records()
        import_page.complete_and_return()
        
        print("Import Vendor flow completed successfully.")

    except Exception as e:
        screenshot_dir = r"D:\Virtual Tax Office_Automation\Failed_Images\Procurement"
        os.makedirs(screenshot_dir, exist_ok=True) 
        
        screenshot_path = os.path.join(screenshot_dir, "failed_vendor_import.png")
        driver.save_screenshot(screenshot_path)
        print(f"Import failed. Screenshot saved at {screenshot_path}")
        
        raise e