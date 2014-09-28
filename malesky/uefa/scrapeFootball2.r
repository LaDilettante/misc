# remove "#" from setwd command below to set working directory
# and be sure to escape \ with \\ in directory name

#setwd("C:\\WorkingDirectory")

library(XML)
library(RCurl)

################################################################################
# Loop to get "Most Capped" Data
# 
################################################################################


years <- c('2004_2005','2005-2006','2006-2007','2007-2008','2008-2009','2009-2010','2010-2011','2011-2012','2012-2013')

for (i in 1:length(years)){

#Test URL <- paste0("http://www.football-lineups.com/tourn/Champions_League_",'2005-2006',"/Stats/Players_Used")
Url <- paste0("http://www.football-lineups.com/tourn/Champions_League_",years[i],"/Stats/Players_Used")
webpage <- getURL(Url)
webpage <- readLines(tc <- textConnection(webpage)); close(tc)
webpageLine <- webpage[grepl("click for detail",webpage)]
webpageLine <- sub(".+?(?=Team \\(click for detail\\))","",webpageLine,perl=TRUE)
webpageLine <- sub("?Total.*", "", webpageLine)
webpageLine <- paste("<table> <td>",webpageLine, "</table>")
webpageLine <- htmlParse(webpageLine)
ahref = getNodeSet(webpageLine, "//a/@href") #Collects Links
	ahref <- unlist(ahref)
soccerdata <- as.data.frame( readHTMLTable(webpageLine) )

#Column names must be added back in; dashes replaced with 0s
names(soccerdata) <- c("Team","PlayersUsed","Foreigners","AverageAge")
soccerdata <- soccerdata[!is.na(soccerdata$PlayersUsed),]

#Merge the Link data to dataframe
soccerdata$CountryLink <- ahref[ seq(1,length(ahref),2) ]
soccerdata$TeamLink <- ahref[ seq(2,length(ahref),2) ]
soccerdata$Year <- years[i]

if (i == 1) { MostCapped <- soccerdata }

MostCapped <- rbind(MostCapped,soccerdata)
rm(soccerdata)
Sys.sleep( runif(1,0,.2) )
}

MostCapped$MCid <- seq_along(MostCapped[,1])
TeamLinks <- paste0("http://www.football-lineups.com/", MostCapped$TeamLink)
Team <- MostCapped$Team
#MostCapped <- SaveValue

############################3
# Loop through and merge team data

rm(i)
for (i in 1:length(TeamLinks)) {

#Test URL <- "http://www.football-lineups.com/team/Real_Madrid/Champions_League_2008-2009/Stats/Most_Capped/"

#Add While Loop in case football-linups server doesn't keep with loop

teamdata <- NA

URL <- TeamLinks[i]
webpage <- getURL(URL)
webpage <- readLines(tc <- textConnection(webpage)); close(tc)
webpage <- paste(webpage, collapse='')
webpageLine <- sub(".+(lineups and substitutions. &nbsp;&nbsp;&nbsp; )","",webpage,perl=TRUE)
webpageLine <- sub("?players used.*", "", webpageLine)
ps <- htmlParse(webpageLine)
teamdata <- readHTMLTable(ps,header=TRUE)
teamdata <- as.data.frame(teamdata)
teamdata[,1] <- NULL
print(length(teamdata) )

if (length(teamdata) <3 ) {
	print( paste("Error:",Team[i],"ID:",i) )
	break
	}


names(teamdata) <- c("Player","Position", "Lineups")
teamdata <- teamdata[!is.na(teamdata$Player),]
teamdata$Position <- gsub(" .*","",teamdata$Position) #Keep only position initials
teamdata$Player <- gsub(",.*","",teamdata$Player) #Keep only last name
teamdata$Player <- gsub("[iI]n.*","",teamdata$Player) #Delete "in" comments
teamdata$Player <- gsub("[oO]ut.*","",teamdata$Player) #Delete "out" comments
teamdata$MCid <- i
teamdata$Team <- Team[i]

MostCapped <- merge(MostCapped,teamdata)
Sys.sleep( runif(1,0,1) )
}


write.table('FootBallLinupsData.csv',MostCapped,sep=',',row.names=FALSE)
print("FootBallLinupsData.csv written to file")
