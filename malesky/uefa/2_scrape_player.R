rm(list=ls())
library(XML)

url <- "http://www.football-lineups.com/footballer/71534/?t=1003"

# data <- xmlInternalTreeParse(url)
# data <- xmlParse(url)
data <- htmlParse(url) # Website seems malformed so must go with htmlParse

a <- getNodeSet(data, '//*[@id="spangraphmsg"]') # Got nothing
b <- getNodeSet(data, '//a[@href]') # Got a bunch of links

node <- getNodeSet(data, '//tr[15]/td/table/tbody/tr/td[1]/table/tbody/tr/td')
test <- xpathApply(data, '//tr[15]/td/table/tbody/tr/td[1]/table/tbody/tr/td', xmlValue)
test # Nothin'

url2 <- "http://www.football-lineups.com/team/Arsenal/Champions_League_2012-2013/Stats/Most_Capped/"
data2 <- htmlParse(url2)
node2 <- getNodeSet(data2, '//*[@id="mainarea"]/tr/td[1]/table[2]')
test2 <- xpathApply(data2, '//*[@id="mainarea"]/tr/td[1]/table[2]', xmlValue)
test2