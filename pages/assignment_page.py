from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from pages.workflow_page import WorkflowPage
import time


class AssignmentPage(WorkflowPage):

    ASSIGNMENTS_MENU = (By.XPATH, "//a[@href='/workflow/assignments']")
    NEW_ASSIGNMENT = (By.XPATH, "//a[contains(text(), 'New Assignment')]")
    ENTITY = (By.ID, "EntityId")
    ASSIGNMENT_TYPE = (By.ID, "AssignmentTypeTypeId")
    TAX_TYPE = (By.ID, "TaxTypeTypeId")
    PERIOD_BEGIN = (By.ID, "txtPeriodBegin")
    PERIOD_END = (By.ID, "txtPeriodEnd")
    COUNTRY = (By.ID, "ddlCountry")
    COUNTRY_CODE = (By.ID, "CurrencyCode")
    SUBMIT_ASSIGNMENT = (By.ID, "btnSubmit")


    def navigate_to_assignments(self):
        self.open_workflow_manager()
        self.click(self.ASSIGNMENTS_MENU)

    def create_assignment(self, data):
        self.click(self.NEW_ASSIGNMENT)
        Select(self.driver.find_element(*self.ENTITY)).select_by_value(str(data["EntityId"]))
        Select(self.driver.find_element(*self.ASSIGNMENT_TYPE)).select_by_value(str(data["AssignmentType"]))
        Select(self.driver.find_element(*self.TAX_TYPE)).select_by_value(str(data["TaxType"]))
        self.type(self.PERIOD_BEGIN, data["PeriodBegin"])
        self.type(self.PERIOD_END, data["PeriodEnd"])
        Select(self.driver.find_element(*self.COUNTRY)).select_by_value(str(data["Country"]))
        time.sleep(4)
        self.click(self.SUBMIT_ASSIGNMENT)

        assignment_link = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href, '/workflow/assignment/detail/')]")
            )
        )

        full_href = assignment_link.get_attribute("href")
        return full_href.split("/")[-1]

    def open_assignment(self, assignment_id):
        self.click((By.XPATH, f"//a[contains(@href, '/workflow/assignment/detail/{assignment_id}')]"))

    def create_assignment_with_task_and_activity(self, data, task_count=1):
        
        assignment_id = self.create_assignment(data)
        print(f"Assignment Created with ID: {assignment_id}")

        self.open_assignment(assignment_id)
        original_name = data.get("ShortName", "Task")
        for i in range(task_count):
            if task_count > 1:
                data["ShortName"] = f"{original_name} {i+1}"
            else:
                data["ShortName"] = original_name
            self.create_task(data)

        self.create_task_activity(data)
        self.create_main_activity(data)

        return assignment_id
