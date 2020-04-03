#### Model running code for BEARmod v.0.6
rm(list=ls())
library(data.table) # fread - fastly reading data
library(lubridate)

# setwd('//worldpop.files.soton.ac.uk/Worldpop/Projects/WP519091_Seasonality')
# setwd('D:/OneDrive - University of Southampton/Wuhan Coronavirus R0/Spread risk')
# setwd('C:/Users/sl4m18/OneDrive - University of Southampton/Wuhan Coronavirus R0/Spread risk')

source("bearmod_fx.R")
source("preprocess_ComVal.R")

size = nrow(movement_data)
half_size = size / 2

# zero mobility
movement_data_zeromob = data.frame(movement_data)
movement_data_zeromob$movers = 0

# reduced mobility (50%)
movement_data_halfmob = data.frame(movement_data)
movement_data_halfmob$movers = movement_data_halfmob$movers * 0.5

# reduced mobility (50%) from day 25
movement_data_halfmob_halfperiod = data.frame(movement_data)
movement_data_halfmob_halfperiod$movers[(half_size + 1):size] = movement_data_halfmob_halfperiod$movers[(half_size + 1):size] * 0.5

# number of patches
NPat = length(patNames)

# number of oxposed people in each patch
patnExp = c(rep(0, NPat))

# pat_locator$pop = 4941509
# population for each patch (three provinces) 
pat_locator$pop = c(575470, 2540707, 1825332)

# number of infected
# start infection in Comunidad Valenciana
patnInf = c(20, 100, 35)

# recovery rate variable for each available day 
recover_df = data.frame(date=seq(from=min(movement_data$date), to=max(movement_data$date), by="days"), recrate = recrate)

# load a new mobility scenario 
relative_move_data = data.frame()
 
relative_move_data = read.table("zeroMobility_CV_alt.csv", sep=",", header=T)

# simulate 120 days of data 
for (t in 1:39) {
  relative_move_data <- rbind(relative_move_data, relative_move_data[1:18,])
}
d <- 1
for (i in seq(1, nrow(relative_move_data), by=6)) {
  relative_move_data$date[i:(i + 5)] <- d
  d <- d + 1
}

# convert dates to format R can read
relative_move_data$date = ymd("2020-02-25") + relative_move_data$date
# relative_move_data$date = ymd("2020-02-25") + 3
 
#### Running the model  ####

HPop = InitiatePop(pat_locator,patnInf,patnExp)
###dates of simulation

input_dates = seq(from=min(movement_data$date), to=max(movement_data$date), by="days")
# input_dates = rep("2020-02-26", 30)
# input_dates = append(input_dates, rep("2020-03-27", 15))
# input_dates = append(input_dates, rep("2020-04-11", 50))

# input_dates = seq(from=min(movement_data$date),to=max(movement_data$date),by="days")
# input_dates = seq(date("2020-02-26"),date("2020-4-26"),by="days") # coresponding to the period from 2020-12-08 to 2 wks after LNY's day 
# input_dates = seq(date("2013-12-02"),date("2014-2-27"),by="days") # coresponding to the period from 2020-12-08 to 4 wks after LNY's day
results = list()

HPop_update1 = runSim(HPop,
                      pat_locator,
                      relative_move_data,
                      movement_data, 
                      input_dates,recover_df, 
                      exposerate,exposepd,
                      exposed_pop_inf_prop=0, 
                      TSinday=1)
run = 1
results[[run]] = HPop_update1$all_spread
onerun1 <- data.frame(results[run])

HPop_update2 = runSim(HPop,
                      pat_locator,
                      relative_move_data,
                      movement_data_halfmob, 
                      input_dates,recover_df, 
                      exposerate,exposepd,
                      exposed_pop_inf_prop=0, 
                      TSinday=1)
run = 2
results[[run]] = HPop_update2$all_spread
onerun2 <- data.frame(results[run])

HPop_update3 = runSim(HPop,
                      pat_locator,
                      relative_move_data,
                      movement_data_zeromob, 
                      input_dates,recover_df, 
                      exposerate,exposepd,
                      exposed_pop_inf_prop=0, 
                      TSinday=1)
run = 3
results[[run]] = HPop_update3$all_spread
onerun3 <- data.frame(results[run])

