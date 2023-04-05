from ScalarFieldPlotter import ScalarFieldPlotter
import plotly.graph_objects as go
import numpy as np
if __name__ == '__main__':
    sfp = ScalarFieldPlotter(['TEMP', 'SALT'])
    idx = 0
    depths = range(5, 235, 10)
    limits = sfp.getLimits(idx)
    frames=[]
    for depth in depths:
        X, Y, Z, plotData = sfp.getXYPlotData(idx,depth)
        frame = go.Frame(
            data = go.Surface(
            x = X.unique(),
            y = Y.unique(),
            z = depth * np.ones((len(X.unique()), len(Y.unique()))),
            surfacecolor=plotData['TEMP'].reshape(len(Y.unique()), len(X.unique())),
            cmin=limits['TEMP'][0], cmax=limits['TEMP'][1],
            colorbar_title="Potential Temperature (degree Celcius)",
            colorscale="Hot",
            colorbar=dict(thickness=20, ticklen=4),
            ),
            name=str(depth)
        )
        frames.append(frame)

    fig = go.Figure(frames=frames)

    X, Y, Z, plotData = sfp.getXYPlotData(idx, 5)
    print((len(X.unique()), len(Y.unique())))
    fig.add_trace(go.Surface(
        x = X.unique(),
        y = Y.unique(),
        z = 5.0 * np.ones((len(X.unique()), len(Y.unique()))),
        surfacecolor=plotData['TEMP'].reshape((len(Y.unique()), len(X.unique()))),
        cmin=limits['TEMP'][0], cmax=limits['TEMP'][1],
        colorbar_title="Potential Temperature (degree Celcius)",
        colorscale="Hot",
        colorbar=dict(thickness=20, ticklen=4)
    ))


    def frame_args(duration):
        return {
                "frame": {"duration": duration, "redraw": True},
                "mode": "immediate",
                "fromcurrent": True,
                "transition": {"duration": duration, "easing": "cubic-in-out"},
            }

    sliders = [
                {
                    "pad": {"b": 10, "t": 60},
                    "len": 0.9,
                    "x": 0.1,
                    "y": 0,
                    "steps": [
                        {
                            "args": [[f.name], frame_args(0)],
                            "label": str(f.name),
                            "method": "animate",
                        }
                        for f in fig.frames
                    ],
                    "currentvalue":dict(font=dict(size=12), 
                        prefix='Depth: ', 
                        visible=True, 
                        xanchor= 'center'
                        ), 
                    "transition":dict(duration=0)
                }
            ]

    # Layout
    fig.update_layout(
            title='Potential Temperature with variation in depth in meters (z-direction) on '+ sfp.getDateString(idx),
            width=1200,
            height=800,
            scene=dict(
                        zaxis=dict(range=[5.0, 225.0],autorange=False,title='Depth in meters'),
                        xaxis = dict(title='Longitude'),
                        yaxis = dict(title='Latitude'),
                        aspectratio=dict(x=1.5, y=1, z=1),
                        ),
            updatemenus = [
                {
                    "buttons": [
                        {
                            "args": [None, frame_args(50)],
                            "label": "&#9654;", # play symbol
                            "method": "animate",
                        },
                        {
                            "args": [[None], frame_args(0)],
                            "label": "&#9724;", # pause symbol
                            "method": "animate",
                        },
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 70},
                    "type": "buttons",
                    "x": 0.1,
                    "y": 0,
                }
            ],
            sliders=sliders
    )

    fig.show()
    