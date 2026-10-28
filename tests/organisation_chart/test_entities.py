import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def test_create_entity(driver, excel_data):
    
    data_rows = excel_data.get_sheet_data("External_Entity_Data")
    
    for row in data_rows:
        # 2. Navigation
        driver.find_element(By.ID, "navbarModules").click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Organization Chart')]"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/OrgChart/Entity']"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Add Entity')]"))).click()
        
        # 3. Basic Entity details
        driver.find_element(By.ID, "EntityCode").send_keys(str(row['EntityCode']))
        driver.find_element(By.ID, "EntityName").send_keys(str(row['EntityName']))
        
        # Determine if External (handling string 'True' or actual boolean from Excel)
        is_external = str(row['IsExternal']).strip().lower() in ['true', '1', 'yes']
        
        external_checkbox = driver.find_element(By.ID, "IsExternal")
        if is_external and not external_checkbox.is_selected():
            external_checkbox.click()
        elif not is_external and external_checkbox.is_selected():
            external_checkbox.click() 

        driver.find_element(By.ID, "TaxIdNumber").send_keys(str(row['TaxIdNumber']))

        # 4. Handle External vs Internal Logic
        if is_external:
            driver.find_element(By.XPATH, "//input[@type='submit']").click()
            time.sleep(2)
            Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "OwningEntity")))).select_by_value(str(row['OwningEntity']))
            driver.find_element(By.XPATH, "//input[@value='Finish']").click()
        else:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "BusinessActivityDescription"))).send_keys(str(row['BusinessActivityDescription']))
            driver.find_element(By.XPATH, "//input[@type='submit']").click()
            time.sleep(2)
            
            # Select2 Dropdowns
            driver.find_element(By.ID, "select2-CountryCodeAlpha3-container").click()
            search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class='select2-search__field']")))
            search_input.send_keys(str(row['CountryCode']))
            search_input.send_keys(Keys.ENTER)

            driver.find_element(By.ID, "select2-SubdivisionCode-container").click()
            search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@class='select2-search__field']")))
            search_input.send_keys(str(row['RegionOfFormation']))
            search_input.send_keys(Keys.ENTER)

            driver.find_element(By.ID, "FormationDate").send_keys(datetime.date.today().strftime("%d/%m/%Y"))
            driver.find_element(By.ID, "FormationAuthority").send_keys(str(row['FormationAuthority']))
            Select(driver.find_element(By.ID, "EntityTypeId")).select_by_value(str(row['EntityTypeId']))
            driver.find_element(By.ID, "EntityIdentifier").send_keys(str(row['EntityIdentifier']))
            driver.find_element(By.XPATH, "//input[@type='submit']").click()

        # 5. Location Details (Common to both)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "LocationCode"))).send_keys(str(row['LocationCode']))
        driver.find_element(By.ID, "LocationName").send_keys(str(row['LocationName']))
        Select(driver.find_element(By.ID, "LocationTypeId")).select_by_value(str(row['LocationTypeId']))
        Select(driver.find_element(By.ID, "LocationCountryCodeAlpha3")).select_by_value(str(row['Country']))
        driver.find_element(By.ID, "LocationAddress1").send_keys(str(row['Address1']))
        driver.find_element(By.ID, "LocationCity").send_keys(str(row['City']))
        Select(driver.find_element(By.ID, "LocationSubdivisionCode")).select_by_value(str(row['Region']))
        driver.find_element(By.ID, "LocationPostalCode").send_keys(str(row['PostalCode']))
        next_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='Next' and @type='submit']"))
        )
        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Finish']"))).click()