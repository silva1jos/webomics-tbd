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


def volcano_plot(exp_calc):
    """ exp_calc is a tsv containing fold chang and pvalues.
        Returns the volcano plot as html in a div"""
    result = pd.read_csv(exp_calc.file_path, sep='\t', index_col=0)
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
