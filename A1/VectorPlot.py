from VectorFieldPlotter import VectorFieldPlotter
from dash import dash
from dash import dcc
from dash import html

if __name__ == "__main__":
    vfp = VectorFieldPlotter(["U", "V"])
    X, Y, U, V = vfp.getVectorPlotData(73)

    fig = vfp.VectorPlot(X, Y ,U, V, 73)
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