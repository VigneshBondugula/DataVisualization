import pickle
import plotly.graph_objects as go
from tqdm import tqdm 
import plotly.figure_factory as ff
import numpy as np
import gif 

class VectorFieldPlotter:
    def __init__(self, attrs) -> None:
        self.attrs = attrs
        self.vectorData = self.extractData()
        self.dates = list(self.vectorData.keys())

    def extractData(self):
        with open('vectorData.pkl', 'rb') as f:
            return pickle.load(f)
    
    def getVectorPlotData(self, idx):
        lats = self.vectorData[self.dates[0]].LAT
        lons = self.vectorData[self.dates[0]].LON
        lats[lats <= -1.e34] = None
        lons[lons <= -1.e34] = None
        X = lats.tolist()
        Y = lons.tolist()
        U = self.vectorData[self.dates[idx]][self.attrs[0]].to_numpy()  
        V = self.vectorData[self.dates[idx]][self.attrs[1]].to_numpy() 
        U[U <= -1.e34] = None
        V[V <= -1.e34] = None
        return np.array(X), np.array(Y), U, V

    def getFrames(self):
        frames = []
        for idx in tqdm(range(len(self.dates[:10]))):
            X, Y, U, V = self.getVectorPlotData(idx)
            frames.append(go.Frame(data = self.VectorPlot(X, Y, U, V), name = self.dates[idx],
            layout=go.Layout(title_text = "Vector Plot on " + self.getDateString(self.dates[idx]))))
        return frames

    def getDateString(self, idx):
        date = self.dates[idx]
        dmy = date.split("_")
        return dmy[1] + "-" + dmy[2] + "-" + dmy[3] 

    def VectorPlot(self, X, Y, U, V, idx):
        fig = ff.create_quiver(Y, X, U, V,
                       scale=.25,
                       arrow_scale=.5,
                       name='quiver',
                       line_width=3,
                       line_color = "black")
        fig.update_layout(
           title_text= "Vector Plot on " + self.getDateString(idx)
        )
        return fig
    
    @gif.frame
    def getGifFrame(self, idx):
        X, Y, U, V = self.getVectorPlotData(idx)
        fig = self.VectorPlot(X, Y ,U, V, idx)
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
        # fig.write_image("vector/only/"+self.getDateString(idx)+".jpg")
        return fig
    
    def getGifFrames(self):
        frames = []
        for i in tqdm(range(len(self.dates))[::3]):
            frame = self.getGifFrame(i)
            frames.append(frame)
        return frames

