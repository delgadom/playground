
import os
import pandas as pd

for f in os.listdir('csv-old'):

    fnew = 'global_hierid_' + f
    fnew = fnew.replace('tas_', 'tas-')
    fnew=fnew.replace('0_2', '0-2')
    fnew=fnew.replace('6_2', '6-2')
    fnew=fnew.replace('_19', '_rcp85_19')
    fnew=fnew.replace('_20', '_rcp85_20')
    fnew=fnew.replace('_tasmax_', '_tasmax-over-95F_')
    fnew=fnew.replace('_tasmin_', '_tasmin-under-32F_')

    old = pd.read_csv('csv-old/' + f, index_col=0)
    new = pd.read_csv('csv/' + fnew, index_col=0)

    diff = abs(old - new)
    notata = diff.loc[[i for i in diff.index if i != 'ATA']]
    if (notata > 0.2).any().any():
        print('XX {} {} {}\n\n{}\n'.format(
            f,
            notata.stack().where(notata.stack() > 0.1).count(),
            diff.loc['ATA'].max(),
            notata.stack()[[notata.stack().argmax()]]))

    else:
        print('OK {} {}'.format(f, diff.loc['ATA'].max()))

    new.loc[[i for i in new.index if i != 'ATA']].to_csv('csv/' + fnew)

