import os
import re
import time
import shutil
import pandas as pd

states = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI',
    'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN',
    'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH',
    'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA',
    'WV', 'WI', 'WY']

periods = ['1981-2010', '2020-2039', '2040-2059', '2080-2099']

cols = [
    ('1981-2010', 'Normal', 0.05),
    ('1981-2010', 'Normal', 0.5),
    ('1981-2010', 'Normal', 0.95),
    ('2020-2039', '5th', 0.05),
    ('2020-2039', '50th', 0.5),
    ('2020-2039', '95th', 0.95),
    ('2040-2059', '5th', 0.05),
    ('2040-2059', '50th', 0.5),
    ('2040-2059', '95th', 0.95),
    ('2080-2099', '5th', 0.05),
    ('2080-2099', '50th', 0.5),
    ('2080-2099', '95th', 0.95)]

data_table_variables = [
    ('Temp - Summer Average', 'tas_JJA', 'degF'),
    ('Temp - Winter Average', 'tas_DJF', 'degF'),
    ('Temp - Max >95F', 'tasmax-over-95F', 'days-over-95F'),
    ('Temp - Min <32F', 'tasmin-under-32F', 'days-under-32F')]

csv_variables = [
    (
        'tas-annual',
        'degF',
        os.path.expanduser(
            '~/Dropbox (Rhodium Group)/Climate Impact Lab - RHG Internal/' +
            'Website/US Data/Impact data files/Temperature/ACP Source Data/' +
            'Averages/Annual/Region/' +
            'tas_SMME_annual_{rcp}_ncdc_region_state_20yr.csv'))]

rcps = [
    ('rcp85', 'RCP 8.5', 2),
    ('rcp60', 'RCP 6.0', 65),
    ('rcp45', 'RCP 4.5', 128),
    ('rcp26', 'RCP 2.6', 191)]

# if os.path.isdir('csv/us-state'):
#     shutil.rmtree('csv/us-state')

# os.makedirs('csv/us-state')


def export(df, var, unit, rcp):

    df = df[[(col[0], col[1]) for col in cols]]
    df.columns = pd.MultiIndex.from_tuples(
        [(col[0], col[2]) for col in cols],
        names=['period', 'quantile'])

    df = df.loc[states].astype(float)

    for period in periods:

        perdf = df.xs(period, level='period', axis=1)

        perdf.to_csv(
                'csv/us-state/{}_{}_{}_absolute_{}_percentiles-state.csv'
                    .format(var, rcp, period, unit))

        if period == '1981-2010':
            hist = perdf
        
        ((perdf-hist)
            .to_csv(
                'csv/us-state/{}_{}_{}_change-from-hist_{}_percentiles-state.csv'
                    .format(var, rcp, period, unit)))

def do_not_annual():
    for xvar, var, unit in data_table_variables:
        for rcp, RCP, skiprows in rcps:

            df = pd.read_excel(
                'csv/ACP Science data tables.xlsx', 
                sheetname=xvar,
                index_col=0,
                skiprows=skiprows,
                nrows=61,
                header=[0, 1])

            df = df.iloc[:61]

            assert df.index.names[0] == RCP
            df.index.names = ['state']

            export(df, var, unit, rcp)

def do_annual():
    for var, unit, path in csv_variables:
        for rcp in map(lambda x: x[0], rcps):
            
            df = pd.read_csv(path.format(rcp=rcp), index_col=0, skiprows=22)
            
            df.columns = pd.MultiIndex.from_tuples(
                [('1981-2010', 'Normal')] +
                [(x.split('_')[0], x.split('_')[1]+'th') for x in df.columns[1:]],
                names=['period', 'quantile'])

            df.index.names = ['state']

            export(df, var, unit, rcp)

if __name__ == '__main__':
    # do_not_annual()
    do_annual()