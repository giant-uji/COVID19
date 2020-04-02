import os
import numpy as np
import pandas as pd
from src.python.plot import plot_seir
import src.python.datamanager as dm
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
# S'(t) = -betaS(t)I(t)/N
# E'(t) = betaS(t)I(t)/N - sigmaE(t)
# I'(t) = sigaE(t) - gammaI(t)
# R'(t) = gammaI(t)
# S(t) --> Susceptibles
# E(t) --> Expuestas
# I(t) --> Infectados
# R(t) --> Recuperados

beta = 1           # Tasa de transmisión, probabilidad de que un susceptible se infecte al entrar en contacto con un infectado.
gamma = 1 / 5      # tasa de recuperación, su inversa es el tiempo medio de recuperación.
sigma = 1 / 7      # tasa de incubación, su inversa es el tiempo promedio de incubación.
St0 = N = 5000000  # N Población total
It0 = 1            # Número de infectados iniciales
Et0 = 0            # Número de expuestos iniciales
Rt0 = 0            # Número de recuperado iniciales

# St_1 = St0
# It_1 = It0
# Et_1 = Et0
# Rt_1 = Rt0
# days = 120
# model_evolution = np.zeros((days, 4))
# for day in range(days):
#     St = St_1 - (beta * St_1 * It_1) / N
#     Et = Et_1 + (beta * St_1 * It_1) / N - (sigma * Et_1)
#     It = It_1 + (sigma * Et_1) - (gamma * It_1)
#     Rt = Rt_1 + (gamma * It-1)
#     St_1 = St
#     Et_1 = Et
#     It_1 = It
#     Rt_1 = Rt
#     model_evolution[day] = [St, Et, It, Rt]
#
# max_infected = np.argmax(model_evolution[:, 2])
# title = f'Pico de infectados: {model_evolution[max_infected, 2]:.2f} (día {max_infected})'
# df = pd.DataFrame(model_evolution, columns=['S(t)', 'E(t)', 'I(t)', 'R(t)'])
# plot_seir(data=df, features=['S(t)', 'E(t)', 'I(t)', 'R(t)'], title=title)
#
# St_1 = St0
# It_1 = It0
# Et_1 = Et0
# Rt_1 = Rt0
# betat = beta
# alpha0 = 0.5
# k = 100
# days = 240
# model_evolution = np.zeros((days, 4))
# for day in range(days):
#     St = St_1 - (betat * St_1 * It_1) / N
#     Et = Et_1 + (betat * St_1 * It_1) / N - (sigma * Et_1)
#     It = It_1 + (sigma * Et_1) - (gamma * It_1)
#     Rt = Rt_1 + (gamma * It-1)
#     betat = beta * (1 - alpha0) * (1 - 0.05 * It / N) ** k
#     St_1 = St
#     Et_1 = Et
#     It_1 = It
#     Rt_1 = Rt
#     model_evolution[day] = [St, Et, It, Rt]
#
# max_infected = np.argmax(model_evolution[:, 2])
# title = f'Pico de infectados: {model_evolution[max_infected, 2]:.2f} (día {max_infected})'
# df = pd.DataFrame(model_evolution, columns=['S(t)', 'E(t)', 'I(t)', 'R(t)'])
# plot_seir(data=df, features=['S(t)', 'E(t)', 'I(t)', 'R(t)'], title=title)
#
# # Con medidas variables en el tiempo
# St_1 = St0
# It_1 = It0
# Et_1 = Et0
# Rt_1 = Rt0
# betat = beta
# k = 100
# days = 500
# alpha = 0.7
# model_evolution = np.zeros((days, 4))
# for day in range(days):
#     St = St_1 - (betat * St_1 * It_1) / N
#     Et = Et_1 + (betat * St_1 * It_1) / N - (sigma * Et_1)
#     It = It_1 + (sigma * Et_1) - (gamma * It_1)
#     Rt = Rt_1 + (gamma * It-1)
#     if day < 20:
#         betat = beta
#     else:
#         betat = beta * (1 - alpha) * (1 - 0.05 * It / N) ** k
#     St_1 = St
#     Et_1 = Et
#     It_1 = It
#     Rt_1 = Rt
#     model_evolution[day] = [St, Et, It, Rt]
#
# max_infected = np.argmax(model_evolution[:, 2])
# title = f'Pico de infectados: {model_evolution[max_infected, 2]:.2f} (día {max_infected})'
# df = pd.DataFrame(model_evolution, columns=['S(t)', 'E(t)', 'I(t)', 'R(t)'])
# plot_seir(data=df, features=['S(t)', 'E(t)', 'I(t)', 'R(t)'], title=title)


