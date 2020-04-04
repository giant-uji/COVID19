import os
import pandas as pd
from datetime import datetime, timedelta

casos_url = 'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_casos_long.csv'
muertes_url = 'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_fallecidos_long.csv'
uci_url = 'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_uci_long.csv'
altas_url = 'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_altas_long.csv'
hosp_url = 'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_hospitalizados_long.csv'


if __name__ == '__main__':
    df_spain_cases = pd.read_csv(casos_url)
    df_spain_deceased = pd.read_csv(muertes_url)
    df_spain_icu = pd.read_csv(uci_url)
    df_spain_recovered = pd.read_csv(altas_url)
    df_spain_hospitalized = pd.read_csv(hosp_url)

    ########################
    # CV
    ########################
    df_cv = df_spain_cases.loc[df_spain_cases['cod_ine'] == 10]
    df_cv = df_cv.rename(columns={'total': 'cases', 'fecha': 'date'})
    df_cv = df_cv.drop(columns=['cod_ine', 'CCAA'])

    # adds data from 01-01 to 26-2, with num. cases = 0
    prev_dates = [str(datetime.strptime('2020-01-01', '%Y-%m-%d') + timedelta(days=d))[:10] for d in range(57)]
    df_prev_cv = pd.DataFrame(prev_dates, columns=['date'])
    df_prev_cv['cases'] = 0
    df_cv = pd.concat((df_prev_cv, df_cv))

    df_cv['deaths'] = 0
    df_cv['icu'] = 0
    df_cv['recovered'] = 0
    df_cv['hospitalized'] = 0

    def add_column(df1, df2, column):
        for i, row in df2.loc[df2['cod_ine'] == 10].iterrows():
            date = row['fecha']
            value = row['total']
            mask = df1['date'] == date
            df1.loc[mask, column] = value
        return df1

    df_cv = add_column(df_cv, df_spain_hospitalized, 'hospitalized')
    df_cv = add_column(df_cv, df_spain_icu, 'icu')
    df_cv = add_column(df_cv, df_spain_recovered, 'recovered')
    df_cv = add_column(df_cv, df_spain_deceased, 'deaths')

    df_cv.to_csv('cv_covid19.csv', index=False)
