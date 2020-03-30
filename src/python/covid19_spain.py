import pandas as pd
import src.python.datamanager as dm
from src.python.plot import plot_dataframe, plot_spain

# spain_covid19_url = 'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/nacional_covid19.csv'
spain_c19_casos_url = 'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_casos_long.csv'
spain_c19_muertes_url = 'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_fallecidos_long.csv'
spain_c19_uci_url = 'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_uci_long.csv'
spain_c19_altas_url = 'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_altas_long.csv'
spain_c19_hosp_url = 'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_hospitalizados_long.csv'
usa_c19_url = 'http://covidtracking.com/api/states/daily.csv'
world_pop_url = 'https://raw.githubusercontent.com/datasets/population/master/data/population.csv'
usa_states_pop = 'https://raw.githubusercontent.com/CivilServiceUSA/us-states/master/data/states.csv'
force_download = False


# df = pd.read_csv(spain_covid19_url)
df_spain_cases = dm.load_csv(spain_c19_casos_url, download=force_download)
df_spain_deceased = dm.load_csv(spain_c19_muertes_url, download=force_download)
df_spain_hospitalized = dm.load_csv(spain_c19_hosp_url, download=force_download)
df_spain_uci = dm.load_csv(spain_c19_uci_url, download=force_download)
df_usa = dm.load_csv(usa_c19_url, download=force_download)
df_states = dm.load_csv(usa_states_pop, download=force_download)
df_usa = df_usa.reindex(df_usa.columns.tolist() + ['r_positive', 'r_negative', 'r_deceased', 'r_total'], axis=1)
df_usa.drop(columns=['pending', 'hospitalized', 'hash', 'dateChecked', 'fips', 'deathIncrease', 'hospitalizedIncrease',
                     'negativeIncrease', 'positiveIncrease', 'totalTestResultsIncrease'], inplace=True)
df_usa.fillna(0, inplace=True)

########################
# SPAIN
########################
df_spain = df_spain_cases.copy()
df_spain.rename(columns={'total': 'cases', 'CCAA': 'region'}, inplace=True)
df_spain['deceased'] = 0
df_spain['hospitalized'] = 0
df_spain['uci'] = 0
df_spain['r_cases'] = 0
df_spain['r_deceased'] = 0
df_spain['r_hospitalized'] = 0
df_spain['r_uci'] = 0
print(df_spain_deceased.columns)
# 'fecha', 'cod_ine', 'CCAA', 'total'], dtype='object'
for i, row in df_spain_deceased.iterrows():
    date = row['fecha']
    cod_ine = row['cod_ine']
    deceased = row['total']
    pop = dm.d_ccaa_cod_population[cod_ine]
    mask = (df_spain['fecha'] == date) & (df_spain['cod_ine'] == cod_ine)
    cases = df_spain.loc[mask, 'cases'].iloc[0]
    df_spain.loc[mask, 'deceased'] = deceased
    df_spain.loc[mask, 'r_cases'] = 1e5 * cases / pop
    df_spain.loc[mask, 'r_deceased'] = 1e5 * deceased / pop

for i, row in df_spain_hospitalized.iterrows():
    date = row['fecha']
    cod_ine = row['cod_ine']
    hospitalized = row['total']
    pop = dm.d_ccaa_cod_population[cod_ine]
    mask = (df_spain['fecha'] == date) & (df_spain['cod_ine'] == cod_ine)
    df_spain.loc[mask, 'hospitalized'] = hospitalized
    df_spain.loc[mask, 'r_hospitalized'] = 1e5 * hospitalized / pop

for i, row in df_spain_uci.iterrows():
    date = row['fecha']
    cod_ine = row['cod_ine']
    uci = row['total']
    pop = dm.d_ccaa_cod_population[cod_ine]
    mask = (df_spain['fecha'] == date) & (df_spain['cod_ine'] == cod_ine)
    df_spain.loc[mask, 'uci'] = uci
    df_spain.loc[mask, 'r_uci'] = 1e5 * uci / pop

df_spain['fecha'] = df_spain['fecha'].apply(lambda x: x[5:])
# plot_dataframe(df_spain, x='fecha', y='r_cases', category='region', title='casos cada 100mil habitantes')
# plot_dataframe(df_spain, x='fecha', y='cases', category='region', title='casos totales')
plot_spain(df_spain, x='fecha', features=['r_cases', 'r_deceased', 'r_hospitalized', 'r_uci'], title='casos cada 100mil habitantes')

exit()
########################
# USA
########################
# store population for each state
for state_code in pd.unique(df_states['code']):
    state_pop = df_states.loc[df_states['code'] == state_code, 'population'].iloc[0]
    df_usa.loc[df_usa['state'] == state_code, 'r_positive'] = 1e5 * df_usa.loc[df_usa['state'] == state_code, 'positive'] / state_pop
    df_usa.loc[df_usa['state'] == state_code, 'r_deceased'] = 1e5 * df_usa.loc[df_usa['state'] == state_code, 'death'] / state_pop
    df_usa.loc[df_usa['state'] == state_code, 'r_total'] = 1e5 * df_usa.loc[df_usa['state'] == state_code, 'total'] / state_pop
df_usa.rename(columns={'state': 'region', 'death': 'deceased'}, inplace=True)

plot_dataframe(df_usa, x='date', y='r_positive', category='region')
