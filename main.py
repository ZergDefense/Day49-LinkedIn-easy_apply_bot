import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

ACCOUNT_EMAIL = os.environ['LINKEDIN_EMAIL']
ACCOUNT_PASSWORD = os.environ['LINKEDIN_PASSWORD']
PHONE = os.environ['PHONE_NUMBER']

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

service = Service(executable_path="C:\ChromeDriver-for-Selenium\chromedriver.exe")

driver = webdriver.Chrome(service=service, chrome_options=chrome_options)

driver.get(
    "https://www.linkedin.com/jobs/search/?currentJobId=3651001673&distance=25&f_LF=f_AL&geoId=106079947&keywords"
    "=junior%20python&refresh=true")

sign_in_button = driver.find_element(by=By.LINK_TEXT, value="Sign in")
sign_in_button.click()

# Wait for the next page to load.
time.sleep(5)

email_field = driver.find_element(by=By.ID, value="username")
email_field.send_keys(ACCOUNT_EMAIL)
password_field = driver.find_element(by=By.ID, value="password")
password_field.send_keys(ACCOUNT_PASSWORD)
password_field.send_keys(Keys.ENTER)

time.sleep(5)

all_listings = driver.find_elements(by=By.CSS_SELECTOR, value=".job-card-container--clickable")

for listing in all_listings:
    print("called")
    listing.click()
    time.sleep(2)

    # Try to locate the apply button, if can't locate then skip the job.
    try:
        apply_button = driver.find_element(by=By.CSS_SELECTOR, value=".jobs-s-apply button")
        apply_button.click()
        time.sleep(5)

        # If phone field is empty, then fill your phone number.
        phone = driver.find_element(by=By.CLASS_NAME, value="fb-single-line-text__input")
        if phone.text == "":
            phone.send_keys(PHONE)

        submit_button = driver.find_element(by=By.CSS_SELECTOR, value="footer button")

        # If the submit_button is a "Next" button, then this is a multi-step application, so skip.
        if submit_button.get_attribute("data-control-name") == "continue_unify":
            close_button = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
            close_button.click()
            time.sleep(2)
            discard_button = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__confirm-dialog-btn")[1]
            discard_button.click()
            print("Complex application, skipped.")
            continue
        else:
            submit_button.click()

        # Once application completed, close the pop-up window.
        time.sleep(2)
        close_button = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
        close_button.click()

    # If already applied to job or job is no longer accepting applications, then skip.
    except NoSuchElementException:
        print("No application button, skipped.")
        continue

time.sleep(5)
driver.quit()
