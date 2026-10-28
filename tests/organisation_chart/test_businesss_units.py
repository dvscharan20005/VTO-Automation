import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_create_business_unit(driver, excel_data):
    data_rows = excel_data.get_sheet_data("Business_Units")

    for row in data_rows:
        # 2. Navigation
        driver.find_element(By.ID, "navbarModules").click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Organization Chart')]"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/OrgChart/BusinessUnit']"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Add Business Unit')]"))).click()

        # 3. Fill Business Unit details
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "BusinessUnitCode"))).send_keys(str(row['BusinessUnitCode']))
        driver.find_element(By.ID, "BusinessUnitName").send_keys(str(row['BusinessUnitName']))

        submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']"))
        )
        driver.execute_script("arguments[0].click();", submit_btn)

        print(f"Successfully submitted Business Unit: {row['BusinessUnitName']}")
        time.sleep(3) 