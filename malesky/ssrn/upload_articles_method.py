import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # provide keyboard keys like RETURN, F1, etc.
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
with open("credentials.txt", "r") as f:
        credentials = json.loads(f.read())

driver.get('https://hq.ssrn.com/login/pubSignInJoin.cfm?')
wait = WebDriverWait(driver, 20)

def wait_then_click(driver, xpath):
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    ).find_element_by_xpath("..").click() # Click the parent element first
    driver.find_element_by_xpath(xpath).click()

try:
    with open("credentials.txt", "r") as f:
        credentials = json.loads(f.read())

    username = wait.until(
        EC.presence_of_element_located((By.ID, "txtLogin"))
    ).send_keys(credentials["username"])

    password = wait.until(
        EC.presence_of_element_located((By.ID, "txtPassword"))
    ).send_keys(credentials["password"])

    # these don't work cuz the page takes a while to load
    # username = selenium.find_element_by_id("txtLogin")
    # password = selenium.find_element_by_id("txtPassword")

    submit = wait.until(
        EC.presence_of_element_located((By.NAME, "signIn"))
    ).click()
except:
    print "Log in not found"

wait_then_click(driver, "//a[@href='http://hq.ssrn.com/submissions/MyPapers.cfm?partid=915350']")
wait_then_click(driver, "//input[@type='button'][@value='Start New Submission']")
