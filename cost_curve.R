rm(list=ls())

toLoad <- c("plyr", "zoo", "chron", "ggplot2", "cshapes")
lapply(toLoad, library, character.only=TRUE)

# ---- Mock data ----
# data <- data.frame(name = c("project1", "project2", "project3"),
#                    start = c("Feb-2008", "Apr-2006", "May-2005"),
#                    end = c("Apr-2012", "Sep-2013", "Jul-2012"),
#                    totexp = c(4577, 263, 2374))

# ---- Real data ----
raw.data <- read.csv("G:/AwardData.csv", na.strings=c("", "NA", "-10141"), stringsAsFactors=FALSE)

# ---- Some constants ----
c_numAll <- 10 # No. of time units in each project

# We don't define middle like this anymore
# c_startMid <- 3 # Which time unit is the first of the project's middle
# c_endMid <- 8 # Which time unit is the last of the project's middle
# c_numMid <- c_endMid - c_startMid + 1 # No. of time untis in the project's middle 

# Define middle by days in the beginning and end
c_beforeMid <- 10 * 7 
c_afterMid <- 20 * 7
c_numMid <- 10 # Divide the middle into smaller units so that they don't go over 3 FY
  
c_ratioMid <- 0.7 # How much of the total cost belongs to the project's middle
c_newFiscal <- "10-01" # When is the new fiscal year


# ---- Clean, rename variable ----

data.full <- raw.data
names(data.full)[names(data.full) == "START"] <- "old.START"
names(data.full)[names(data.full) == "AWARD_MECH"] <- "award_mech"
names(data.full)[names(data.full) == "AWARD_ID"] <- "name"
names(data.full)[names(data.full) == "CONT_START"] <- "start"
data.full <- within(data.full, end <- ifelse(!(is.na(CONT_END_AMD)), CONT_END_AMD, CONT_END_PLAN))
data.full <- within(data.full, totexp <- ifelse(!(is.na(AMEND_FIN_BUDG)), AMEND_FIN_BUDG, CONSTRUCT_BUDGET_PLAN))

data <- na.omit(data.full[, c("name", "start", "end", "totexp", "award_mech")])

apply(raw.data[, c("CONT_START", "CONT_END_PLAN", "CONT_END_AMD", "AMEND_FIN_BUDG", "CONSTRUCT_BUDGET_PLAN")],
      2, function(x) sum(!is.na(x)))

# ---- Clearning date ----

data <- within(data, start <- as.yearmon(start, "%b-%y"))
data <- within(data, start <- as.Date.yearmon(start, frac=0))
data <- within(data, end <- as.yearmon(end, "%b-%y"))
data <- within(data, end <- as.Date.yearmon(end, frac=1))

# Split a project into units
f_splitIntoUnit <- function(row) {
  cost <- row[ , "totexp"] / c_numMid
  startDate <- seq(from = row[, "start"] + c_beforeMid, to = row[, "end"] - c_afterMid, length.out = c_numMid)
  endDate <- seq(from = row[, "start"] + c_beforeMid, to = row[, "end"] - c_afterMid, length.out = c_numMid)
  return(data.frame(startDate = startDate, endDate = endDate, cost = cost))
  
}

# Turn each time unit into fiscal year (split across 2 years if necessary)
f_splitIntoFiscalYear <- function(row) {
  # Just compare two dates, year is irrelevant
  # Year 2020, a leap year, is chosen. Otherwise Feb 29th will be invalid
  if ( as.Date(paste("2020", format(row$startDate, "%m-%d"), sep="-"), format="%Y-%m-%d") < 
    as.Date(paste("2020", c_newFiscal, sep="-"), format="%Y-%m-%d") ) {
    # if project start date is before the new fiscal year
    startFiscalYear <- as.numeric(format(row$startDate, "%Y"))
  } else {
    startFiscalYear <- as.numeric(format(row$startDate, "%Y")) + 1
  }
  
  if ( as.Date(paste("2020", format(row$endDate, "%m-%d"), sep="-"), format="%Y-%m-%d") >= 
    as.Date(paste("2020", c_newFiscal, sep="-"), format="%Y-%m-%d") ) {
    # if project end date is after the new fiscal year
    endFiscalYear <- as.numeric(format(row$startDate, "%Y")) + 1
  } else {
    endFiscalYear <- as.numeric(format(row$startDate, "%Y"))
  }
  
  if (endFiscalYear > startFiscalYear) {
    cutpoint <- chron(paste(startFiscalYear:(endFiscalYear-1), c_newFiscal, sep="-"), format="y-m-d")
    time1 <- cutpoint - chron(format(row$startDate), format="y-m-d")
    time2 <- chron(format(row$endDate), format="y-m-d") - cutpoint
    cost1 <- as.numeric((time1 / (time1 + time2))) * row$cost
    cost2 <- row$cost - cost1
    
    data.frame(year = c(startFiscalYear, endFiscalYear), time = c(time1, time2),
               cost = c(cost1, cost2))
  } else {
    time <- chron(format(row$endDate), format="y-m-d") - chron(format(row$startDate), format="y-m-d")
    data.frame(year = startFiscalYear, time = time, cost = row$cost)
  }
}

# Do it
df_splitIntoUnit <- ddply(data, c("award_mech", "name"), f_splitIntoUnit, .inform=TRUE)
df_splitIntoFiscalYear <- ddply(df_splitIntoUnit, c("award_mech", "name", "startDate"), f_splitIntoFiscalYear, .inform=TRUE)
df_summary <- ddply(df_splitIntoFiscalYear, c("award_mech", "year"), summarize, tot = sum(cost))
#df_summary <- data.frame(name = rep("all projects", nrow(df_summary)), df_summary)
#df_summary2 <- ddply(df_splitIntoFiscalYear, c("name", "year"), summarize, tot = sum(cost))

# Preview the result
df_summary

# Plot the result
ggplot() + geom_bar(data=df_summary, aes(x=year, y=tot, fill=factor(award_mech)), stat="identity")
ggsave("cost_curve.png")
