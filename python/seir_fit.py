##################################################
# Fits a SEIR model with mobility restrictions
# to real data from Comunitat Valenciana (Spain)
##################################################
# Author: Emilio Sansano
# Email: esansano@uji.es
##################################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, DayLocator
from datetime import datetime, timedelta

from scipy.optimize import minimize


def plot_seir(df_seir, df_data, npi_data, zoom=None, title=''):
    cmap = plt.get_cmap('Set1')
    fig, ax = plt.subplots(1, 1, figsize=(10, 5), dpi=200)
    dates = [datetime.strptime(d, '%Y-%m-%d') for d in df_seir['date']]
    formatter = DateFormatter('%d-%m')
    locator = DayLocator()
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_tick_params(rotation=90, labelsize=8)
    ax.yaxis.set_tick_params(labelsize=8)

    # plot model curves
    ax.plot(dates, df_seir['susceptibles'], linestyle='-', color=cmap(1), alpha=0.25, label='Susceptibles')
    ax.plot(dates, df_seir['exposed'], linestyle='-', linewidth=4, color=cmap(3), alpha=0.25, label='Exposed')
    ax.plot(dates, df_seir['infectious'], linestyle='-', linewidth=4, color=cmap(0), alpha=0.25, label='Infectious')
    ax.plot(dates, df_seir['recovered'], linestyle='-', linewidth=4, color=cmap(2), alpha=0.25, label='Recovered')

    # plot real data
    ax.plot(dates, df_data['recovered'] + df_data['deaths'], linestyle='-', color=cmap(2), alpha=0.9,
            label='Actual recovered')
    ax.plot(dates, df_data['cases'], linestyle='-', color=cmap(0), alpha=0.9,
            label='Actual infectious')

    if zoom is not None:
        date1 = dates[0] + timedelta(days=zoom[0][0])
        date2 = dates[0] + timedelta(days=zoom[0][1])
        ax.set_xlim(xmin=date1, xmax=date2)
        ax.set_ylim(*zoom[1])

    # plot NPIs
    for npi in npi_data:
        date = datetime.strptime(npi_data[npi], '%Y-%m-%d')
        height = ax.get_ylim()[1]
        ax.axvline(date, linestyle='--', color='k', alpha=0.5)
        ax.text(date, height, npi, {'ha': 'right', 'va': 'top'}, rotation=90, size=8)

    ax.set_xlabel('population')
    ax.set_ylabel('date')
    ax.set_title(title)

    plt.legend(fontsize=8)
    plt.show()


def run_model(data, alphas, inf0, beta0, rect):
    # Tasa de transmisión, probabilidad de que un susceptible se infecte al entrar en contacto con un infectado.
    beta = beta0

    # tasa de recuperación, su inversa es el tiempo medio de recuperación.
    gamma = 1 / rect

    # tasa de incubación, su inversa es el tiempo promedio de incubación.
    sigma = 1 / 5

    # N Población total
    N = 5000000

    # Número de infectados iniciales
    It0 = inf0

    # Número de susceptibles iniciales
    St0 = N - It0

    # Número de expuestos iniciales
    Et0 = 0

    # Número de recuperado iniciales
    Rt0 = 0

    St = St0
    It = It0
    Et = Et0
    Rt = Rt0
    dt = 1 / 1

    betat = beta
    k = [1000, 1000, 1000, 1000, 1000]
    days = data.shape[0]
    df_model = pd.DataFrame(np.zeros((days, 5)),
                            columns=['date', 'susceptibles', 'exposed', 'infectious', 'recovered'])
    npi_stage = 0
    for i, day in enumerate(data['date']):
        dS = -((betat * St * It) / N) * dt
        dE = ((betat * St * It) / N - (sigma * Et)) * dt
        dI = ((sigma * Et) - (gamma * It)) * dt
        dR = (gamma * It) * dt
        if npi_stage < len(npi_dates) and day >= npi_dates[npi_stage]:
            npi_stage += 1
            betat = beta * (1 - alphas[npi_stage]) * (1 - 0.05 * It / N) ** k[npi_stage]

        St += dS
        Et += dE
        It += dI
        Rt += dR
        df_model.iloc[i] = [day, St, Et, It, Rt]

    return df_model


def eval_error(r_df, m_df):
    error1, error2 = 0, 0
    for r_cases, r_deaths, r_recovered, m_cases, m_recovered in zip(r_df['cases'], r_df['deaths'], r_df['recovered'],
                                                                    m_df['infectious'], m_df['recovered']):
        error1 += abs(r_cases - m_cases)
        error2 += abs(r_deaths + r_recovered - m_recovered)

    return error1 + error2


start_infection_date = '2020-02-27'
social_distancing_date = '2020-03-09'
school_closure_date = '2020-03-13'
lockdown_date = '2020-03-14'
full_lockdown_date = '2020-03-30'
npi_dates = [social_distancing_date, school_closure_date, lockdown_date, full_lockdown_date]
npi_dict = {'social distancing': social_distancing_date,
            'school closure': school_closure_date,
            'lockdown': lockdown_date,
            'full lockdown': full_lockdown_date}
df_cv = pd.read_csv('cv_covid19.csv')
df_cv = df_cv.loc[df_cv['date'] >= start_infection_date]


def err_func(x):
    alpha1, alpha2, alpha3, alpha4, inf0, beta0, rect0 = x
    alphas = [0.0, alpha1, alpha2, alpha3, alpha4]
    df = run_model(df_cv, alphas=alphas, inf0=inf0, beta0=beta0, rect=rect0)
    return eval_error(df_cv, df)


############################################
#   Ajuste del modelo a los datos reales   #
############################################
# method='Nelder-Mead'  ->   6734     (no bounds)
# method='Powell'       ->   6261     (no bounds)
# method='CG'           ->  15073     (no bounds)
# method='BFGS'         ->   4651     (no bounds)
# method='L-BFGS-B'     ->  14650     (with bounds)
# method='TNC'          ->  14816     (with bounds)
# method='COBYLA'       ->  18659     (no bounds)
# method='SLSQP'        ->  10807     (with bounds)
# method='trust-constr' ->  11727     (with bounds)

method = 'BFGS'
result = minimize(fun=err_func, x0=np.array([0.2, 0.4, 0.8, 0.9, 10, 1.0, 25.0]), method=method,
                  bounds=[(0.0, 0.2), (0.2, 0.5), (0.5, 1.0), (0.5, 1.0), (1, 100), (0.5, 5), (15.0, 30.0)])
print(result)
_alphas = [0.0, result.x[0], result.x[1], result.x[2], result.x[3]]
_inf0 = result.x[4]
_beta0 = result.x[5]
_rect0 = result.x[6]
df_model_evolution = run_model(df_cv, alphas=_alphas, inf0=_inf0, beta0=_beta0, rect=_rect0)
print(eval_error(df_cv, df_model_evolution))
plot_seir(df_seir=df_model_evolution, df_data=df_cv, npi_data=npi_dict, zoom=[(0, 40), (0, 10000)],
          title=f'SEIR model and real data [fit method: {method}]')
