rm(list=ls())

# ---- Look through table and scrape player function ----

source("0_function.R")

# ---- Get team names ----
url_team <- "http://www.football-lineups.com/tourn/Champions_League_2004_2005/Stats/Players_Used/"
data_team <- htmlParse(url_team)
tables_team <- readHTMLTable(data_team)

# Run look_through to find out where is the wanted table
# look_through(tables_team)

# Table with team names is 22
all_teams <- tables_team[[22]][, 1]
# Truncate the header and the two footers
all_teams <- all_teams[2:(length(all_teams)-2)]
all_teams <- gsub(" ", "_", all_teams)

# ---- Scrape each team to get player stat ----

result <- sapply(all_teams, scrape_player, USE.NAMES=TRUE)

text <- result$Roma[, 1]
grep("Out", text)