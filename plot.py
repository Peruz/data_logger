import argparse
import pandas as pd
from dateutil import parser, rrule
from datetime import datetime, time, date, timedelta
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates



def get_fname(fname=None):
    """get file name from command line if none"""
    if fname is None:
        parse = argparse.ArgumentParser()
        parse.add_argument('-fname', type=str, help='name of file to read', nargs='?')
        args = parse.parse_args()
        fname = args.fname
    if fname is None:
        raise SystemExit('Provide a file name, from script or cmd-line')
    return(fname)

def read_fname(fname):
    df = pd.read_csv(fname, skiprows=0, header=[0, 1, 2], delim_whitespace=False)
    df['Timestap'] = pd.to_datetime(df.iloc[:, 0])
    df = df.set_index('Timestap')
    df = df.resample('5min').mean()
    rename_dict = {' m³/m³ Water Content': 'water_vol',
                            ' °C Soil Temperature': 'temp_C',
                            ' mS/cm Saturation Extract EC': 'saturation',
                            ' kPa Matric Potential': 'pot'}
    df = df.rename(columns=rename_dict)
    return(df)

def plot_datetime(df, output_name):
    fig = plt.figure()
    ax = plt.gca()
    for i,c in enumerate(df.columns):
        ax.plot_date(df.index, df[c], '-', linewidth=4, label=c)
    locator = matplotlib.dates.AutoDateLocator(minticks=5, maxticks=20)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    fig.autofmt_xdate()
    ax.legend()
    ax.grid()
    plt.tight_layout()
    plt.savefig(output_name, dpi=600)
    plt.show()


if __name__ == '__main__':
    fname = get_fname()
    data = read_fname(fname)

    columns = data.columns.get_level_values(level=2)
    if 'water_vol' in columns:
        data_water = data.loc[:, (slice(None), slice(None), 'water_vol')]
        plot_datetime(data_water, 'water.png')
    if 'temp_C' in columns:
        data_temp = data.loc[:, (slice(None), slice(None), 'temp_C')]
        plot_datetime(data_temp, 'temp.png')
    if 'saturation' in columns:
        data_saturation = data.loc[:, (slice(None), slice(None), 'saturation')]
        plot_datetime(data_saturation, 'saturation.png')
    if 'pot' in columns:
        data_pot = data.loc[:, (slice(None), slice(None), 'pot')]
        plot_datetime(data_pot, 'pot.png')
