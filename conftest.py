import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage
from utils.excel_reader import ExcelReader


# -------- Excel Fixture --------
@pytest.fixture
def excel_data():
    reader = ExcelReader("test_data/Workflow_Manager.xlsx")
    return reader


# -------- Driver Fixture --------
@pytest.fixture
def driver(excel_data):

    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get("https://my.r3vto.com/Client")

    login_page = LoginPage(driver)

    login_data = excel_data.get_sheet_data("Assignments")[0]

    login_page.login(
        login_data["ClientCode"],
        login_data["Username"],
        login_data["Password"]
    )

    yield driver
    driver.quit()
