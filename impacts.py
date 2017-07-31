import os
import re
import pandas as pd

impactpath_a = os.path.expanduser(
    '~/Dropbox (Rhodium Group)/Climate Impact Lab - RHG Internal/Website/' +
    'US Data/Impact data files/{var}/{subvar}-{rcp}-{year}b.csv')

impactpath_src = os.path.expanduser(
    '~/Dropbox (Rhodium Group)/ACP Team/Impacts Depot/{var}/' +
    '{agglev}_20a/{subvar}-{rcp}-{year}b.csv')

impactpath_srcy = os.path.expanduser(
    '~/Dropbox (Rhodium Group)/ACP Team/Impacts Depot/{var}/' +
    '{agglev}_20yr/{subvar}-{rcp}-{year}b.csv')

variables = [
    (impactpath_src, 'county', 'Agriculture', 'yields-total', 'Agricultural Yields', 'ag-yields-total', 'pct'),
    (impactpath_srcy, 'state', 'Agriculture', 'yields-total', 'Agricultural Yields', 'ag-yields-total', 'pct'),
    (impactpath_src, 'county', 'Mortality', 'health-mortality', 'Mortality', 'mortality-all', 'deathsper100k'),
    (impactpath_src, 'county', 'Mortality_Age', 'health-mortage-0-0', 'Mortality', 'mortality-0-0', 'deathsper100k'),
    (impactpath_src, 'county', 'Mortality_Age', 'health-mortage-1-44', 'Mortality', 'mortality-1-44', 'deathsper100k'),
    (impactpath_src, 'county', 'Mortality_Age', 'health-mortage-45-64', 'Mortality', 'mortality-45-64', 'deathsper100k'),
    (impactpath_src, 'county', 'Mortality_Age', 'health-mortage-65-inf', 'Mortality', 'mortality-65-inf', 'deathsper100k'),
    (impactpath_srcy, 'state', 'Mortality', 'health-mortality', 'Mortality', 'mortality-all', 'deathsper100k'),
    (impactpath_srcy, 'state', 'Mortality_Age', 'health-mortage-0-0', 'Mortality', 'mortality-0-0', 'deathsper100k'),
    (impactpath_srcy, 'state', 'Mortality_Age', 'health-mortage-1-44', 'Mortality', 'mortality-1-44', 'deathsper100k'),
    (impactpath_srcy, 'state', 'Mortality_Age', 'health-mortage-45-64', 'Mortality', 'mortality-45-64', 'deathsper100k'),
    (impactpath_srcy, 'state', 'Mortality_Age', 'health-mortage-65-inf', 'Mortality', 'mortality-65-inf', 'deathsper100k'),
    (impactpath_src, 'county', 'Labor', 'labor-low-productivity', 'Low-Risk Labor', 'labor-low', 'pct'),
    (impactpath_src, 'county', 'Labor', 'labor-high-productivity', 'High-Risk Labor', 'labor-high', 'pct'),
    (impactpath_src, 'county', 'Labor', 'labor-total-productivity', 'Total Labor', 'labor-total', 'pct'),
    (impactpath_srcy, 'state', 'Labor', 'labor-low-productivity', 'Low-Risk Labor', 'labor-low', 'pct'),
    (impactpath_srcy, 'state', 'Labor', 'labor-high-productivity', 'High-Risk Labor', 'labor-high', 'pct'),
    (impactpath_srcy, 'state', 'Labor', 'labor-total-productivity', 'Total Labor', 'labor-total', 'pct'),
    (impactpath_src, 'county', 'Crime', 'crime-property', 'Property Crime', 'crime-property', 'pct'),
    (impactpath_src, 'county', 'Crime', 'crime-violent', 'Violent Crime', 'crime-violent', 'pct'),
    (impactpath_srcy, 'state', 'Crime', 'crime-property', 'Property Crime', 'crime-property', 'pct'),
    (impactpath_srcy, 'state', 'Crime', 'crime-violent', 'Violent Crime', 'crime-violent', 'pct')]

variables_b = [
    # ('Energy Expenditures', 'Energy Expenditures', 'energy-expenditures-pct'),
    # ('Coastal Damage', 'Coastal Damage', 'coastal- gdpshare-pct'),
    # ('Total Direct Damages', 'Total Direct Damages', 'total-direct-gdpshare')
    ]


quantiles = [0.05, 0.5, 0.95]
periods = ['2020-2039', '2040-2059', '2080-2099']

for pattern, agglev, var, subvar, varname, machine, unit in variables:
    for period in periods:
        year = int(period.split('-')[0])
        for rcp in ['rcp26', 'rcp45', 'rcp85']:
            fp = pattern.format(agglev=agglev, var=var, subvar=subvar, rcp=rcp, year=year)
            
            df = pd.read_csv(fp, index_col=0)
            df.index.names = ['FIPS']
            df = df[['q{:0.2}'.format(q) for q in quantiles]]
            df.columns = quantiles
            df.sort_index(inplace=True)

            fp = ('csv/us-{}/{}_{}_{}_{}_percentiles.csv'
                                .format(agglev, machine, rcp, period, unit))

            if not os.path.isdir(os.path.dirname(fp)):
                os.makedirs(os.path.dirname(fp))

            df.to_csv(fp)

