library(lubridate)
library(data.table)

rm(list=ls())

source("bearmod_fx.R")

start_date = "2020-01-25"
n_days_sim = 365

# 3 days data por 3 patches
movement_data = read.table("testmove_CV_normalmob_alt.csv",sep=",",header=T)

# simulate n_days_sim days of data 
for (t in 1:(n_days_sim / 3 - 1)) {
  movement_data <- rbind(movement_data, movement_data[1:18,])
}
d <- 1
for (i in seq(1, nrow(movement_data), by=6)) {
  movement_data$date[i:(i + 5)] <- d
  d <- d + 1
}

# load a new mobility scenario 
relative_move_data = read.table("zeroMobility_CV_alt.csv", sep=",", header=T)

# simulate 120 days of data 
for (t in 1:(n_days_sim / 3 - 1)) {
  relative_move_data <- rbind(relative_move_data, relative_move_data[1:18,])
}
d <- 1
for (i in seq(1, nrow(relative_move_data), by=6)) {
  relative_move_data$date[i:(i + 5)] <- d
  d <- d + 1
}

# convert dates to format R can read
movement_data$date = ymd(start_date) + movement_data$date
relative_move_data$date = ymd(start_date) + relative_move_data$date

# names of the patches. In this case 1, 2, 3, corresponding to
# 1 -> Castellón, 2 -> Valencia, 3 -> Alicante
patNames = unique(movement_data$to)[order(unique(movement_data$to))]

# names of the patches. In this case 1, 2, 3, corresponding to
# 1 -> Castellón, 2 -> Valencia, 3 -> Alicante
patIDs = 1:length(patNames)

# correspondence between patch names an patch ids
# 1 -> 1, 2 -> 2, 3 -> 3
pat_locator = data.frame(patNames, patIDs)

# daily probability of recovery
recrate = 1 / 12 

# incubation period
exposepd = 5.1

size = nrow(movement_data)
half_size = size / 2

################################
# Different mobility scenarios #
################################

# zero mobility scenario
movement_data_zeromob = data.frame(movement_data)
movement_data_zeromob$movers = 0

# reduced mobility (50%) scenario
movement_data_halfmob = data.frame(movement_data)
movement_data_halfmob$movers = movement_data_halfmob$movers * 0.5

# reduced mobility (50%) from day 25 scenario
movement_data_halfmob_halfperiod = data.frame(movement_data)
movement_data_halfmob_halfperiod$movers[(half_size + 1):size] = movement_data_halfmob_halfperiod$movers[(half_size + 1):size] * 0.5

# number of patches
NPat <- length(patNames)

# number of oxposed people in each patch
patnExp <- c(rep(0, NPat))

# pat_locator$pop = 4941509
# population for each patch (three provinces) 
pat_locator$pop <- c(575470, 2540707, 1825332)

# number of infected
# start infection in Comunidad Valenciana
patnInf <- c(20, 100, 35)

# recovery rate variable for each available day 
recover_df <- data.frame(date=seq(from=min(movement_data$date), to=max(movement_data$date), by="days"), recrate = recrate)

# R0 of 2.68, 5.8 days till seeking treatment 
# How many people a single person potentially infects per day -- can be calculated from R0 estimate 
# if you divide R0 by infectious period
inf_period = 6
exposerate0 = 4.5 / inf_period

# exposed rate variable for each available day 
exposer_df <- data.frame(date=seq(from=min(movement_data$date), to=max(movement_data$date), by="days"), exposerate = exposerate0)

############################
# Different NPIs scenarios #
############################
# Lockdown from day 35
social_distancing_date <- "2020-03-09"
school_closure_date <- "2020-03-13"
lockdown_date <- "2020-03-14"
full_lockdown_date <- "2020-03-30"
end_lockdown_date <- "2020-04-12"
exposer_df$exposerate[exposer_df$date >= social_distancing_date] <- 4.5 / inf_period 
exposer_df$exposerate[exposer_df$date >= school_closure_date] <- 3.5 / inf_period 
exposer_df$exposerate[exposer_df$date >= lockdown_date] <- 1.5 / inf_period 
exposer_df$exposerate[exposer_df$date >= full_lockdown_date] <- 0.75 / inf_period 
exposer_df$exposerate[exposer_df$date >= end_lockdown_date] <- 1.5 / inf_period 

############################
#### Running the model  ####
############################
HPop = InitiatePop(pat_locator, patnInf, patnExp)

# dates of simulation
input_dates = seq(from=min(movement_data$date), to=max(movement_data$date), by="days")
results = list()

HPop_update1 = runSim(HPop,
                      pat_locator,
                      relative_move_data,
                      movement_data, 
                      input_dates,
                      recover_df, 
                      exposer_df,
                      exposepd,
                      exposed_pop_inf_prop=0, 
                      TSinday=1)
run = 1
results[[run]] = HPop_update1$all_spread
onerun1 <- data.frame(results[run])

par(mfrow=c(2, 2))

plot(input_dates, onerun1$inf_1 + onerun1$inf_2 + onerun1$inf_3, col="red", type='l', 
     xlab="date", ylab="population", ylim = c(0, 5000000), main="Comunidad Valenciana")
abline(v=c(which(social_distancing_date==input_dates)), col='blue', lty=1)
lines(input_dates, onerun1$exp_1 + onerun1$exp_2 + onerun1$exp_3, col="light blue", lty=1)
lines(input_dates, onerun1$rec_1 + onerun1$rec_2 + onerun1$rec_3, col="green", lty=2)
lines(input_dates, onerun1$sus_1 + onerun1$sus_2 + onerun1$sus_3, col="magenta", lty=3)
legend("left", legend=c("infectious", "exposed", "recovered", "susceptible"), 
       col=c("blue", "red", "green", "magenta"), lty=c(1, 1, 2, 3), cex=0.7)


plot(input_dates, onerun1$inf_1, col="red", type='l', 
     xlab="date", ylab="population", ylim = c(0, 600000), main="Castellón")
lines(input_dates, onerun1$exp_1, col="light blue", lty=1)
lines(input_dates, onerun1$rec_1, col="green", lty=2)
lines(input_dates, onerun1$sus_1, col="magenta", lty=3)
legend("left", legend=c("infectious", "exposed", "recovered", "susceptible"), 
       col=c("blue", "red", "green", "magenta"), lty=c(1, 1, 2, 3), cex=0.7)


plot(input_dates, onerun1$inf_2, col="red", type='l', 
     xlab="date", ylab="population", ylim = c(0, 2600000), main="Valencia")
lines(input_dates, onerun1$exp_2, col="light blue", lty=1)
lines(input_dates, onerun1$rec_2, col="green", lty=2)
lines(input_dates, onerun1$sus_2, col="magenta", lty=3)
legend("left", legend=c("infectious", "exposed", "recovered", "susceptible"), 
       col=c("blue", "red", "green", "magenta"), lty=c(1, 1, 2, 3), cex=0.7)


plot(input_dates, onerun1$inf_3, col="red", type='l', 
     xlab="date", ylab="population", ylim = c(0, 2000000), main="Alicante")
lines(input_dates, onerun1$exp_3, col="light blue", lty=1)
lines(input_dates, onerun1$rec_3, col="green", lty=2)
lines(input_dates, onerun1$sus_3, col="magenta", lty=3)
legend("left", legend=c("infectious", "exposed", "recovered", "susceptible"), 
       col=c("blue", "red", "green", "magenta"), lty=c(1, 1, 2, 3), cex=0.7)


# save(results,file="results_cv_test01.RData")
