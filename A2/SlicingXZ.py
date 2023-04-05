from ScalarFieldPlotter import ScalarFieldPlotter
import plotly.graph_objects as go
import numpy as np
if __name__ == '__main__':
    sfp = ScalarFieldPlotter(['TEMP', 'SALT'])
    idx = 0
    latitudes = sfp.getLatitudes()
    limits = sfp.getLimits(idx)
    frames=[]
    for lat in latitudes:
        X, Y, Z, plotData = sfp.getXZPlotData(idx,lat)
        frame = go.Frame(
            data = go.Surface(
            x = X.unique(),
            y = Z.unique(),
            z = lat * np.ones((len(Z.unique()), len(X.unique()))),
            surfacecolor=plotData['TEMP'].reshape(len(Z.unique()), len(X.unique())),
            cmin=limits['TEMP'][0], cmax=limits['TEMP'][1],
            colorbar_title="Potential Temperature (degree Celcius)",
            colorscale='Hot',
            colorbar=dict(thickness=20, ticklen=4),
            ),
            name=str(lat)
        )
        frames.append(frame)

    fig = go.Figure(frames=frames)

    X, Y, Z, plotData = sfp.getXZPlotData(idx, latitudes[0])
    print((len(X.unique()), len(Z.unique())))
    fig.add_trace(go.Surface(
        x = X.unique(),
        y = Z.unique(),
        z = latitudes[0] * np.ones((len(Z.unique()), len(X.unique()))),
        surfacecolor=plotData['TEMP'].reshape((len(Z.unique()), len(X.unique()))),
        cmin=limits['TEMP'][0], cmax=limits['TEMP'][1],
        colorbar_title="Potential Temperature (degree Celcius)",
        colorscale='Hot',
        colorbar=dict(thickness=20, ticklen=4)
    ))


    def frame_args(duration):
        return {
                "frame": {"duration": duration},
                "mode": "immediate",
                "fromcurrent": True,
                "transition": {"duration": duration, "easing": "linear"},
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
                        prefix='Latitude: ', 
                        visible=True, 
                        xanchor= 'center'
                        ), 
                }
            ]

    # Layout
    fig.update_layout(
            title='Potential Temperature with variation in Latitude (z-direction) on '+ sfp.getDateString(idx),
            width=1200,
            height=800,
            scene=dict(
                        zaxis=dict(range = [latitudes[0], latitudes[-1]],autorange=False,title='Latitude'),
                        xaxis = dict(title='Longitude'),
                        yaxis = dict(title='Depth'),
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
    