from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from pages.workflow_page import WorkflowPage
import time

class AuditPage(WorkflowPage):

    AUDITS_MENU = (By.XPATH, "//a[@href='/workflow/audits']")
    NEW_AUDIT = (By.XPATH, "//a[contains(text(), 'New Audit')]")
    ENTITY = (By.ID, "EntityId")
    AUDIT_TYPE = (By.ID, "AuditTypeTypeId") 
    TAX_TYPE = (By.ID, "TaxTypeTypeId")
    PERIOD_BEGIN = (By.ID, "txtPeriodBegin")
    PERIOD_END = (By.ID, "txtPeriodEnd")
    COUNTRY = (By.ID, "ddlCountry")
    SUBMIT_AUDIT = (By.ID, "btnSubmit")

    def navigate_to_audits(self):
        self.open_workflow_manager()
        self.click(self.AUDITS_MENU)

    def create_audit(self, data):
        self.click(self.NEW_AUDIT)

        Select(self.driver.find_element(*self.ENTITY)).select_by_value(str(data["EntityId"]))
        Select(self.driver.find_element(*self.AUDIT_TYPE)).select_by_value(str(data["AuditType"]))
        Select(self.driver.find_element(*self.TAX_TYPE)).select_by_value(str(data["TaxType"]))
        self.type(self.PERIOD_BEGIN, data["PeriodBegin"])
        self.type(self.PERIOD_END, data["PeriodEnd"])

        Select(self.driver.find_element(*self.COUNTRY)).select_by_value(str(data["Country"]))
        time.sleep(4)

        self.click(self.SUBMIT_AUDIT)

        audit_link = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href, '/workflow/audit/detail/')]")
            )
        )

        full_href = audit_link.get_attribute("href")
        return full_href.split("/")[-1]

    def open_audit(self, audit_id):
        self.click((By.XPATH, f"//a[contains(@href, '/workflow/audit/detail/{audit_id}')]"))

    def create_audit_with_task_and_activity(self, data, task_count=1):
        audit_id = self.create_audit(data)
        print(f"Audit Created with ID: {audit_id}")

        self.open_audit(audit_id)
        
        original_name = data.get("ShortName", "Task")
        for i in range(task_count):
            if task_count > 1:
                data["ShortName"] = f"{original_name} {i+1}"
            else:
                data["ShortName"] = original_name
            self.create_task(data)
            
        self.create_task_activity(data)
        self.create_main_activity(data)

        return audit_id