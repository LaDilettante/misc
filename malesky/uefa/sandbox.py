from selenium import webdriver

link = "http://www.football-lineups.com"
#link = "http://www.python.org"
p = webdriver.Firefox()
p.get(link)
print p.title
p.close()
