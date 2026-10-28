import time
from pages.certificates_page import CertificatesPage

def test_create_certificates_from_excel(driver, excel_data):
    data_rows = excel_data.get_sheet_data("CertificatesData")
    cert_page = CertificatesPage(driver)
    for row in data_rows:
        print(f"\n--- Starting automation for: {row['CustomerName']} ---")
        
        cert_page.navigate_to_excert_manager()
        cert_page.navigate_to_sales()
        cert_page.navigate_to_certificates()
        cert_page.click_create_certificate()
        cert_page.fill_step_1_entity(row)
        cert_page.fill_step_2_issuer(row)
        cert_page.fill_step_3_form_selection(row)
        cert_page.fill_step_4_registrations(row)
        
        cert_page.fill_step_5_attachment_and_submit(row)
        
        print(f"--- Finished automation for: {row['CustomerName']} ---")
        time.sleep(2)