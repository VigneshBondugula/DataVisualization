import plotly.graph_objects as go
from dash import dash
from dash import dcc
from dash import html
from ScalarFieldPlotter import ScalarFieldPlotter

if __name__ == '__main__':
    sfp = ScalarFieldPlotter(["SST", "SSS", "SSHA"])
    X, Y, plotData = sfp.getContourPlotData(0)
    frames = sfp.getFrames("SST", [15, 36, 1])
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": frames
    }

    # fill in most of layout
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 50, "redraw": True},
                                    "fromcurrent": True, "transition": {"duration": 0,
                                                                        "easing": "quadratic-in-out"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 10},
            "showactive": False,
            "type": "buttons",
            "x": 0.8,
            "y": 1.12,
            "xanchor" : "left",
            "yanchor" : "top"
        }
    ]

    fig_dict["data"].append(sfp.getContour(X, Y, plotData["SST"], "SST", [15,36,1]))

    fig = go.Figure(fig_dict)
    fig.update_layout(
        autosize=False,
        width=1200,
        height=800,
        title_x = 0.5,
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