# Con medidas variables en el tiempo
df_ccvv = pd.read_csv(os.path.join(dm.data_path, 'ccvv_covid19.csv'))
retired = df_ccvv['recovered'].to_numpy() + df_ccvv['deceased'].to_numpy()
infected = df_ccvv['cases'].to_numpy() - retired
first_day_series = df_ccvv['fecha'].iloc[0]
date1 = datetime.strptime('2020-' + first_day_series, '%Y-%m-%d')
beta = 1.0
gamma = 1 / 5.1
sigma = 1 / 12
St_1 = St0
It_1 = It0
Et_1 = Et0
Rt_1 = Rt0
betat = beta
days = 500
dates = [str(date1 + timedelta(days=d))[5:10] for d in range(-26, days + 26)]
sim_shift = -10
ccvv_day = 26
action1_day = ccvv_day + 13     # se suspenden fallas y magdalena  (11/3)
action2_day = action1_day + 2   # se anuncia estado de alarma      (13/3)
action3_day = action2_day + 2   # se declara estado de alarma      (15/3)
action4_day = action3_day + 14  # se refuerza estado de alarma +   (29/3)
alpha = [0.4, 0.5, 0.75, 0.85]
k = [100, 500, 1000, 1500]
model_evolution = np.zeros((days, 4))
for day in range(days):
    St = St_1 - (betat * St_1 * It_1) / N
    Et = Et_1 + (betat * St_1 * It_1) / N - (sigma * Et_1)
    It = It_1 + (sigma * Et_1) - (gamma * It_1)
    Rt = Rt_1 + (gamma * It-1)
    if day < action1_day:
        betat = beta
    elif day < action2_day:
        betat = beta * (1 - alpha[0]) * (1 - 0.05 * It / N) ** k[0]
    elif day < action3_day:
        betat = beta * (1 - alpha[1]) * (1 - 0.05 * It / N) ** k[1]
    elif day < action4_day:
        betat = beta * (1 - alpha[2]) * (1 - 0.05 * It / N) ** k[2]
    else:
        betat = beta * (1 - alpha[3]) * (1 - 0.05 * It / N) ** k[3]
    St_1 = St
    Et_1 = Et
    It_1 = It
    Rt_1 = Rt
    model_evolution[day] = [St, Et, It, Rt]


max_infected = np.argmax(model_evolution[:, 2])
title = f'Pico de infectados: {model_evolution[max_infected, 2]:.2f} (día {max_infected})'
df = pd.DataFrame(model_evolution, columns=['S(t)', 'E(t)', 'I(t)', 'R(t)'])
plt_max_day = 60
plt_max_pop = 1000
fig, ax = plt.subplots(1, 1, figsize=(10, 5), dpi=200)
for feature in ['S(t)', 'E(t)', 'I(t)', 'R(t)']:
    ax.plot(dates[(sim_shift + ccvv_day):(len(df[feature]) + sim_shift + ccvv_day)], df[feature], label=feature)
ax.plot(dates[ccvv_day:(len(retired) + ccvv_day)], retired)
ax.plot(dates[ccvv_day:(len(infected) + ccvv_day)], infected)
ax.set_ylim(ymin=0, ymax=plt_max_pop)
ax.set_xlim(xmin=-sim_shift, xmax=plt_max_day - sim_shift)
plt.axvline(dates[action1_day])
plt.axvline(dates[action2_day])
plt.axvline(dates[action3_day])
plt.axvline(dates[action4_day])
ax.xaxis.set_tick_params(rotation=90, labelsize=6)
plt.legend()
plt.suptitle(title)
plt.show()
