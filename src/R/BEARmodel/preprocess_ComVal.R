library(lubridate)

# ## 2013 - 2014 data
# movement_data2 = read.csv("baidu/7 feb/Baidu_LBS_flow_201312-201404.csv")
# cell_user_from_data = read.csv("baidu/7 feb/LBSusers_from_201312-201404.csv")
# cell_user_from_data$date = date(cell_user_from_data$date) + days(1)
# cell_user_to_data = read.csv("baidu/7 feb/LBSusers_to_201312-201404.csv")
# cell_user_to_data$date = date(cell_user_to_data$date) + days(1)

# 3 days data
movement_data = read.table("testmove_CV_normalmob_alt.csv",sep=",",header=T)

# simulate 48 days of data 
for (t in 1:4) {
  movement_data <- rbind(movement_data, movement_data)
}
d <- 1
for (i in seq(1, nrow(movement_data), by=6)) {
  movement_data$date[i:(i + 5)] <- d
  d <- d + 1
}

# convert dates to format R can read
movement_data$date = ymd("2020-02-25") + movement_data$date


# names of the patches. In this case 1, 2, 3, corresponding to
# 1 -> Castellón, 2 -> Valencia, 3 -> Alicante
patNames = unique(movement_data$to)[order(unique(movement_data$to))]

# names of the patches. In this case 1, 2, 3, corresponding to
# 1 -> Castellón, 2 -> Valencia, 3 -> Alicante
patIDs = 1:length(patNames)

# correspondence between patch names an patch ids
# 1 -> 1, 2 -> 2, 3 -> 3
pat_locator = data.frame(patNames, patIDs)

# 
# missing_dates = c(date("2014-1-17"), date("2014-2-2"),date("2014-2-18"),date("2014-2-20"),date("2014-3-1"),date("2014-3-2"))
# for (dates in 1:length(missing_dates)){
#   replaceday = subset(movement_data,Date == missing_dates[dates] - days(1))
#   replaceday$Date = replaceday$Date + days(1)
#   movement_data = rbind(movement_data,replaceday)
# }

# daily probability of recovery
recrate = 1 / 12 

# R0 of 2.68, 5.8 days till seeking treatment 
# How many people a single person potentially infects per day -- can be calculated from R0 estimate 
# if you divide R0 by infectious period
exposerate = 2.68 / 6 

# incubation period
exposepd = 5.1
