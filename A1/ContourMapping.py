import plotly.graph_objects as go
from dash import dash
from dash import dcc
from dash import html
from ScalarFieldPlotter import ScalarFieldPlotter

if __name__ == '__main__':
    sfp = ScalarFieldPlotter(['SSHA', 'SSS', 'SST'])
    idx = 73
    X, Y, plotData = sfp.getContourPlotData(idx)
    fig = go.Figure()
    sfp.ContourPlot(X, Y, plotData['SSS'], 'SSS', fig, [24,40,0.5])
    sfp.ContourPlot(X, Y, plotData['SSHA'], 'SSHA', fig, [-1,1,0.1])
    sfp.ContourPlot(X, Y, plotData['SST'], 'SST', fig, [18,35,1])

    fig.for_each_trace(
        lambda trace: trace.update(visible=False) if trace.name != 'SST' else (),
    )

    fig.update_layout(
        title_text= 'SST Contour Plot on ' + sfp.getDateString(idx)
    )

    fig.update_layout(
    autosize=False,
    width=1200,
    height=800,
    title_x = 0.5,
    # Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd.
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
                    args=[{'visible': [False, False, True]}, {'title' : 'SST Contour Plot on ' + sfp.getDateString(idx)}],
                    label='SST',
                    method='update'
                ),
                dict(
                    args=[{'visible': [True, False, False]}, {'title' : 'SSS Contour Plot on ' + sfp.getDateString(idx)}],
                    label='SSS',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, True, False]}, {'title' : 'SSHA Contour Plot on ' + sfp.getDateString(idx)}],
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

    fig.update_xaxes(
            tickangle = 90,
            title_text = 'Longitude',
    )
    fig.update_yaxes(
            title_text = 'Latitude',
    )

    app = dash.Dash()
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    app.run_server(debug=True)
