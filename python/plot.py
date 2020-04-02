import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np


def plot_dataframe(data, x, y, category, title='confirmed cases by region'):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10), dpi=200)
    sns.lineplot(x=x,
                 y=y,
                 hue=category,
                 data=data
                 ).set_title(title)

    plt.legend(ncol=4)
    plt.xticks(rotation=90)
    plt.show()
    # for region in regions:
    #     region_data = data.loc[data['region'] == region]
    #     pass


def plot_spain(data, x, features, title='confirmed cases by region'):
    fig, axes = plt.subplots(5, 4, figsize=(20, 25), dpi=200)
    axes = [axes[i, j] for i in range(5) for j in range(4)]
    y_max = 0
    for feature in features:
        y_max = max(y_max, int(np.max(data[feature]) * 1.1))

    for i, region in enumerate(pd.unique(data['region'])):
        ax = axes[i]
        ax.xaxis.set_tick_params(rotation=90, labelsize=8)
        ax.set_ylim(ymin=0, ymax=y_max)
        x_values = data.loc[data['region'] == region, x]
        for feature in features:
            y_values = data.loc[data['region'] == region, feature]
            ax.plot(x_values, y_values)
        ax.set_title(region)

    plt.suptitle(title)
    plt.show()


def plot_seir(data, features, title):
    fig, ax = plt.subplots(1, 1, figsize=(10, 5), dpi=200)
    for feature in features:
        ax.plot(data[feature], label=feature)
    plt.legend()
    plt.suptitle(title)
    plt.show()