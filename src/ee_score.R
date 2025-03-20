library(dplyr)
library(tidyr)
library(tibble)

#ee_2 <- read.csv('../data/raw/EE.csv')
#ee_2$date <- as.Date(ee_2$date, format = "%m/%d/%Y")

ee_pool <- read.csv('../data/raw/EE_pool.csv')
colnames(ee_pool) <- gsub("^X", "", colnames(ee_pool))
ee_pool$date <- as.Date(ee_pool$date, format = "%m/%d/%Y")

View(ee_pool)
str(ee_pool)
