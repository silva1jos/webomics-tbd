import pandas as pd

from plotly.offline import plot
import plotly.graph_objs as go


def volcano_plot(fold_file):
    pd.read_csv(fold_file)
    fig = go.Figure()
    scatter = go.Scatter(x=[0, 1, 2, 3], y=[0, 1, 2, 3],
                         mode='markers', name='test',
                         opacity=0.8, marker_color='green')
    fig.add_trace(scatter)  # might not want
    plt_div = plot(fig, output_type='div', include_plotlyjs=False,
                   config={'displaylogo': False})
    return render(request, 'view/index.html', {'graph': plt_div})
