from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

df = pd.read_excel("client_signup (1).xlsx")

service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://dev.my.r3vto.com/account/clientsignup")
driver.maximize_window()
driver.find_element(By.ID, "details-button").click()
driver.find_element(By.ID, "proceed-link").click()
#-------------------------------------------------------
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='chkSubscribe']"))).click()
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "btnClientSignUpTerms"))).click()
time.sleep(2)
#-------------------------------------------------------
driver.find_element(By.ID, "CompanyName").send_keys(df.loc[0, 'CompanyName'])
driver.find_element(By.ID, "CompanyCode").send_keys(df.loc[0, 'CompanyCode'])
Select(driver.find_element(By.ID, "CountryCodeAlpha3")).select_by_value(str(df.loc[0, 'Country']))
driver.find_element(By.ID, "Address1").send_keys(df.loc[0, 'Address1'])
driver.find_element(By.ID, "City").send_keys(df.loc[0, 'City'])
Select(driver.find_element(By.ID, "SubdivisionCode")).select_by_value(str(df.loc[0, 'Region']))
driver.find_element(By.ID, "PostalCode").send_keys(df.loc[0, 'PostalCode'])  
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "chkCopyCompanyDetails"))).click()
#-------------------------------------------------------
driver.find_element(By.ID, "UserName").send_keys(df.loc[0, 'UserName'])
driver.find_element(By.ID, "FirstName").send_keys(df.loc[0, 'FirstName'])
driver.find_element(By.ID, "LastName").send_keys(df.loc[0, 'LastName'])
driver.find_element(By.ID, "PreferredName").send_keys(df.loc[0, 'PreferredName'])
driver.find_element(By.ID, "EmailAddress").send_keys(df.loc[0, 'EmailAddress'])
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "TelephoneNumber"))).send_keys(str(df.loc[0, 'TelephoneNumber']))
Select(driver.find_element(By.ID, "TimeZone")).select_by_value(str(df.loc[0, 'TimeZone']))
Select(driver.find_element(By.ID, "TimeFormat")).select_by_value(str(df.loc[0, 'TimeFormat']))
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnNext"))).click()


wait = WebDriverWait(driver, 20)

card_name_field = wait.until(
    EC.presence_of_element_located((By.ID, "CardName"))
)
card_name_field.send_keys("Test User")


# ------------------ Switch to Payment iframe ------------------
wait.until(
    EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe"))
)

# ------------------ Fill Card Details ------------------
wait.until(
    EC.presence_of_element_located((By.NAME, "cardnumber"))
).send_keys("4242424242424242")

wait.until(
    EC.presence_of_element_located((By.NAME, "exp-date"))
).send_keys("04/29")

wait.until(
    EC.presence_of_element_located((By.NAME, "cvc"))
).send_keys("424")

wait.until(
    EC.presence_of_element_located((By.NAME, "postal"))
).send_keys("42424")

# Switch back to main page
driver.switch_to.default_content()


signup_button = wait.until(
    EC.element_to_be_clickable((By.ID, "btnSignUp"))
)

driver.execute_script(
    "arguments[0].scrollIntoView({block: 'center'});",
    signup_button
)

signup_button.click()

# ------------------ Verify Success Page ------------------
try:
    success_header = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h1.display-4"))
    )

    if "Welcome to Virtual Tax Office" in success_header.text:
        print("✅ Registration successful!")
    else:
        print("⚠️ Success page loaded but text mismatch.")

except TimeoutException:
    print("⚠️ Success page not found after waiting.")


input("Press Enter to close the browser...")
driver.quit()