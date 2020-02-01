import math
import pandas as pd
from scipy import stats
from plotly.offline import plot
import plotly.graph_objs as go


def volcano_plot(file_path, a, b, gene):
    """ a is group a column names, and b is group b column names, gene is name
        of gene column. Returns the volcano plot as html in a div"""
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
    fig = go.Figure()
    print('create_graph')
    scatter = go.Scatter(x=result['log_fc'], y=result['log_pval'],
                         text=result.index,
                         mode='markers', name='test',
                         opacity=0.8, marker_color='green')
    fig.add_trace(scatter)
    fig.update_layout(
        title="Plot Title",
        xaxis_title="log2(Fold Change)",
        yaxis_title="-log(p-value)",
        font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"))
    print('create_plot')
    return plot(fig, output_type='div', include_plotlyjs=False,
                config={'displaylogo': False})
