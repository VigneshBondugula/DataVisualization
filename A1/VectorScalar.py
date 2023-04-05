from VectorFieldPlotter import VectorFieldPlotter
from dash import dash
from dash import dcc
from dash import html
from ScalarFieldPlotter import ScalarFieldPlotter
import plotly.graph_objects as go

if __name__ == '__main__':
    sfp = ScalarFieldPlotter(['SSHA', 'SSS', 'SST'])
    X1, Y1, plotData = sfp.getContourPlotData(0)
    # X1, Y1, plotData = sfp.getColorPlotData(0)
    vfp = VectorFieldPlotter(["U", "V"])
    X, Y, U, V = vfp.getVectorPlotData(0)
    f = vfp.VectorPlot(X, Y ,U, V, 0)
    trace1 = f.data[0]
    fig = go.Figure()
    sfp.ContourPlot(X1, Y1, plotData['SSS'], "SSS", fig, [24,40,0.5])
    sfp.ContourPlot(X1, Y1, plotData['SSHA'], "SSHA", fig, [-1,1,0.1])
    sfp.ContourPlot(X1, Y1, plotData['SST'], "SST", fig, [18,35,1])
    # sfp.ColorPlot(Y1, X1, plotData['SSS'], "SSS", fig)
    # sfp.ColorPlot(Y1, X1, plotData['SSHA'], "SSHA", fig)
    # sfp.ColorPlot(Y1, X1, plotData['SST'], "SST", fig)
    fig.add_trace(trace1)
    fig.for_each_trace(
        lambda trace: trace.update(visible=False) if trace.name == "SSS" or  trace.name == "SSHA" else (),
    )
    fig.update_layout(
        title_text= "SST + Vector Plot on " + sfp.getDateString(0)
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
            type = "buttons",
            direction="right",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.12,
            yanchor="top"
        ),

        dict(
              buttons=list([
                dict(
                    args=[{"visible": [False, False, True, True]}, {"title" : "SST + Vector Plot on " + sfp.getDateString(0)}],
                    label="SST",
                    method="update"
                ),
                dict(
                    args=[{"visible": [True, False, False, True]}, {"title" : "SSS + Vector Plot on " + sfp.getDateString(0)}],
                    label="SSS",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False, True, False, True]}, {"title" : "SSHA + Vector Plot on " + sfp.getDateString(0)}],
                    label="SSHA",
                    method="update"
                ),
            ]),
            type = "buttons",
            direction="right",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.76,
            xanchor="left",
            y=1.12,
            yanchor="top"
        )
        ],
        annotations=[
        dict(text="Colorscale", x=0.02, xref="paper", y=1.09, yref="paper",
                             align="left", showarrow=False),
        dict(text="Variables", x=0.75, xref="paper", y=1.09, yref="paper",
                    align="left", showarrow=False),                
        ]
    )

    fig.update_xaxes(
            tickangle = 90,
            title_text = "Longitude",
    )
    fig.update_yaxes(
            title_text = "Latitude",
    )

    app = dash.Dash()
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    app.run_server(debug=True)
