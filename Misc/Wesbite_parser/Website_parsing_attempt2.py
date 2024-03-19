from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui

#driver_path = r'...chromedriver-win64\chromedriver-win64'

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = r'...chrome-win64\chrome.exe' 

driver = webdriver.Chrome(options=chrome_options)

website_url = '...wesbite...'
#...wesbite.../Dashboard/Index
#...wesbite.../LeaveManagement/LeaveRequestStatus
#...wesbite.../LeaveManagement/Apply#tabApplyWFH

"""Explore inspect page

<span id="show-hide-sidebar" class="checkbox-toggle">
<input type="checkbox" checked>
<button id="show-hide-sidebar-toggle" class="active toggle-menu">
<i class="fa fa-bars"></i>
</button>
<label for="show-hide-sidebar-toggle"></label>
</span>"""

driver.get(website_url)

wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Login via SSO")]')))
print("Wait complete for SSO login")

initial_cookies = driver.get_cookies()

sso_button = driver.find_element(By.XPATH, '//button[contains(text(), "Login via SSO")]')
#print("SSO button found: {0}".format(sso_button))
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
    username_field.send_keys('...username...')  

    next_button = driver.find_element(By.ID, 'idSIButton9')
    next_button.click()
    time.sleep(2)

    wait.until(EC.element_to_be_clickable((By.NAME, 'passwd')))
    password_field = driver.find_element(By.NAME, 'passwd')
    password_field.send_keys('...password...')

    sign_in_button = driver.find_element(By.ID, 'idSIButton9')
    sign_in_button.click()
    time.sleep(2)

for handle in driver.window_handles:
    if handle != main_window_handle:
        popup_window_handle = handle
        break

if popup_window_handle:
    #microsoft authenticator
    driver.switch_to.window(popup_window_handle)
    time.sleep(10)
    #post_login_cookies = driver.get_cookies()

    #for cookie in post_login_cookies:
    #    driver.add_cookie(cookie)
    print("reached authenticator")

for handle in driver.window_handles:
    if handle != main_window_handle:
        popup_window_handle = handle
        break

if popup_window_handle:
    # remain signed in
    print("reached signed in")
    driver.switch_to.window(popup_window_handle)
    time.sleep(2)
    pyautogui.press("enter")
    #pyautogui.typewrite('\n')
    #pyautogui.hotkey('enter')

driver.switch_to.window(main_window_handle)

'''
wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Leave Management")]')))
leave_management_item = driver.find_element(By.XPATH, '//span[contains(text(), "Leave Management")]')
leave_management_item.click()

wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Apply")]')))
leave_apply_link = driver.find_element(By.XPATH, '//a[contains(span, "Apply")]')
leave_apply_link.click()

wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Work From Home")]')))
wfh_tab = driver.find_element(By.XPATH, '//span[contains(text(), "Work From Home")]')
wfh_tab.click()
'''

print("reached navigation")

#driver.refresh()

#website_url = '...wesbite.../LeaveManagement/Apply#tabApplyWFH'
#driver.get(website_url)

time.sleep(20)

# Find the "Leave Management" menu
leave_management_menu = driver.find_element(By.XPATH, "//span[text()='Leave Management']")

# Click the "Leave Management" menu to expand the submenu
leave_management_menu.click()

# Find and click the "Apply" link under "Leave Management"
apply_wfh_link = driver.find_element(By.XPATH, "//a[@href='...wesbite.../LeaveManagement/Apply']")
apply_wfh_link.click()

#work_from_home_tab =driver.find_element(By.XPATH, "//a[@href='#tabApplyWFH']")))
work_from_home_tab = driver.find_element(By.XPATH, "//a[@href='#tabApplyWFH']")
work_from_home_tab.click()
driver.execute_script("window.__cfRLUnblockHandlers = true;")
work_from_home_tab.click()
time.sleep(5)
work_from_home_tab.click()

time.sleep(5)
#date_select = driver.find_element(By.ID, 'WorkFromHomeDate')
#date_select.select_by_visible_text('09/01/2023')  # Replace with the desired date option
#date_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'WorkFromHomeDate')))
#wait.until(EC.element_to_be_clickable((By.NAME, 'WorkFromHomeDate')))
date_dropdown = driver.find_element(By.ID, 'WorkFromHomeDate')
date_dropdown.find_element(By.XPATH, "//option[@value='12944']").click()

reason_textarea = driver.find_element(By.ID, 'WFHReason')
reason_textarea.clear()  # Clear any existing text (optional)
reason_textarea.send_keys('Requesting WFH to maintain productivity and enjoy the allowed flexibility')  # Replace with your reason

#submit_button = driver.find_element(By.ID, 'btnSubmitLeave')
#submit_button.click()

time.sleep(20)
driver.quit()
