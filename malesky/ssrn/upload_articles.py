import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # provide keyboard keys like RETURN, F1, etc.
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ff = webdriver.Firefox()

ff.get('https://hq.ssrn.com/login/pubSignInJoin.cfm?')

try:
    username = WebDriverWait(ff, 10).until(
        EC.presence_of_element_located((By.ID, "txtLogin"))
    )

    password = WebDriverWait(ff, 10).until(
        EC.presence_of_element_located((By.ID, "txtPassword"))
    )

    # these don't work cuz the page takes a while to load
    # username = selenium.find_element_by_id("txtLogin")
    # password = selenium.find_element_by_id("txtPassword")

    with open("credentials.txt", "r") as f:
        credentials = json.loads(f.read())
    username.send_keys(credentials["username"])
    password.send_keys(credentials["password"])

    submit = WebDriverWait(ff, 10).until(
        EC.presence_of_element_located((By.NAME, "signIn"))
    ).click()
except:
    print "Log in not found"

try:
    mypapers = WebDriverWait(ff, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "My Papers -"))
    ).click()

    newsubmission = WebDriverWait(ff, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='button'][@value='Start New Submission']"))
    ).click()
except:
    print "Link to My papers not found"

try:
    okmessage = WebDriverWait(ff, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='button'][@title='Continue']"))
    ).click()

    uploadfield = WebDriverWait(ff, 10).until(
        EC.presence_of_element_located((By.ID, "editAll"))
    ).click()
except:
    print "okmessage and expand all edit field"

try:
    uploadbutton = WebDriverWait(ff, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="file"][@name="FILE_NAME"]'))
    ).clear().send_keys('/home/anh/Desktop/AJPS_MaleskyGueorguiveJensen_Appendix.pdf')
except:
    print "can't upload"

try:
    title = WebDriverWait(ff, 10).until(
        EC.presence_of_element_located((By.XPATH, '//textarea[@id="ab_title"]'))
    ).clear().send_keys("Money Talks: Foreign Investment and Bribery in Vietnam, a Survey Experiment")
except:
    print "can't fill in title"

try:
    markaspublished = WebDriverWait(ff, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="rdoAbType"]'))
    ).click()
except:
    print "can't mark as published"

try:
    abstract = WebDriverWait(ff, 10).until(
        EC.presence_of_element_located((By.XPATH, '//textarea[@id="ab_content"]'))
    ).clear().send_keys('This is the online appendix to the correponding paper.')
except:
    print "can't fill in abstract"

try:
    classification = WebDriverWait(ff, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='radio][@name='SSRNeClass'"))
    ).click()
except:
    print "can't let SSRN classify"

try:
    monthwritten = WebDriverWait(ff, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='paper_month']"))
    ).clear()
    daywritten = WebDriverWait(ff, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='paper_day']"))
    ).clear()
    yearwritten = WebDriverWait(ff, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='paper_year']"))
    ).clear()
except:
    print "can't clear the date paper was written"

