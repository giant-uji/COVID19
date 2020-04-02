import os
import pandas as pd

data_path = os.path.join('..', 'data')

d_ccaa_name_population = {
    'Andalucía': 8414240,
    'Aragón': 1319291,
    'Principado de Asturias': 1022800,
    'Islas Baleares': 1149460,
    'Islas Canarias': 2153389,
    'Cantabria': 581078,
    'Castilla-La Mancha': 2032863,
    'Castilla y León': 2399548,
    'Cataluña': 7675217,
    'Comunidad Valenciana': 5003769,
    'Extremadura': 1067710,
    'Galicia': 2699499,
    'Comunidad de Madrid': 6663394,
    'Ceuta y Melilla': 171264,
    'Región de Murcia': 1493898,
    'Comunidad Foral de Navarra': 654214,
    'País Vasco': 2207776,
    'La Rioja': 316798
}

d_ccaa_cod_population = {
    0: 49248430,
    1: 8414240,
    2: 1319291,
    3: 1022800,
    4: 1149460,
    5: 2153389,
    6: 581078,
    8: 2032863,
    7: 2399548,
    9: 7675217,
    10: 5003769,
    11: 1067710,
    12: 2699499,
    13: 6663394,
    18: 84777,
    19: 86487,
    14: 1493898,
    15: 654214,
    16: 2207776,
    17: 316798
}


def load_csv(url, download=False):
    file_name = url.split('/')[-1]
    file_path = os.path.join(data_path, file_name)
    if os.path.exists(file_path) and not download:
        print(f'loading {file_path}')
        return pd.read_csv(file_path)
    else:
        print(f'downloading {file_name}')
        df = pd.read_csv(url)
        df.to_csv(file_path, index=False)
        return df
