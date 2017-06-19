import os
import json
import pandas as pd
import numpy as np

pers = ['1986_2005', '2020_2039', '2040_2059', '2080_2099']
variables = [
    ('tas_DJF', 'degF'),
    ('tas_MAM', 'degF'),
    ('tas_JJA', 'degF'),
    ('tas_SON', 'degF'),
    ('tasmax', 'days-over-95F'),
    ('tasmin', 'days-under-32F')]

relatives = [
    ('absolute', '1986_2005'),
    ('change-from-hist', '2080_2099')]

def get_data(var, rel, unit):
  return pd.concat([
    pd.read_csv(
        'csv/{var}_{per}_{rel}_{unit}_percentiles.csv'
          .format(var=var, per=per, rel=rel, unit=unit),
        index_col=0)
      for per in pers], axis=1, keys=pd.Index(pers, name='period'), names=['period', 'quantile'])

def create_range(var, rel, df, base_period):
    middle = df.stack('quantile')[base_period].median()
    bottom, top = df.stack('quantile').stack('period').quantile([0.02, 0.98])

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
