
import os
import re
import math
import pandas as pd

state_summaries = ['TX', 'WA', 'UT', 'AL', 'FL']

input_pattern = os.path.expanduser(
    '~/Dropbox (Rhodium Group)/Climate Impact Lab - RHG Internal/Website/' +
    'US Data/Impact data files/Temperature/{vartype}/{invar}')

state_input_pattern = os.path.expanduser(
    '~/Dropbox (Rhodium Group)/Climate Impact Lab - RHG Internal/Website/' +
    'US Data/Impact data files/Temperature/ACP Source Data/{regvar}')

variables = [
    (
        'Ave Annual',
        'tas_SMME_annual_{rcp}_ncdc_county_20-yr.csv',
        'Averages/Annual/Region/' +
            'tas_SMME_annual_{rcp}_ncdc_region_state_20yr_{wt}.tsv',
        '{reg}_annual-average-temp_degF_{rcp}.csv'),
    (
        'Ave Summer',
        'tas_SMME_JJA_{rcp}_ncdc_county_20yr_area.csv',
        'Averages/Summer/Region/' +
            'tas_SMME_JJA_{rcp}_ncdc_region_state_20yr_{wt}.tsv',
        '{reg}_seasonal-average-temp_JJA_degF_{rcp}.csv'),
    # (
    #     'Ave Temp Fall',
    #     'tas_SMME_CDF_SON_{rcp}_county_AREA.csv',
    #     '{reg}_seasonal-average-temp_SON_degF_{rcp}.csv'),
    # (
    #     'Ave Temp Spring',
    #     'tas_SMME_CDF_MAM_{rcp}_county_AREA.csv',
    #     '{reg}_seasonal-average-temp_MAM_degF_{rcp}.csv'),
    (
        'Ave Winter',
        'Winter Ave Temp - {rcp_upper}.xlsx',
        'Averages/Winter/Region/' +
            'tas_SMME_DJF_{rcp}_ncdc_region_state_20yr_{wt}.tsv',
        '{reg}_seasonal-average-temp_DJF_degF_{rcp}.csv'),
    (
        'Extreme cold days',
        'Cold days - {rcp_upper}.xlsx',
        'Exceedances/Percentiles/Tmin/Region/' +
            'tasmin_SMME_annual_region-state_lt32F_' +
            '{rcp}_exceedances_20yr_percentiles_{wt}.tsv',
        '{reg}_days-below-32F_day-counts_{rcp}.csv'),
    (
        'Extreme heat days',
        'Max Temp 95 - {rcp_upper}.xlsx',
        'Exceedances/Percentiles/Tmin/Region/' +
            'tasmax_SMME_annual_region-state_gt95F_' +
            '{rcp}_exceedances_20yr_percentiles_{wt}.tsv',
        '{reg}_days-above-95F_day-counts_{rcp}.csv'),
    # (
    #     'Humidity',
    #     'Humidity Cat II - {rcp_upper}.{ext}',
    #     '{reg}_humidity-cat-II_day-counts_{rcp}.csv'),
    # (
    #     'Humidity',
    #     'Humidity Cat III - {rcp_upper}.{ext}',
    #     '{reg}_humidity-cat-III_day-counts_{rcp}.csv')
    ]


for vartype, invar, regvar, outvar in variables:
    for rcp in ['rcp45', 'rcp85']:
        rcp_upper = re.sub(r'([0-9])([0-9])', r'\g<1>.\g<2>', rcp.upper())
        df = None

        fp = (input_pattern
                .format(vartype=vartype, invar=invar)
                .format(rcp=rcp, rcp_upper=rcp_upper))

        if fp.endswith('.xlsx'):
            df = pd.read_excel(fp, index_col=range(5))

        elif fp.endswith('.csv'):
            df = pd.read_csv(fp, index_col=range(5))

        elif fp.endswith('.tsv'):
            df = pd.read_csv(fp, index_col=range(5), sep='\t')

        else:
            raise ValueError('File type "{}" not recognized: {}'
                .format(os.path.splitext(fp)[1], fp))

        df.columns = pd.MultiIndex.from_tuples(
            [('1981-2010', 50)] +
            [(a, int(math.ceil(float(b))))
                for a, b in map(lambda x: x.split('_')[:2], df.columns[1:])],
            names=['Period', 'Quantile'])

        for state in state_summaries:
            outfile = (
                'csv3/us-state-summaries-v1.0/{outvar}'
                    .format(outvar=outvar)
                    .format(reg=state, rcp=rcp))

            if not os.path.isdir(os.path.dirname(outfile)):
                os.makedirs(os.path.dirname(outfile))

            dfs = (df[df.index.get_level_values('State') == state]
                        .reset_index(['Lat', 'Lon'], drop=True))

            dfs.stack('Period')[[5, 17, 50, 83, 95]].to_csv(outfile)
