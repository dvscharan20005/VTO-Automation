from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
import time

class CreatePage(BasePage):
     
    ENTITY = (By.ID, "EntityId")
    ASSIGNMENT_TYPE = (By.ID, "AssignmentTypeTypeId")
    AUDIT_TYPE = (By.ID, "AuditTypeTypeId")
    NOTICE_TYPE = (By.ID, "NoticeTypeTypeId")
    TAX_TYPE = (By.ID, "TaxTypeTypeId")
    PERIOD_BEGIN = (By.ID, "txtPeriodBegin")
    PERIOD_END = (By.ID, "txtPeriodEnd")
    COUNTRY = (By.ID, "ddlCountry")
    COUNTRY_CODE = (By.ID, "CurrencyCode")
    SUBMIT_WORK_ITEM = (By.ID, "btnSubmit")

        

    def create_item(self, data):
        self.select_dropdown(self.ENTITY, str(data["EntityId"]))

        if "AssignmentType" in data:
            locator = (By.ID, "AssignmentTypeTypeId")
            value = str(data["AssignmentType"])
        elif "AuditType" in data:
            locator = (By.ID, "AuditTypeTypeId")
            value = str(data["AuditType"])
        elif "NoticeType" in data:
            locator = (By.ID, "NoticeTypeTypeId")
            value = str(data["NoticeType"])
        else:
            raise KeyError("No valid type key (Assignment, Audit, or Notice) found in data.")

        self.select_dropdown(locator, value)
        self.select_dropdown(self.TAX_TYPE, str(data["TaxType"]))
        self.type(self.PERIOD_BEGIN, data["PeriodBegin"])
        self.type(self.PERIOD_END, data["PeriodEnd"])
        self.select_dropdown(self.COUNTRY, str(data["Country"]))
        time.sleep(4)
        self.click(self.SUBMIT_WORK_ITEM)
