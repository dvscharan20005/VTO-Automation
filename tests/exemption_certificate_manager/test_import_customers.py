import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_import_customers(driver):
    
    # 1. Navigation to Customers
    driver.find_element(By.ID, "navbarModules").click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Exemption Certificate Manager')]"))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/ExCert/Sales']"))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/ExCert/Customer']"))).click()

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/ExCert/Customer/Import']"))).click()

    file_input = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "UploadedFiles")))

    file_input.send_keys(r"C:\Users\hp\Downloads\VTO Customer Import Template.xlsx")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "UpdateExisting"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ReviewBeforeImport"))).click()

    UPLOAD_CUSTOMERS_BTN = (By.XPATH, "//input[@type='submit' and @value='Upload Customers']")
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(UPLOAD_CUSTOMERS_BTN)).click()

    import_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Import Valid Records')]")))
    driver.execute_script("arguments[0].click();", import_btn)
    
    time.sleep(5)

    # 6. Return to Customers Grid
    return_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Return to Customers')] | //button[contains(text(), 'Return to Customers')]"))
    )
    driver.execute_script("arguments[0].click();", return_btn)

    print("Successfully imported the customers file!")
    time.sleep(3)