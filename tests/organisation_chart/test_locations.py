import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def test_create_location(driver, excel_data):
    data_rows = excel_data.get_sheet_data("Locations")

    for row in data_rows:
        # 2. Navigation
        driver.find_element(By.ID, "navbarModules").click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Organization Chart')]"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/OrgChart/Location']"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Add Location')]"))).click()

        # 3. Fill basic Location details
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "LocationCode"))).send_keys(str(row['LocationCode']))
        driver.find_element(By.ID, "LocationName").send_keys(str(row['LocationName']))
        Select(driver.find_element(By.ID, "LocationTypeId")).select_by_value(str(row['LocationTypeId']))

        # 4. Country Select2 Dropdown
        driver.find_element(By.ID, "select2-CountryCodeAlpha3-container").click()
        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class='select2-search__field']")))
        search_input.send_keys(str(row['Country']))
        search_input.send_keys(Keys.ENTER)
        
        # 5. Address Details
        driver.find_element(By.ID, "Address1").send_keys(str(row['Address1']))
        driver.find_element(By.ID, "City").send_keys(str(row['City']))

        # 6. Region Select2 Dropdown
        driver.find_element(By.ID, "select2-SubdivisionCode-container").click()
        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class='select2-search__field']")))
        search_input.send_keys(str(row['Region']))
        search_input.send_keys(Keys.ENTER)
        
        driver.find_element(By.ID, "PostalCode").send_keys(str(row['PostalCode']))

        # 7. Submit (Using the reliable JS Click we learned from the Entities page)
        submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']"))
        )
        driver.execute_script("arguments[0].click();", submit_btn)

        print(f"Successfully submitted location: {row['LocationName']}")
        time.sleep(3) # Short wait to let the page process before looping to the next row