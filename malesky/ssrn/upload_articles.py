import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # provide keyboard keys like RETURN, F1, etc.
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()

driver.get('https://hq.ssrn.com/login/pubSignInJoin.cfm?')

wait = WebDriverWait(driver, 20)

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

try:
    mypapers = wait.until(
        EC.presence_of_element_located((By.LINK_TEXT, "My Papers -"))
    ).find_element_by_xpath("..").click() # Click the parent element first
    driver.find_element_by_link_text("My Papers -").click()

    newsubmission = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='button'][@value='Start New Submission']"))
    ).find_element_by_xpath("..").click()
    driver.find_element_by_xpath("//input[@type='button'][@value='Start New Submission']").click()
except:
    print "Link to My papers not found"

try:
    okmessage = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='button'][@title='Continue']"))
    ).click()

    uploadfield = wait.until(
        EC.presence_of_element_located((By.ID, "editAll"))
    ).click()
except:
    print "okmessage and expand all edit field"

try:
    uploadbutton = wait.until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="file"][@name="FILE_NAME"]'))
    ).clear().send_keys('/home/anh/Desktop/AJPS_MaleskyGueorguiveJensen_Appendix.pdf')
except:
    print "can't upload"

try:
    title = wait.until(
        EC.presence_of_element_located((By.XPATH, '//textarea[@id="ab_title"]'))
    ).clear().send_keys("Money Talks: Foreign Investment and Bribery in Vietnam, a Survey Experiment")
except:
    print "can't fill in title"

try:
    markaspublished = wait.until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="rdoAbType"]'))
    ).click()
except:
    print "can't mark as published"

try:
    abstract = wait.until(
        EC.presence_of_element_located((By.XPATH, '//textarea[@id="ab_content"]'))
    ).clear().send_keys('This is the online appendix to the correponding paper.')
except:
    print "can't fill in abstract"

try:
    classification = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='radio][@name='SSRNeClass'"))
    ).click()
except:
    print "can't let SSRN classify"

try:
    monthwritten = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='paper_month']"))
    ).clear()
    daywritten = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='paper_day']"))
    ).clear()
    yearwritten = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='paper_year']"))
    ).clear()
except:
    print "can't clear the date paper was written"

