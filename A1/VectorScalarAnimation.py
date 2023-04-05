from VectorFieldPlotter import VectorFieldPlotter
from ScalarFieldPlotter import ScalarFieldPlotter
import plotly.graph_objects as go

import gif
from tqdm import tqdm
if __name__ == '__main__':
    vfp = VectorFieldPlotter(["U", "V"])
    sfp = ScalarFieldPlotter(['SSHA', 'SSS', 'SST'])

    @gif.frame
    def getVSFrame(attr, idx, range):
        X1, Y1, plotData = sfp.getContourPlotData(idx)
        # X1, Y1, plotData = sfp.getColorPlotData(idx)
        X, Y, U, V = vfp.getVectorPlotData(idx)
        f = vfp.VectorPlot(X, Y ,U, V, idx)
        trace1 = f.data[0]
        fig = go.Figure()
        sfp.ContourPlot(X1, Y1, plotData[attr], attr, fig, range)
        # sfp.ColorPlot(Y1, X1, plotData[attr], attr, fig)
        fig.add_trace(trace1)
        fig.update_layout(
            title_text= attr + " + Vector Plot on " + sfp.getDateString(idx)
        )
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
        # fig.write_image("vector/"+attr+"/"+sfp.getDateString(idx)+".jpg")
        return fig
    
    frames = []
    for i in tqdm(range(len(sfp.dates))[65:80]):
        # frame = getVSFrame("SST", i, [18,35,1])
        # frame = getVSFrame("SSS", i, [24,40,0.5])
        frame = getVSFrame("SSHA", i, [-0.5,0.4,0.01])

        frames.append(frame)
    gif.save(frames, 'VectorContourAnimationSSHA.gif', duration=1000, between="frames")

