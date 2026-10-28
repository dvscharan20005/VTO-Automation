import os
import pytest
from pages.notice_page import NoticePage
from pages.workflow_page import WorkflowPage
from pages.create_page import CreatePage
from utils.email_helper import verify_email_received
from utils.excel_helper import update_excel_status

def test_create_notice(driver, excel_data):
    workflow = WorkflowPage(driver)
    create = CreatePage(driver)

    workflow.open_workflow_manager()
    workflow.open_module("Notices")
    
    notice_page = NoticePage(driver)
    notice_page.click(notice_page.NEW_NOTICE)

    data = excel_data.get_sheet_data("Notices")

    for row in data:
        create.create_item(row)

def test_create_notice_with_tasks_and_activities(driver, excel_data):
    excel_file = r"D:\Virtual Tax Office_Automation\test_data\Workflow_Manager.xlsx"
    sheet_name = "Notices"
    
    workflow = WorkflowPage(driver)
    notice_page = NoticePage(driver)
    
    workflow.open_workflow_manager()
    workflow.open_module("Notices")
    data_rows = excel_data.get_sheet_data(sheet_name)

    for index, data in enumerate(data_rows, start=2):
        if not data.get("EntityId") or str(data.get("EntityId")).strip() == "":
            continue
            
        try:
            raw_task_count = data.get("TaskCount")
            try:
                target_count = int(raw_task_count) if raw_task_count else 1
            except (ValueError, TypeError):
                target_count = 1

            notice_id = notice_page.create_notice_with_task_and_activity(data, task_count=target_count)

            recipient_email = data.get("Email_OtherRecipient")
            expected_subject = data.get("ExpectedSubject")
            
            email_arrived = verify_email_received(
                username=recipient_email, 
                app_password="pncluibkrpnoybcr",
                subject_to_find=expected_subject, 
                max_wait_time=60 
            )
            
            assert email_arrived is True, f"ERROR: The email to {recipient_email} was never received in the inbox!"
            assert notice_id is not None, "Notice ID was not generated."

            update_excel_status(excel_file, sheet_name, index, column_name="Status", status="Passed")
            print(f"Successfully processed Notice ID {notice_id} for {recipient_email}")

        except Exception as e:
            screenshot_dir = r"D:\Virtual Tax Office_Automation\Failed_Images\workflow manager\Notices"
            screenshot_name = f"failed_notice_row_{index}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_name)
            
            driver.save_screenshot(screenshot_path)
            update_excel_status(excel_file, sheet_name, index, column_name="Status", status="Failed")
            print(f"Failed at row {index}. Screenshot saved at {screenshot_path}")
            
            raise e