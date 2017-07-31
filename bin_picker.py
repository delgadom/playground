import os
import json
import pandas as pd
import numpy as np

pers = ['1986-2005', '2020-2039', '2040-2059', '2080-2099']
variables = [
    ('tas-annual', 'degF'),
    ('tas-DJF', 'degF'),
    ('tas-DJF', 'degF'),
    ('tas-MAM', 'degF'),
    ('tas-JJA', 'degF'),
    ('tas-SON', 'degF'),
    ('tasmax-over-95F', 'days-over-95F'),
    ('tasmin-under-32F', 'days-under-32F')]

relatives = [
    ('absolute', '1986-2005'),
    ('change-from-hist', '2080-2099')]

scenarios = ['rcp45', 'rcp85']

def get_data(var, rel, unit):
  return pd.concat([
    pd.concat([
        pd.read_csv(
            'csv/global_hierid_{var}_{rcp}_{per}_{rel}_{unit}_percentiles.csv'
              .format(var=var, rcp=rcp, per=per, rel=rel, unit=unit),
            index_col=0)
          for per in pers], axis=1, keys=pd.Index(pers, name='period'), names=['period', 'quantile'])
    for rcp in scenarios], axis=1, keys=pd.Index(scenarios, name='rcp'), names=['rcp', 'period', 'quantile'])

def create_range(var, rel, df, base_period):
    middle = df.stack(['quantile', 'rcp'])[base_period].median()
    bottom, top = df.stack(['rcp', 'period'])['0.5'].quantile([0.05, 0.95])

    print(var, rel, bottom, middle, top)

    # round middle with precision 10
    rmiddle = np.around(middle, -1)
    
    # take floor/ceiling of bottom/top with precision 10
    rbottom = np.around(bottom - 5, -1)
    rtop = np.around(top + 5, -1)

    span = max(rtop - rmiddle, rmiddle - rbottom)

    if bottom == 0:
        lbound = 0
        ubound = rtop

    elif top == 0:
        lbound = rbottom
        ubound = 0

    else:
        lbound = rmiddle - span
        ubound = rmiddle + span

    step = 5

    bins = np.arange(lbound, ubound + step, step)

    while len(bins) > 14:
        step += 5
        bins = np.arange(lbound, ubound + step, step)

    while len(bins) < 9:
        step = int(np.floor(step/2))
        bins = np.arange(lbound, ubound + step, step)

    return bins


def get_bin_ranges():
    for var, unit in variables:
        for rel, base_period in relatives:
            yield (
                '{}_{}'.format(var, rel),
                create_range(var, rel, get_data(var, rel, unit), base_period))


def set_bin_ranges():
    for varrel, bins in get_bin_ranges():
        fp = 'color_palettes/{}.json'.format(varrel)
        with open(fp, 'r') as f:
            palette = json.loads(f.read())

        palette['bins'] = list(map(int, bins))

        with open(fp, 'w+') as f:
            f.write(json.dumps(palette))


if __name__ == '__main__':
    set_bin_ranges()
