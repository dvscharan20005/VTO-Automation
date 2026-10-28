import os
import pytest
from pages.assignment_page import AssignmentPage
from pages.workflow_page import WorkflowPage
from pages.create_page import CreatePage
from utils.email_helper import verify_email_received
from utils.excel_helper import update_excel_status


def test_create_assignment(driver, excel_data):

    workflow = WorkflowPage(driver)
    create = CreatePage(driver)
    workflow.open_workflow_manager()
    workflow.open_module("Assignments")
    data = excel_data.get_sheet_data("Assignments")
    for row in data:
        workflow.click_new()
        create.create_item(row)

def test_create_assignment_with_tasks_and_activities(driver, excel_data):
    excel_file = r"D:\Virtual Tax Office_Automation\test_data\Workflow_Manager.xlsx"
    sheet_name = "Assignments"
    
    workflow = WorkflowPage(driver)
    assignment_page = AssignmentPage(driver)
    
    workflow.open_workflow_manager()
    workflow.open_module("Assignments")
    
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

            assignment_id = assignment_page.create_assignment_with_task_and_activity(data, task_count=target_count)
            recipient_email = data.get("Email_OtherRecipient")
            expected_subject = data.get("ExpectedSubject")
            
            email_arrived = verify_email_received(
                username=recipient_email,
                app_password="pncluibkrpnoybcr",
                subject_to_find=expected_subject, 
                max_wait_time=60 
            )
            
            assert email_arrived is True, f"ERROR: The email to {recipient_email} was never received in the inbox!"
            assert assignment_id is not None, "Assignment ID was not generated."

            update_excel_status(excel_file, sheet_name, index, column_name="Status", status="Passed")
            print(f"Successfully processed Assignment ID {assignment_id} for {recipient_email}")

        except Exception as e:
            screenshot_dir = r"D:\Virtual Tax Office_Automation\Failed_Images\workflow manager\Assignments"
            screenshot_name = f"failed_assignment_row_{index}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_name)
            
            driver.save_screenshot(screenshot_path)

            update_excel_status(excel_file, sheet_name, index, column_name="Status", status="Failed")
            print(f"Failed at row {index}. Screenshot saved at {screenshot_path}")
            
            raise e




 