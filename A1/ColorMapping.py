import plotly.graph_objects as go
from dash import dash
from dash import dcc
from dash import html
from ScalarFieldPlotter import ScalarFieldPlotter

if __name__ == '__main__':
    sfp = ScalarFieldPlotter(['SSHA', 'SSS', 'SST'])
    X, Y, plotData = sfp.getColorPlotData(0)
    fig = go.Figure()
    sfp.ColorPlot(Y, X, plotData['SSS'], 'SSS', fig, [18, 40])
    sfp.ColorPlot(Y, X, plotData['SSHA'], 'SSHA', fig, [-0.57, 0.45])
    sfp.ColorPlot(Y, X, plotData['SST'], 'SST', fig, [15,35])

    fig.for_each_trace(
        lambda trace: trace.update(visible=False) if trace.name != 'SST' else (),
    )

    fig.update_layout(
        title_text= 'SST ColorMap on ' + sfp.getDateString(0)
    )

    fig.update_layout(
    autosize=False,
    width=1200,
    height=800,
    title_x = 0.5,
    updatemenus=[
        dict(
            buttons=list([
               dict(
                    args=['colorscale', 'Viridis'],
                    label='Viridis',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'RdBu'],
                    label='RdBu',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'Hot'],
                    label='Hot',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'Bluered'],
                    label='Bluered',
                    method='restyle'
                ),
            ]),
            type = 'buttons',
            direction='right',
            pad={'r': 10, 't': 10},
            showactive=True,
            x=0.1,
            xanchor='left',
            y=1.12,
            yanchor='top'
        ),

        dict(
              buttons=list([
                dict(
                    args=[{'visible': [False, False, True]}, {'title' : 'SST ColorMap on ' + sfp.getDateString(0)}],
                    label='SST',
                    method='update'
                ),
                dict(
                    args=[{'visible': [True, False, False]}, {'title' : 'SSS ColorMap on ' + sfp.getDateString(0)}],
                    label='SSS',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, True, False]}, {'title' : 'SSHA ColorMap on ' + sfp.getDateString(0)}],
                    label='SSHA',
                    method='update'
                ),
            ]),
            type = 'buttons',
            direction='right',
            pad={'r': 10, 't': 10},
            showactive=True,
            x=0.76,
            xanchor='left',
            y=1.12,
            yanchor='top'
        )
        ],
        annotations=[
        dict(text='Colorscale', x=0.02, xref='paper', y=1.09, yref='paper',
                             align='left', showarrow=False),
        dict(text='Variables', x=0.75, xref='paper', y=1.09, yref='paper',
                    align='left', showarrow=False),                
        ]
    )

    app = dash.Dash()
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    app.run_server(debug=True)
