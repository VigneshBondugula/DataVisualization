import pickle
import plotly.graph_objects as go
import numpy as np

class ScalarFieldPlotter:
    def __init__(self, attrs) -> None:
        self.attrs = attrs
        self.scalarData = self.extractData()
        self.dates = list(self.scalarData.keys())

    def extractData(self):
        with open('scalarData.pkl', 'rb') as f:
            return pickle.load(f)
    
    def getPlotData(self, idx, dep_range):
        plotData = {}
        limits = {}
        df = self.scalarData[self.dates[idx]]
        updated_df = df[df['DEP'] >= dep_range[0]]
        updated_df = updated_df[updated_df['DEP'] <= dep_range[1]]
        X = updated_df.LON
        Y = updated_df.LAT
        Z = updated_df.DEP
        for attr in self.attrs:
            data = updated_df[attr]
            data[data <= -1.e34] = np.nan
            data = data.tolist()
            plotData[attr] = data
            limits[attr] = [np.nanmin(data), np.nanmax(data)]
        
        return X, Y, Z, plotData, limits
    
    def getXYPlotData(self, idx, dep):
        plotData = {}
        df = self.scalarData[self.dates[idx]]
        updated_df = df[df['DEP'] == dep]
        X = updated_df.LON
        Y = updated_df.LAT
        Z = updated_df.DEP
        # print(updated_df)
        for attr in self.attrs:
            data = updated_df[attr].to_numpy()  
            data[data <= -1.e34] = None
            plotData[attr] = data
        
        return X, Y, Z, plotData

    def getXZPlotData(self, idx, lat):
        plotData = {}
        df = self.scalarData[self.dates[idx]]
        updated_df = df[df['LAT'] == lat]
        X = updated_df.LON
        Y = updated_df.LAT
        Z = updated_df.DEP
        # print(updated_df)
        for attr in self.attrs:
            data = updated_df[attr].to_numpy()  
            data[data <= -1.e34] = None
            plotData[attr] = data
        
        return X, Y, Z, plotData

    def getYZPlotData(self, idx, lon):
        plotData = {}
        df = self.scalarData[self.dates[idx]]
        updated_df = df[df['LON'] == lon]
        X = updated_df.LON
        Y = updated_df.LAT
        Z = updated_df.DEP
        # print(updated_df)
        for attr in self.attrs:
            data = updated_df[attr].to_numpy()  
            data[data <= -1.e34] = None
            plotData[attr] = data
        
        return X, Y, Z, plotData

    def getXTPlotData(self, idx, lat, depth):
        plotData = {}
        df = self.scalarData[self.dates[idx]]
        updated_df = df[df['LAT'] == lat]
        updated_df = updated_df[updated_df['DEP'] == depth]
        X = updated_df.LON
        Y = updated_df.LAT
        Z = updated_df.DEP
        # print(updated_df)
        for attr in self.attrs:
            data = updated_df[attr].to_numpy()  
            data[data <= -1.e34] = None
            plotData[attr] = data
        
        return X, Y, Z, plotData
    
    def getYTPlotData(self, idx, lon, depth):
        plotData = {}
        df = self.scalarData[self.dates[idx]]
        updated_df = df[df['LON'] == lon]
        updated_df = updated_df[updated_df['DEP'] == depth]
        X = updated_df.LON
        Y = updated_df.LAT
        Z = updated_df.DEP
        # print(updated_df)
        for attr in self.attrs:
            data = updated_df[attr].to_numpy()  
            data[data <= -1.e34] = None
            plotData[attr] = data
        
        return X, Y, Z, plotData

    def getZTPlotData(self, idx, lon, lat):
        plotData = {}
        df = self.scalarData[self.dates[idx]]
        updated_df = df[df['LON'] == lon]
        updated_df = updated_df[updated_df['LAT'] == lat]
        X = updated_df.LON
        Y = updated_df.LAT
        Z = updated_df.DEP
        # print(updated_df)
        for attr in self.attrs:
            data = updated_df[attr].to_numpy()  
            data[data <= -1.e34] = None
            plotData[attr] = data
        
        return X, Y, Z, plotData

    def getLongitudes(self):
        return self.scalarData[self.dates[0]].LON.unique()

    def getLatitudes(self):
        return self.scalarData[self.dates[0]].LAT.unique()
    
    def getDates(self):
        return [self.getDateString(date) for date in range(len(self.dates))]

    def getIsosurface(self, X, Y, Z, data, limits, attr):
        return go.Isosurface(
                x=X,
                y=Y,
                z=Z,
                value=data,
                isomin=limits[0],
                isomax=limits[1],
                surface_count=5,
                colorscale="Hot",
                colorbar_title=attr,
                caps=dict(x_show=False,y_show=False,z_show=False),
            )

    def getDateString(self, idx):
        date = self.dates[idx]
        dmy = date.split("_")
        return dmy[1] + "-" + dmy[2] + "-" + dmy[3] 

    def IsoSurfacePlot(self, X, Y, Z, data, attr, limits, idx):
        fig= go.Figure(
            data=self.getIsosurface(X, Y, Z, data, limits, attr),
            layout=go.Layout(
                scene = dict(
                            xaxis = dict(title='Longitude'),
                            yaxis = dict(title='Latitude'),
                            zaxis = dict(title='Depth in meters'),
                        ),
                title = go.layout.Title(
                    text= attr + " with variation in Depth(in m) on " + self.getDateString(idx),
                )
            )
        )
        return fig
    
    def getLimits(self, idx):
        limits = {}
        df = self.scalarData[self.dates[idx]]
        for attr in self.attrs:
            data = df[attr].to_numpy()  
            data[data <= -1.e34] = np.nan
            limits[attr] = [np.nanmin(data), np.nanmax(data)]        
        return limits

        
