from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from pages.workflow_page import WorkflowPage
import time

class NoticePage(WorkflowPage):

    NOTICES_MENU = (By.XPATH, "//a[@href='/workflow/notices']")
    NEW_NOTICE = (By.XPATH, "//a[contains(text(), 'New Notice')]")

    # Assuming form fields follow the same pattern as Assignments/Audits
    ENTITY = (By.ID, "EntityId")
    
    # NOTE: Double-check this ID in the HTML if it fails to find the dropdown
    NOTICE_TYPE = (By.ID, "NoticeTypeTypeId") 
    TAX_TYPE = (By.ID, "TaxTypeTypeId")
    
    PERIOD_BEGIN = (By.ID, "txtPeriodBegin")
    PERIOD_END = (By.ID, "txtPeriodEnd")
    COUNTRY = (By.ID, "ddlCountry")
    SUBMIT_NOTICE = (By.ID, "btnSubmit")

    def navigate_to_notices(self):
        self.open_workflow_manager()
        self.click(self.NOTICES_MENU)

    def create_notice(self, data):
        self.click(self.NEW_NOTICE)

        Select(self.driver.find_element(*self.ENTITY)).select_by_value(str(data["EntityId"]))
        
        # Pulls from the "NoticeType" column in your Excel sheet
        Select(self.driver.find_element(*self.NOTICE_TYPE)).select_by_value(str(data["NoticeType"]))
        Select(self.driver.find_element(*self.TAX_TYPE)).select_by_value(str(data["TaxType"]))

        self.type(self.PERIOD_BEGIN, data["PeriodBegin"])
        self.type(self.PERIOD_END, data["PeriodEnd"])

        Select(self.driver.find_element(*self.COUNTRY)).select_by_value(str(data["Country"]))
        time.sleep(4)

        self.click(self.SUBMIT_NOTICE)

        # Wait for the URL to contain 'notice/detail'
        notice_link = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href, '/workflow/notice/detail/')]")
            )
        )

        full_href = notice_link.get_attribute("href")
        return full_href.split("/")[-1]

    def open_notice(self, notice_id):
        self.click((By.XPATH, f"//a[contains(@href, '/workflow/notice/detail/{notice_id}')]"))

    def create_notice_with_task_and_activity(self, data, task_count=1):
        notice_id = self.create_notice(data)
        print(f"Notice Created with ID: {notice_id}")

        self.open_notice(notice_id)

        original_name = data.get("ShortName", "Task")
        for i in range(task_count):
            if task_count > 1:
                data["ShortName"] = f"{original_name} {i+1}"
            else:
                data["ShortName"] = original_name
            self.create_task(data)
            
        self.create_task_activity(data)
        self.create_main_activity(data)

        return notice_id
    