import pickle
import plotly.graph_objects as go
from tqdm import tqdm 
import gif 

class ScalarFieldPlotter:
    def __init__(self, attrs) -> None:
        self.attrs = attrs
        self.scalarData = self.extractData()
        self.dates = list(self.scalarData.keys())

    def extractData(self):
        with open('scalarData.pkl', 'rb') as f:
            return pickle.load(f)
    
    def getContourPlotData(self, idx):
        plotData = {}
        for attr in self.attrs:
            lats = self.scalarData[self.dates[0]].LAT
            lons = self.scalarData[self.dates[0]].LON
            X = lats.unique().tolist()
            Y = lons.unique().tolist()
            data = self.scalarData[self.dates[idx]][attr].to_numpy()  
            data = data.reshape(len(X), len(Y)) 
            data[data <= -1.e34] = None
            data = data.tolist()
            plotData[attr] = data

        return X, Y, plotData

    def getColorPlotData(self, idx):
        plotData = {}
        for attr in self.attrs:
            lats = self.scalarData[self.dates[0]].LAT
            lons = self.scalarData[self.dates[0]].LON
            X = lats.tolist()
            Y = lons.tolist()
            data = self.scalarData[self.dates[idx]][attr].to_numpy()  
            data[data <= -1.e34] = None
            data = data.tolist()
            plotData[attr] = data

        return X, Y, plotData

    def getFrames(self, attr, limits):
        frames = []
        for idx in tqdm(range(len(self.dates[:10]))):
            X, Y, plotData = self.getContourPlotData(idx)
            frames.append(go.Frame(data = self.getContour(X, Y, plotData[attr], attr, limits), name = self.dates[idx],
            layout=go.Layout(title_text= attr + " Contour Plot on " + self.getDateString(idx))))
        return frames

    def getColorMap(self, X, Y, data, attr, limits):
        return go.Heatmap(
                    x = X, 
                    y = Y, 
                    z = data,
                    colorscale='Viridis',
                    colorbar=dict(
                        title = attr ,
                        titleside='bottom',
                        titlefont=dict(
                            size=16,
                            family='Arial, sans-serif')
                    ),
                    zmin = limits[0],
                    zmax = limits[1],
                    name = attr,                
                )

    def getContour(self, X, Y, data, attr, limits):
        return go.Contour(
                    x = Y,
                    y = X,
                    z = data,
                    colorscale='Viridis',
                    colorbar=dict(
                        title=attr,
                        titleside='bottom',
                        titlefont=dict(
                            size=16,
                            family='Arial, sans-serif')
                    ),
                    contours=dict(
                        start=limits[0],
                        end=limits[1],
                        size=limits[2],
                        showlines = False
                    ),
                    name = attr,  
                )

    def getDateString(self, idx):
        date = self.dates[idx]
        dmy = date.split("_")
        return dmy[1] + "-" + dmy[2] + "-" + dmy[3] 

    def ContourPlot(self, X, Y, data, attr, fig, limits):
        fig.add_trace(
            self.getContour(X, Y, data, attr, limits),
        )

    def ColorPlot(self, X, Y, data, attr, fig, limits):
        fig.add_trace(
            self.getColorMap(X, Y, data, attr, limits)
        )
        
    @gif.frame
    def getGifFrame(self, idx, attr, limits):
        X, Y, plotData = self.getContourPlotData(idx)

        fig = go.Figure()
        self.ContourPlot(X, Y, plotData[attr], attr, fig, limits)
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
        fig.update_layout(
            title_text= attr + " Contour Plot on " + self.getDateString(idx)
        )
        # fig.write_image("scalarfieldcontour/"+attr+"/"+self.getDateString(idx)+".jpg")
        return fig
    
    def getGifFrames(self, attr, limits):
        frames = []
        for i in tqdm(range(len(self.dates))[65:80]):
            frame = self.getGifFrame(i, attr, limits)
            frames.append(frame)
        return frames

