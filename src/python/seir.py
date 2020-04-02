import numpy as np
import pandas as pd
from src.python.plot import plot_seir

# S'(t) = -betaS(t)I(t)/N
# E'(t) = betaS(t)I(t)/N - sigmaE(t)
# I'(t) = sigaE(t) - gammaI(t)
# R'(t) = gammaI(t)
# S(t) --> Susceptibles
# E(t) --> Expuestas
# I(t) --> Infectados
# R(t) --> Recuperados

beta = 1          # Tasa de transmisión, probabilidad de que un susceptible se infecte al entrar en contacto con un infectado.
gamma = 1 / 5     # tasa de recuperación, su inversa es el tiempo medio de recuperación.
sigma = 1 / 7     # tasa de incubación, su inversa es el tiempo promedio de incubación.
N = 48000000  # N Población total
It0 = 10           # Número de infectados iniciales
St0 = N - It0    # Número de susceptibles iniciales
Et0 = 0           # Número de expuestos iniciales
Rt0 = 0           # Número de recuperado iniciales
St = St0
It = It0
Et = Et0
Rt = Rt0
dt = 1/1
days_total = (int)(240 / dt)
days_before = (int)(30 / dt)

model_evolution = np.zeros((days_total, 4))

for day in range(days_before):
    dS = -((beta * St * It)/N) * dt
    dE = ((beta * St * It) / N - (sigma * Et)) * dt
    dI = ((sigma * Et) - (gamma * It)) * dt
    dR = ((gamma * It-1)) * dt
    St += dS
    Et += dE
    It += dI
    Rt += dR
    model_evolution[day] = [St, Et, It, Rt]
    print(St, Et, It, Rt)

beta = 0.5
for day in range(days_before, days_total):
    dS = -((beta * St * It)/N) * dt
    dE = ((beta * St * It) / N - (sigma * Et)) * dt
    dI = ((sigma * Et) - (gamma * It)) * dt
    dR = ((gamma * It-1)) * dt
    St += dS
    Et += dE
    It += dI
    Rt += dR
    model_evolution[day] = [St, Et, It, Rt]
    print(St, Et, It, Rt)

df = pd.DataFrame(model_evolution, columns=['S(t)', 'E(t)', 'I(t)', 'R(t)'])
plot_seir(data=df, features=['S(t)', 'E(t)', 'I(t)', 'R(t)'])
