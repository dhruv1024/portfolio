import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import pyautogui
import datetime

# Function to initialize the Selenium WebDriver
def initialize_driver(chrome_binary_location):
    print(f"Initializing WebDriver with Chrome binary location: {chrome_binary_location}\n")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = chrome_binary_location
    driver = webdriver.Chrome(options=chrome_options)

    #chrome_options.add_argument('--headless')  # Enable headless mode
    #chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration (often necessary for headless mode)
    #chrome_service = Service(executable_path=r'C:\Users\dhruv.sawhney\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')
    #driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    
    return driver

# Function to handle login with retry logic
def login(driver, website_url, sso_button_text, username, password, max_retries):
    retries = 0
    while retries < max_retries:
        try:
            print(f"Attempting to login to {website_url} (Attempt {retries + 1}/{max_retries})")
            driver.get(website_url)
            wait = WebDriverWait(driver, 10)
            wait.until(EC.element_to_be_clickable((By.XPATH, f'//button[contains(text(), "{sso_button_text}")]')))
            print("Waiting for SSO login button")

            initial_cookies = driver.get_cookies()

            sso_button = driver.find_element(By.XPATH, f'//button[contains(text(), "{sso_button_text}")]')
            driver.execute_script("window.__cfRLUnblockHandlers = true;")
            sso_button.click()
            time.sleep(5)
            sso_button.click()

            main_window_handle = driver.current_window_handle
            popup_window_handle = None
            wait.until(EC.number_of_windows_to_be(2))

            for handle in driver.window_handles:
                if handle != main_window_handle:
                    popup_window_handle = handle
                    break

            if popup_window_handle:
                driver.switch_to.window(popup_window_handle)
                wait.until(EC.element_to_be_clickable((By.NAME, 'loginfmt')))
                username_field = driver.find_element(By.NAME, 'loginfmt')
                username_field.send_keys(username)

                next_button = driver.find_element(By.ID, 'idSIButton9')
                next_button.click()
                time.sleep(2)

                wait.until(EC.element_to_be_clickable((By.NAME, 'passwd')))
                password_field = driver.find_element(By.NAME, 'passwd')
                password_field.send_keys(password)  # Mask the password
                print("Entered username and password")

                sign_in_button = driver.find_element(By.ID, 'idSIButton9')
                sign_in_button.click()
                time.sleep(2)

            return driver, main_window_handle

        except Exception as e:
            print(f"An error occurred during login: {str(e)}")
            retries += 1
            print(f"Retrying... (Attempt {retries}/{max_retries})")
            time.sleep(5)  # Adding a short delay before retry

    print(f"Max retry attempts reached. Failed to login after {max_retries} retries.")
    return None, None

# Function to handle Microsoft Authenticator with retry logic
def handle_microsoft_authenticator(driver, main_window_handle, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            popup_window_handle = None
            for handle in driver.window_handles:
                if handle != main_window_handle:
                    popup_window_handle = handle
                    break

            if popup_window_handle:
                driver.switch_to.window(popup_window_handle)
                time.sleep(10)  # Wait for Authenticator
                print("Reached authenticator")
                return True

            print("Failed to handle Microsoft Authenticator")
            retries += 1
            print(f"Retrying... (Attempt {retries}/{max_retries})")
            time.sleep(5)  # Adding a short delay before retry

        except Exception as e:
            print(f"An error occurred during Microsoft Authenticator handling: {str(e)}")
            retries += 1
            print(f"Retrying... (Attempt {retries}/{max_retries})")
            time.sleep(5)  # Adding a short delay before retry

    print(f"Max retry attempts reached. Failed to handle Microsoft Authenticator after {max_retries} retries.")
    return False

# Function to handle "Remain Signed In"
def handle_remain_signed_in(driver, main_window_handle, max_retries=3):
    for handle in driver.window_handles:
        if handle != main_window_handle:
            popup_window_handle = handle
            break

    if popup_window_handle:
        # Remain signed in
        print("Reached signed in")
        driver.switch_to.window(popup_window_handle)
        time.sleep(2)
        pyautogui.press("enter")
        return

# Function to navigate to the WFH application
def navigate_to_wfh_application(driver, main_window_handle):
    try:
        driver.switch_to.window(main_window_handle)
        time.sleep(20)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Leave Management")]')))
        leave_management_item = driver.find_element(By.XPATH, '//span[contains(text(), "Leave Management")]')
        leave_management_item.click()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Apply")]')))
        leave_apply_link = driver.find_element(By.XPATH, '//a[contains(span, "Apply")]')
        leave_apply_link.click()
        print("Reached navigation")

    except Exception as e:
        print(f"An error occurred during navigation to WFH application: {str(e)}")

# Function to apply for WFH
def apply_for_wfh(driver, wfh_reason, wfh_date):
    try:
        work_from_home_tab = driver.find_element(By.XPATH, "//a[@href='#tabApplyWFH']")
        work_from_home_tab.click()
        driver.execute_script("window.__cfRLUnblockHandlers = true;")
        work_from_home_tab.click()
        time.sleep(5)
        work_from_home_tab.click()
        time.sleep(5)

        date_dropdown = driver.find_element(By.ID, 'WorkFromHomeDate')
        # date_dropdown.find_element(By.XPATH, "//option[@value='12944']").click()
        date_dropdown.find_element(By.XPATH, f"//option[contains(text(), '{wfh_date}')]").click()

        reason_textarea = driver.find_element(By.ID, 'WFHReason')
        reason_textarea.clear()
        reason_textarea.send_keys(wfh_reason)

        time.sleep(20)
    except Exception as e:
        print(f"An error occurred during WFH application: {str(e)}")

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Automate login and application process.')
    parser.add_argument('--url', default='...website...', help='Website URL')
    parser.add_argument('--username', default='...username...', help='Username for login')
    parser.add_argument('--password', default='...password...', help='Password for login')
    parser.add_argument('--chrome_binary_location', \
                        default=r'...chrome-win64\chrome.exe' \
                        , help='Path to Chrome binary')
    parser.add_argument('--max_retries', type=int, default=3, help='Maximum retry attempts')
    parser.add_argument('--wfh_reason',
                        default='Requesting WFH to maintain productivity and enjoy the allowed flexibility',
                        help='WFH Reason')
    parser.add_argument('--wfh_date', default=datetime.datetime.now().strftime("%m/%d/%Y"), help='Date for WFH')
    args = parser.parse_args()

    try:
        driver = initialize_driver(args.chrome_binary_location)
        driver, main_window_handle = login(
            driver, args.url, "Login via SSO", args.username, args.password, args.max_retries)
        if handle_microsoft_authenticator(driver, main_window_handle, args.max_retries):
            handle_remain_signed_in(driver, main_window_handle, args.max_retries)
            navigate_to_wfh_application(driver, main_window_handle)
            apply_for_wfh(driver, args.wfh_reason, args.wfh_date)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if driver:
            driver.quit()
