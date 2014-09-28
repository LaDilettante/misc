from unicode_csv import UnicodeWriter
import time
import pickle
import sys
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import *

file_player_link2 = open("clean_result_player_link2")
result_player_link = pickle.load(file_player_link2)

links = list()
for i in range(len(result_player_link)):
    links.append(result_player_link[i][1])
result = list()
result_file = open("result_file.csv", "a")
wr = UnicodeWriter(result_file)


for link in links[6234:]:
    proxy = ["173.9.233.186", "54.227.39.120", "194.141.96.1", "218.108.232.190", "80.193.214.233", "125.39.171.194"]
    port = [3128, 80, 8080, 843, 3128, 86]
    while True:
        chosen = random.randint(0, len(proxy)-1)
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", proxy[chosen])
        profile.set_preference("network.proxy.http_port", port[chosen])
        profile.update_preferences()
        ff = webdriver.Firefox(firefox_profile=profile)
        ff.set_page_load_timeout(20)
        try:
            ff.get(link)
            while ff.find_element_by_tag_name("b").text == "Server under heavy load":
                print "Server under heavy load. Sleep now"
                time.sleep(150)
                ff.get(link)
        except TimeoutException:
            print " ".join((proxy[chosen], "load more 30s. Get new proxy"))
            ff.quit()
            continue
        except:
            print sys.exc_info()[0], "Problem getting link. Sleep now", str(links.index(link))
            ff.quit()
            time.sleep(150)
            continue
        else:
            break

    try:
        playername = ff.find_element_by_class_name("fn")
    except NoSuchElementException:
        print "No such playername"
        name = "NA"
    else:
        name = playername.text

    try:
        playtime = ff.find_element_by_xpath("//td[ b[text() = 'Minutes:'] ]")
    except NoSuchElementException:
        print "No such playtime"
        minute = "NA"
        percent = "NA"
    else:
        minute = playtime.text.split()[1]
        percent = playtime.text.split()[-1]

        #playername = WebDriverWait(ff, 60).until(
            #EC.presence_of_element_located((
                #By.CLASS_NAME, "fn"
            #))
        #)

        #playtime = WebDriverWait(ff, 60).until(
            #EC.presence_of_element_located((
                #By.XPATH, "//td[ b[text() = 'Minutes:'] ]"
            #))
        #)

    finally:
        wr.writerow([link, name, minute, percent])
        result.append([link, name, minute, percent])
        ff.close()

    print " ".join(("done", str(links.index(link))))
    time.sleep(random.randint(3,7))

result_file.close()

pickle.dump(result, open("result_file2", "w"))


# /html/body/form/section/article/div/table/tbody/tr/td/table[3]/tbody/tr[2]/td/span/table[2]/tbody/tr[12]/td/table/tbody/tr/td/table/tbody/tr[4]/td
