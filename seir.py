# S'(t) = -betaS(t)I(t)/N
# E'(t) = betaS(t)I(t)/N - sigmaE(t)
# I'(t) = sigaE(t) - gammaI(t)
# R'(t) = gammaI(t)
# S(t) --> Susceptibles
# E(t) --> Expuestas
# I(t) --> Infectados
# R(t) --> Recuperados

beta = 1 # Tasa de transmisión, probabilidad de que un susceptible se infecte al entrar en contacto con un infectado.
gamma = 1/5 # tasa de recuperación, su inversa es el tiempo medio de recuperación.
sigma = 1/7 # tasa de incubación, su inversa es el tiempo promedio de incubación.
St0 = N =100000 # N Población total
It0 = 1 # Número de infectados iniciales
Et0 = 0 # Número de expuestos iniciales
Rt0 = 0 # Número de recuperado iniciales
St_1 = St0
It_1 = It0
Et_1 = Et0
Rt_1 = Rt0

for t in range(0,120):
    St = St_1 - (beta * St_1 * It_1)/N
    Et = Et_1 + (beta * St_1 * It_1) / N - (sigma * Et_1)
    It = It_1 + (sigma * Et_1) - (gamma * It_1)
    Rt = Rt_1 + (gamma * It-1)
    St_1 = St
    Et_1 = Et
    It_1 = It
    Rt_1 = Rt
    print(St, Et, It, Rt)