# plot infected 
# plot(input_dates, onerun1$inf_1+onerun1$inf_2+onerun1$inf_3, col="blue", type='l', xlab="date", ylab="infected")
# lines(input_dates, onerun2$inf_1+onerun2$inf_2+onerun2$inf_3, col="dark red", lty=3)
# lines(input_dates, onerun3$inf_1+onerun3$inf_2+onerun3$inf_3, col="green", lty=3)
# legend("topleft", legend=c("Movilidad normal", "Movilidad media", "Sin movilidad"), 
#        col=c("blue", "dark red", "green"), lty=1:3, cex=0.8)

# plot SEIR 
# plot(input_dates, onerun1$inf_1 + onerun1$inf_2 + onerun1$inf_3, col="blue", type='l', 
#      xlab="date", ylab="population", ylim = c(0, 5000000))
# lines(input_dates, onerun1$exp_1 + onerun1$exp_2 + onerun1$exp_3, col="red", lty=1)
# lines(input_dates, onerun1$rec_1 + onerun1$rec_2 + onerun1$rec_3, col="green", lty=1)
# lines(input_dates, onerun1$sus_1 + onerun1$sus_2 + onerun1$sus_3, col="magenta", lty=1)
# legend("left", legend=c("infectious", "exposed", "recovered", "susceptible"), 
#        col=c("blue", "red", "green", "magenta"), lty=1)

par(mfrow=c(2,2))

plot(input_dates, onerun1$inf_1 + onerun1$inf_2 + onerun1$inf_3, col="blue", type='l', 
     xlab="date", ylab="population", ylim = c(0, 5000000), main="Comunidad Valenciana")
lines(input_dates, onerun1$exp_1 + onerun1$exp_2 + onerun1$exp_3, col="red", lty=1)
lines(input_dates, onerun1$rec_1 + onerun1$rec_2 + onerun1$rec_3, col="green", lty=1)
lines(input_dates, onerun1$sus_1 + onerun1$sus_2 + onerun1$sus_3, col="magenta", lty=1)
legend("left", legend=c("infectious", "exposed", "recovered", "susceptible"), 
       col=c("blue", "red", "green", "magenta"), lty=1, cex=0.7)


plot(input_dates, onerun1$inf_1, col="blue", type='l', 
     xlab="date", ylab="population", ylim = c(0, 600000), main="Castellón")
lines(input_dates, onerun1$exp_1, col="red", lty=1)
lines(input_dates, onerun1$rec_1, col="green", lty=1)
lines(input_dates, onerun1$sus_1, col="magenta", lty=1)
legend("left", legend=c("infectious", "exposed", "recovered", "susceptible"), 
       col=c("blue", "red", "green", "magenta"), lty=1, cex=0.7)


plot(input_dates, onerun1$inf_2, col="blue", type='l', 
     xlab="date", ylab="population", ylim = c(0, 2600000), main="Valencia")
lines(input_dates, onerun1$exp_2, col="red", lty=1)
lines(input_dates, onerun1$rec_2, col="green", lty=1)
lines(input_dates, onerun1$sus_2, col="magenta", lty=1)
legend("left", legend=c("infectious", "exposed", "recovered", "susceptible"), 
       col=c("blue", "red", "green", "magenta"), lty=1, cex=0.7)


plot(input_dates, onerun1$inf_3, col="blue", type='l', 
     xlab="date", ylab="population", ylim = c(0, 2000000), main="Alicante")
lines(input_dates, onerun1$exp_3, col="red", lty=1)
lines(input_dates, onerun1$rec_3, col="green", lty=1)
lines(input_dates, onerun1$sus_3, col="magenta", lty=1)
legend("left", legend=c("infectious", "exposed", "recovered", "susceptible"), 
       col=c("blue", "red", "green", "magenta"), lty=1, cex=0.7)


# for (run in 1:2){
#   
#   HPop_update2 = runSim(HPop,
#                         pat_locator,
#                         relative_move_data,
#                         movement_data, 
#                         input_dates,
#                         recover_df, 
#                         exposerate,
#                         exposepd,
#                         exposed_pop_inf_prop=0, 
#                         TSinday=1)
#   #print(paste0("Run # ",run))
#   results[[run]] = HPop_update2$all_spread
# }
# 
# # this is just one run of the model instance 10 
# onerun <- data.frame(results[run])
# 
# # plot infected 
# plot(onerun$X3, col="blue", lty=3)
# points(onerun$X3 * 2, col="dark red", lty=3)
# onerun$X3[35:48]

# save(results,file="results_ComVal.RData")
