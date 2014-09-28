rm(list=ls())

options(stringsAsFactors = FALSE)

toInstall <- c("XML", "devtools", "RCurl", "digest")
lapply(toInstall, library, character.only = TRUE)

# ---- Look through table ----

look_through <- function(table) {
  for (i in 1:length(table)) {
    if (length(table[[i]]) != 0) {
      print(i)
      print(head(table[i]))
    }
  }
}

# ---- Scrape player match from team ----

scrape_player <- function(team_name) {
  url <- paste("http://www.football-lineups.com/team/", team_name, 
               "/Champions_League_2004_2005/Stats/Most_Capped/", sep='')
  url.data <- htmlParse(url)
  tables <- readHTMLTable(url.data)
  tryCatch({
    print(team_name)
    table <- as.data.frame(tables[[20]])
    table <- table[1:(nrow(table)-1), 2:4]
    return(table)
  }, error=function(cond) {
    message(paste("Here is the problem team", team_name))
    message(cond)
    return(NA)
  })
}

# ---- Scrape player profile link ----

scrape_player_link <- function(team_name) {
  url <- paste("http://www.football-lineups.com/team/", team_name, 
               "/Champions_League_2004_2005/Stats/Most_Capped/", sep='')
  url.data <- htmlParse(url)
  links <- xpathApply(url.data, 
    '//*[@id="mainarea"]/tbody/tr/td[1]/table[2]/tbody/tr[2]/td[2]/a/@href', xmlAttrs)
  return(links)
}