from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys


class WorkflowPage(BasePage):

    NAVBAR_MODULES = (By.ID, "navbarModules")
    WORKFLOW_MANAGER = (By.XPATH, "//a[contains(text(), 'Workflow Manager')]")
    ENTITY = (By.ID, "EntityId")
    ADD_TASK = (By.XPATH, "//a[contains(text(), 'Add Task')]")
    TASK_TYPE = (By.ID, "TaskTypeTypeId")
    DUE_DATE = (By.ID, "DueDate")
    SHORT_NAME = (By.ID, "ShortName")
    PRIORITY = (By.ID, "PriorityLevel")
    SUBMIT_TASK = (By.XPATH, "//button[contains(text(), 'Submit Task')]")

    VIEW_TASK = (By.XPATH, "//a[contains(text(), 'View')]")
    ADD_ACTIVITY = (By.XPATH, "//a[contains(text(), 'Add Activity')]")
    ADD_MAIN_ACTIVITY = (By.CSS_SELECTOR, "a.btn-activity-action")
    ACTIVITY_TYPE = (By.ID, "activityTypeDropdown")
    EMAIL = (By.ID, "Email_OtherRecipient")
    MEMO = (By.ID, "MemoText")

    SUBMIT_ACTIVITY = (By.ID, "btnCreateActivity")
    ADD = (By.ID, "addAttachmentBtn")
    RETURN_TO_ITEM = (By.XPATH, "//a[contains(text(), 'Return to Assignment') or contains(text(), 'Return to Audit') or contains(text(), 'Return to Notice')]")
    RETURN_TO_HOME = (By.XPATH, "//a[contains(text(), 'Return to Assignments') or contains(text(), 'Return to Audits') or contains(text(), 'Return to Notices')]")
    FILE_UPLOAD = (By.ID, "fileUpload0")
    EXPORT_WITH_TASKS = (By.XPATH, "//button[contains(text(), 'Export with Tasks')]")
    ADVANCED_SEARCH = (By.XPATH, "//a[contains(text(), 'Advanced Search')]")
    VIEW_TASKS = (By.XPATH, "//a[contains(text(), 'View Tasks')]")

    # --------------------------------------

    def open_workflow_manager(self): 
        self.click(self.NAVBAR_MODULES)
        self.click(self.WORKFLOW_MANAGER)

    def open_module(self, module_name):
        MODULE_LOCATOR = (By.LINK_TEXT, module_name)
        self.click(MODULE_LOCATOR)

    def click_new(self):
        NEW_ASSIGNMENT_BTN = (By.XPATH, "//a[contains(text(), 'New Assignment')]")
        self.click(NEW_ASSIGNMENT_BTN)

    def create_task(self, data):
        self.click(self.ADD_TASK)
        self.wait.until(EC.visibility_of_element_located(self.TASK_TYPE))
        Select(self.driver.find_element(*self.TASK_TYPE)).select_by_value(str(data["TaskType"]))
        self.type(self.DUE_DATE, data["DueDate"])
        self.type(self.SHORT_NAME, data["ShortName"])
        Select(self.driver.find_element(*self.PRIORITY)).select_by_value(str(data["PriorityLevel"]))
        self.click(self.SUBMIT_TASK)
        time.sleep(3)

    def create_task_activity(self, data):
        self.click(self.VIEW_TASK)
        self.click(self.ADD_ACTIVITY)
        self.click(self.ACTIVITY_TYPE)
        time.sleep(2)
        Select(self.driver.find_element(*self.ACTIVITY_TYPE)).select_by_value(str(data["ActivityTypeTypeId"]))
        time.sleep(2)
        self.type(self.EMAIL, data["Email_OtherRecipient"])
        self.type(self.MEMO, data["MemoText"])
        
        file_path = str(data['File_Path']) 
        description_input = self.wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Description']"))) 
        description_input.send_keys(str(data['Description']))
        time.sleep(2)
        upload_input = self.wait.until(EC.presence_of_element_located((By.ID, "fileUpload0")))

        upload_input.send_keys(file_path)

        add_btn = self.wait.until(EC.element_to_be_clickable(self.ADD))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", add_btn)
        add_btn.click()
        time.sleep(3)
        self.click(self.SUBMIT_ACTIVITY)
        time.sleep(3)
        self.wait.until(EC.presence_of_element_located(self.RETURN_TO_ITEM))
        self.click(self.RETURN_TO_ITEM)
   

    def create_main_activity(self, data):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.click(self.ADD_MAIN_ACTIVITY)
        time.sleep(2)
        self.wait.until(EC.visibility_of_element_located(self.ACTIVITY_TYPE))

        dropdown = self.driver.find_element(*self.ACTIVITY_TYPE)
        Select(dropdown).select_by_value(str(data["ActivityType"]))
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", dropdown)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL))
        time.sleep(2)
        self.type(self.EMAIL, data["Email_OtherRecipient"])
        self.type(self.MEMO, data["MemoText"])

        file_path = str(data['File_Path'])
        description_input = self.wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Description']"))) 
        description_input.send_keys(str(data['Description']))
        time.sleep(2)
        upload_input = self.wait.until(EC.presence_of_element_located((By.ID, "fileUpload0")))

        upload_input.send_keys(file_path)
        self.click(self.SUBMIT_ACTIVITY)
        time.sleep(3)
        self.click(self.RETURN_TO_HOME)
        




    # def click_export_main(self, module_name):
    #     """
    #     Dynamically clicks 'Export Assignments', 'Export Audits', or 'Export Notices'
    #     """
    #     # We use a dynamic XPath to plug in the module name
    #     dynamic_xpath = f"//a[contains(text(), 'Export {module_name}')] | //button[contains(text(), 'Export {module_name}')]"
    #     self.click((By.XPATH, dynamic_xpath))
    #     print(f"Clicked Export {module_name}")
    #     time.sleep(2) # Short wait to let the browser trigger the file download

    # def click_export_with_tasks(self):
    #     self.click(self.EXPORT_WITH_TASKS)
    #     print("Clicked Export with Tasks")
    #     time.sleep(2) # Short wait to let the browser trigger the file download

    # def click_advanced_search(self):
    #     self.click(self.ADVANCED_SEARCH)
    #     print("Clicked Advanced Search")
    #     time.sleep(1) # Wait for the modal/panel to open

    # def click_view_tasks(self):
    #     self.click(self.VIEW_TASKS)
    #     print("Clicked View Tasks")
    #     # You can add a wait here for the URL to change if it navigates to a new page