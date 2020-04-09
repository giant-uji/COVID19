# Load EpiModel
suppressMessages(library(EpiModel))

control <- control.icm(type = "SIR", nsteps = 100, nsims = 10)
init <- init.icm(s.num = 997, i.num = 3, r.num = 0)

param <- param.icm(inf.prob = 0.05, act.rate = 10, rec.rate = 1/20, 
                   a.rate = (10.5/365)/1000, ds.rate = (7/365)/1000, di.rate = (14/365)/1000, 
                   dr.rate = (7/365)/1000)

sim <- icm(param, init, control)

plot(sim)
plot(sim, y = "si.flow", mean.col = "red", qnts.col = "red")