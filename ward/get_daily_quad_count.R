rm(list=ls())
toLoad <- c("RMySQL", "plyr")
lapply(toLoad, library, character.only=TRUE)

# Connection
conn <- dbConnect(MySQL(), user="aql3", password="gdeltmike97", 
                  dbname="event_data", host="152.3.32.10")

quadEvents <- function(cameo.codes, date=NULL, source.country=NULL, target.country=NULL) {
  # Gets relevant event counts for the given CAMEO codes and 
  # the given country interaction, e.g. countryA to countryB
  # country is given as ISOA3Code
  sql.select <- ("SELECT e.event_date AS DATE
                  , cSource.ISOA3Code AS source_country
                  , cTarget.ISOA3Code AS target_country
                  , COUNT(*) AS quad_count")
  sql.from <- ("FROM simple_events e
                  JOIN eventtypes t ON e.eventtype_id = t.eventtype_ID
                  JOIN countries cSource ON e.source_country_id = cSource.id
                  JOIN countries cTarget ON e.target_country_id = cTarget.id")
  
  # Write the where clause, which depends on whether country is supplied or not
  # If not, use all the countries, i.e. only impose the cameo.codes where condition
  sql.where <- paste("WHERE", paste("SUBSTRING(t.code, 1, 2) IN", cameo.codes))
  if (!is.null(source.country)) {
    sql.where <- paste(sql.where, "AND", 
                       paste0("cSource.ISOA3Code IN ('", source.country, "')"))
  }
  if (!is.null(target.country)) {
    sql.where <- paste(sql.where, "AND", 
                       paste0("cTarget.ISOA3Code IN ('", target.country, "')"))
  }
  # date is YYYYMMDD
  if (!is.null(date)) {
    sql.where <- paste(sql.where, "AND",
                       paste0("e.event_date IN (STR_TO_DATE('", date, "', '%Y%m%d'))"))
  }
  
  # Write the group by clause, grouping by date, source, and target
  sql.group <- ("GROUP BY e.event_date, e.source_country_id, e.target_country_id
                ORDER BY e.event_date ASC")
  
  # Paste the select, from, where, group clause
  sql <- paste(sql.select, sql.from, sql.where, sql.group, ";")
  
  # Get and return the result
  res <- dbGetQuery(conn, sql)
  return(res)
}

getIcewsQuad <- function(quad, date=NULL, source.country=NULL, target.country=NULL) {
  # quad: verb.coop, verb.conf, matl.coop, matl.confl
  # country: ISOA3Code
  if (!exists("conn")) stop("No MySQL connection ('conn')")
  
  # Get SQL list of roots codes for quad category
  quad.root.codes <- list(
    verb.coop="('01', '02', '03', '04', '05')",
    matl.coop="('06', '07', '08')",
    verb.conf="('09', '10', '11', '12', '13')",
    matl.conf="('14', '15', '16', '17', '18', '19', '20')"
  )
  cameo.codes <- quad.root.codes[[quad]]
  
  # Get counts from DB
  counts <- quadEvents(cameo.codes, date, source.country, target.country)
  
  if (nrow(counts) > 0) {
    res <- data.frame(date=counts[ , 1], 
                      source_country=counts[ , 2],
                      target_country=counts[ , 3],
                      quad_category=rep(quad, nrow(counts)), 
                      quad_count=counts[ , 4])  
  } else {
    res <- data.frame(date=NULL, 
                      source_country=NULL, target_country=NULL, 
                      quad_category=NULL, quad_count=NULL)
  }
  
  return(res)
}


quads <- c("verb.coop", "verb.conf", "matl.coop", "matl.conf")

# Get quad counts between all country-dyads in a given date
result1 <- ldply(quads, .fun=getIcewsQuad, date="20021025")

# Get quad counts between one dyad for all dates
result2 <- ldply(quads, .fun=getIcewsQuad, 
                 source.country="AFG", target.country="ALB")

# Get quad counts for one dyad in one date
result3 <- ldply(quads, .fun=getIcewsQuad, date="20021025", 
                 source.country="AFG", target.country="ALB")

head(result1)
head(result2)
head(result3)
