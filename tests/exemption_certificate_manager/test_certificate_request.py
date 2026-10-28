import os
import openpyxl
from conftest import excel_data
from pages.certificate_request_page import RequestPage

def update_excel_status(file_path, row_num, status):
    """Opens the Excel file, writes the pass/fail status, and saves it."""
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook["Requests"]
    sheet.cell(row=row_num, column=9).value = status

    workbook.save(file_path)

def test_create_excert_request(driver, excel_data):
    excel_file = "D:\\Virtual Tax Office_Automation\\test_data\\Workflow_Manager.xlsx"

    data_rows = excel_data.get_sheet_data("Requests")
    req_page = RequestPage(driver)

    for index, row in enumerate(data_rows, start=2):
        # Ignore empty Excel rows
        if str(row.get('Customer', '')).strip() in ['None', '', 'nan']:
            break

        try:
            req_page.navigate_to_excert_manager()
            req_page.navigate_to_sales()
            req_page.navigate_to_requests()

            req_page.start_wizard()

            req_page.fill_step_1_contact(row)
            req_page.fill_step_2_template(row)
            req_page.fill_step_3_jurisdiction(row)
            req_page.submit_final_wizard()

            assert "Requests" in driver.title, f"Wizard submission failed for {row['Customer']}"

            update_excel_status(excel_file, index, "Passed")
            print(f"Successfully created request for: {row['Customer']}")

        except Exception as e:
            screenshot_dir = r"D:\Virtual Tax Office_Automation\Failed_Images"
            screenshot_name = f"failed_request_row_{index}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_name)
            driver.save_screenshot(screenshot_path)
            update_excel_status(excel_file, index, "Failed")
            print(f"Failed at row {index}. Screenshot saved at {screenshot_path}")
            
            raise e