import os
import time
from pages.import_vendor_contacts_page import ImportVendorContactsPage

def test_vendor_contacts_import_flow(driver):
    file_to_upload = r"C:\Users\hp\Downloads\VTO Vendor Contact Import Template.xlsx"

    import_contacts_page = ImportVendorContactsPage(driver)

    try:
        import_contacts_page.navigate_to_excert_manager() 
        import_contacts_page.navigate_to_procurement()
        import_contacts_page.navigate_to_vendors()
        import_contacts_page.click_import_contacts()
        
        import_contacts_page.upload_contacts_file(file_to_upload)
        import_contacts_page.select_review_option()
        import_contacts_page.submit_upload()
        time.sleep(5)
        
        print("Import Vendor Contacts flow completed successfully.")

    except Exception as e:
        screenshot_dir = r"D:\Virtual Tax Office_Automation\Failed_Images\Procurement"
        os.makedirs(screenshot_dir, exist_ok=True) 
        
        screenshot_path = os.path.join(screenshot_dir, "failed_vendor_contacts_import.png")
        driver.save_screenshot(screenshot_path)
        print(f"Import failed. Screenshot saved at {screenshot_path}")
        
        raise e