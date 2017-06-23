
import os
import shutil
import itertools

read_path = 'csv3/global-csvs-v2.3/{agglev}/global_{transformation}_{rcp}_{period}_{relative}_{unit}_{qty}.csv'
write_path = 'csv/global_{agglev}_{variable}_{rcp}_{period}_{relative}_{unit}_{qty}.csv'

variables = [
    {'transformation': 'tasmax-over-95F', 'variable': 'tasmax-over-95F', 'unit': 'days-over-95F'},
    {'transformation': 'tasmax-over-118F', 'variable': 'tasmax-over-118F', 'unit': 'days-over-118F'},
    {'transformation': 'tasmin-under-32F', 'variable': 'tasmin-under-32F', 'unit': 'days-under-32F'},
    {'transformation': 'tas-seasonal_DJF', 'variable': 'tas-DJF', 'unit': 'degF'},
    {'transformation': 'tas-seasonal_MAM', 'variable': 'tas-MAM', 'unit': 'degF'},
    {'transformation': 'tas-seasonal_JJA', 'variable': 'tas-JJA', 'unit': 'degF'},
    {'transformation': 'tas-seasonal_SON', 'variable': 'tas-SON', 'unit': 'degF'},
    {'transformation': 'tas-annual', 'variable': 'tas-annual', 'unit': 'degF'}
]

agglevs = [
    {'agglev': 'hierid', 'qty': 'percentiles'},
    # {'agglev': 'ISO', 'qty': 'percentiles-national'}
]


rcps = ['rcp45', 'rcp85']
periods = ['1986-2005', '2020-2039', '2040-2059', '2080-2099']
relatives = ['absolute', 'change-from-hist']

things = [variables, agglevs, rcps, periods, relatives]
thing_names = ['variable', 'agglev', 'rcp', 'period', 'relative']

for args in itertools.product(*things):
    varspec, aggspec, others = args[0], args[1], args[2:]
    spec = {}
    spec.update(varspec)
    spec.update(aggspec)
    spec.update(dict(zip(thing_names[2:], others)))

    src = read_path.format(**spec)
    dst = write_path.format(**spec)
    if not os.path.exists(src):
        print(src)
    shutil.copyfile(src, dst)
