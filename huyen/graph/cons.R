install.packages(c("XLConnect", "dplyr", "ggplot2", "Hmisc"))

library("XLConnect")
library("dplyr")
library("ggplot2")
library("Hmisc")

wb <- loadWorkbook("huyen/graph/desc_stats.xlsx")
data <- readWorksheet(wb, sheet="Sheet1", startRow=1, endRow=32)

clean <- data %>%
  filter(!(is.na(cons)) & agm_at.e != ".") %>%
  mutate(agm = as.numeric(agm_at.e), cons = capitalize(cons)) %>%
  select(-agm_at.e)

ggplot(data = clean, aes(x=cumul.ll, y=agm)) + geom_point(col="red") +
  geom_text(aes(label=cons), hjust=0, vjust=0, angle=0, size=5, alpha=0.6) + theme_bw() +
  scale_x_continuous(limits = c(0, 65)) + 
  labs(x = "Cumulative number of Institutional/Governance",
       y = "Percentage of AGM attendance",
       title = "AGM Attendance and Technical Assistance at Base Line")
