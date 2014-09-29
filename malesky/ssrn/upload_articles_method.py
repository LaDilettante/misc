import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # provide keyboard keys like RETURN, F1, etc.
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 5)

def wait_then_click(xpath, clickparent=True, driver=driver, wait=wait):
    if clickparent == True:
        wait.until(
            EC.presence_of_element_located((By.XPATH, xpath))
        ).find_element_by_xpath("..").click() # Click the parent element first
        driver.find_element_by_xpath(xpath).click()
        print xpath + "done with parent"
    else:
        wait.until(
            EC.presence_of_element_located((By.XPATH, xpath))
        ).click()
        print xpath + "done without parent"

def wait_then_sendkeys(xpath, keys, clear=False, driver=driver):
    if clear==False:
        wait.until(
                EC.presence_of_element_located((By.XPATH, xpath))
        ).send_keys(keys)
        print xpath + "done - no clear"
    else:
        wait.until(
                EC.presence_of_element_located((By.XPATH, xpath))
        ).clear().send_keys(keys)
        print xpath + "done - with clear"

driver.get('https://hq.ssrn.com/login/pubSignInJoin.cfm?')
try:
    with open("credentials.txt", "r") as f:
        credentials = json.loads(f.read())

    wait_then_sendkeys("//input[@id='txtLogin']", credentials["username"])
    wait_then_sendkeys("//input[@id='txtPassword']", credentials["password"])
    wait_then_click("//input[@name='signIn']", clickparent=False)
except:
    print "Log in not found"

# # My papers
# wait_then_click("//a[@href='http://hq.ssrn.com/submissions/MyPapers.cfm?partid=915350']")
# # Start new submission
# wait_then_click("//input[@type='button'][@value='Start New Submission']", clickparent=False)
# # Ok message
# wait_then_click("//input[@type='button'][@title='Continue']", clickparent=False)

driver.get('http://hq.ssrn.com/submissions/SimpleSubmission.cfm?AbstractID=2502658&NewABID=1&show=JyMsPyRVT0NaPDAgIAo=#top')
# Ok message
wait_then_click("//input[@type='button'][@title='Continue']", clickparent=False)
# Expand all
wait_then_click("//a[@id='editAll']")
# Upload
wait_then_sendkeys('//input[@type="file"]',
    '/home/anh/Desktop/AJPS_MaleskyGueorguiveJensen_Appendix.pdf')
# wait.until(
#     EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
# ).send_keys('/home/anh/Desktop/AJPS_MaleskyGueorguiveJensen_Appendix.pdf')

# driver.execute_script('document.querySelector(\"input[name=\'FILE_NAME\']\").setAttribute(\"value\", \"/home/anh/Desktop/AJPS_MaleskyGueorguiveJensen_Appendix.pdf\")')


# Title
wait_then_sendkeys("//textarea[@id='ab_title']",
    "Money Talks: Foreign Investment and Bribery in Vietnam, a Survey Experiment")
# Mark as published
wait_then_click('//input[@name="rdoAbType"]')
# Abstract
wait_then_sendkeys('//textarea[@id="ab_content"]', 
    'This is the online appendix to the correponding paper.')
# Let SSRN classify the paper
wait_then_click("//input[@type='radio][@name='SSRNeClass'")
# Month / day / year written
wait_then_sendkeys("//input[@id='paper_month']", "", clear=True)
wait_then_sendkeys("//input[@id='paper_day']", "", clear=True)
wait_then_sendkeys("//input[@id='paper_year']", "", clear=True)
