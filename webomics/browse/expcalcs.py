import os
import math
from datetime import datetime
import pandas as pd
from scipy import stats

from .models import ExperimentCalc, CalcOptions
from webomics.settings import MEDIA_ROOT


def volcano_calc(exp, a, b, gene):
    file_path = exp.file_path.path
    df_a = pd.read_csv(file_path, sep='\t', index_col=gene, usecols=a + [gene])
    df_b = pd.read_csv(file_path, sep='\t', index_col=gene, usecols=b + [gene])
    fold_change = df_b.mean(axis=1) / df_a.mean(axis=1)
    p_val = []
    print('before stat')
    for (_, m), (_, f) in zip(df_a.iterrows(), df_b.iterrows()):
        p_val.append(stats.ttest_ind(m, f)[1])
    p_val = pd.Series(p_val, index=df_a.index)
    print('exit stat')
    result = pd.DataFrame(index=df_a.index, data={'pval': p_val,
                                                  'fc': fold_change})
    result.dropna(inplace=True)
    # Drops any zero values
    result = result.loc[(result != 0).all(axis=1)]
    result['log_pval'] = result.pval.apply(lambda x: -math.log(x))
    result['log_fc'] = result.fc.apply(lambda x: math.log(x, 2))
    fp = os.path.join(os.path.join(MEDIA_ROOT, 'calcs/volcano'),
                      exp.exp_name
                      + datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    result.to_csv(fp, sep='\t')
    exp_calc = ExperimentCalc(calc_name='volcano', exp_ref=exp, file_path=fp)
    exp_calc.save()
    for sample in a:
        CalcOptions(calc=exp_calc, name='group_a', value=sample).save()
    for sample in b:
        CalcOptions(calc=exp_calc, name='group_b', value=sample).save()
    return exp_calc
