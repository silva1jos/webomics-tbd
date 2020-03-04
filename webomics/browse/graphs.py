""" Functions to generate interactive plots for html implementation.
    Require the inclusion of plotly.js in html templates.
    """
import math
import pandas as pd
from scipy import stats
from plotly.offline import plot
import plotly.graph_objs as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def volcano_plot(file_path, a, b, gene):
    """ a is group a column names, and b is group b column names, gene is name
        of gene column. Returns the volcano plot as html in a div"""
    print(file_path, a, b, gene)
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
    scatter = go.Scattergl(x=result['log_fc'], y=result['log_pval'],
                           text=result.index,
                           mode='markers', name='test',
                           opacity=0.8, marker_color='green')
    fig.add_trace(scatter)
    fig.update_layout(
        title="Volcano Plot",
        xaxis_title="log2(Fold Change)",
        yaxis_title="-log(p-value)")
    print('create_plot')
    return plot(fig, output_type='div', include_plotlyjs=False,
                config={'displaylogo': False})


def pca_plot(file_path, groups=None, index_col=0):
    """ Plots a pca plot, where each data point is a sample.
        Takes in groups optionally, to color points by named groups.
        Groups is a list of groups ordered to match the samples in count_file.
        Takes a file path for gene counts file."""
    df = pd.read_csv(file_path, sep='\t', index_col=index_col).T
    df = pd.DataFrame(PCA(n_components=2)
                      .fit_transform(StandardScaler().fit_transform(df)),
                      columns=['principal component 1',
                               'principal component 2'],
                      index=df.index)
    fig = go.Figure()
    if groups is None:
        fig.add_trace(go.Scatter(x=df['principal component 1'],
                                 y=df['principal component 2'],
                                 text=df.index, mode='markers',
                                 name='test', opacity=0.8))
    else:
        df['group'] = groups
        for g in set(groups):
            subset = df[df['group'] == g]
            fig.add_trace(go.Scatter(x=subset['principal component 1'],
                                     y=subset['principal component 2'],
                                     text=subset.index, mode='markers',
                                     name=g, opacity=0.8))
    fig.update_layout(
        title="PCA Test",
        xaxis_title="principal component 1",
        yaxis_title="principal component 2",
        legend_orientation="h")
    return plot(fig, output_type='div', include_plotlyjs=False,
                config={'displaylogo': False})
