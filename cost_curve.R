rm(list=ls())
library(plyr)
library(zoo)
library(chron)
library(ggplot2)

# ---- Mock data ----
data <- data.frame(name = c("project1", "project2", "project3"),
                   start = c("Feb-2008", "Apr-2006", "May-2005"),
                   end = c("Apr-2012", "Sep-2013", "Jul-2012"),
                   totexp = c(4577, 263, 2374))

# ---- Some constants ----
c_numAll <- 10
c_startMid <- 3
c_endMid <- 8
c_numMid <- 6
c_ratioMid <- 0.7
c_newFiscal <- "10-01"

# ---- Clearning date ----

data <- within(data, start <- as.yearmon(start, "%b-%Y"))
data <- within(data, start <- as.Date.yearmon(start, frac=0))
data <- within(data, end <- as.yearmon(end, "%b-%Y"))
data <- within(data, end <- as.Date.yearmon(end, frac=1))

# Split a project into units
f_splitIntoUnit <- function(row) {
  cost <- row[ , "totexp"] / c_numMid
  startDate <- seq(from = row[, "start"], to = row[, "end"], length.out = c_numAll)[c_startMid:c_endMid]
  endDate <- seq(from = row[, "start"], to = row[, "end"], length.out = c_numAll)[(c_startMid+1):(c_endMid+1)]
  return(data.frame(name = row[ , "name"], startDate = startDate, 
                    endDate = endDate, cost = cost))
  
}

# Turn year into fiscal year
f_splitIntoFiscalYear <- function(row) {
  if (as.Date(format(row$startDate, "%m-%d"), format="%m-%d") < as.Date(c_newFiscal, format="%m-%d")) {
    # if project start date is before the new fiscal year
    startFiscalYear <- as.numeric(format(row$startDate, "%Y"))
  } else {
    startFiscalYear <- as.numeric(format(row$startDate, "%Y")) + 1
  }
  
  if (as.Date(format(row$endDate, "%m-%d"), format="%m-%d") >= as.Date(c_newFiscal, format="%m-%d")) {
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
    
    data.frame(name = rep(row$name, 2), 
               year = c(startFiscalYear, endFiscalYear), time = c(time1, time2),
               cost = c(cost1, cost2))
  } else {
    time <- chron(format(row$endDate), format="y-m-d") - chron(format(row$startDate), format="y-m-d")
    data.frame(name = row$name, year = startFiscalYear, time = time, cost = row$cost)
  }
}

# Do it
df_splitIntoUnit <- ddply(data, c("name"), f_splitIntoUnit)
df_splitIntoFiscalYear <- ddply(df_splitIntoUnit, c("startDate"), f_splitIntoFiscalYear)
df_summary <- ddply(df_splitIntoFiscalYear, c("year"), summarize, tot = sum(cost))
df_summary <- data.frame(name = rep("all projects", nrow(df_summary)), df_summary)
df_summary2 <- ddply(df_splitIntoFiscalYear, c("name", "year"), summarize, tot = sum(cost))
df_summary3 <- rbind(df_summary2, df_summary)

# Preview the result
df_summary
df_summary3

# Plot the result
ggplot() + 
  geom_line(data=df_summary3, aes(x=year, y=tot, col=name))
ggsave("cost_curve.png")
