import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.interpolate import griddata
from mpl_toolkits.basemap import Basemap
class VectorFieldPlotter:
    def __init__(self, attrs) -> None:
        self.attrs = attrs
        self.vectorData = self.extractData()
        self.dates = list(self.vectorData.keys())

    def extractData(self):
        with open('vectorData.pkl', 'rb') as f:
            return pickle.load(f)
    
    def getVectorPlotData(self, idx, dep):
        df = self.vectorData[self.dates[idx]]
        updated_df = df[df['DEP'] == dep]
        lats = sorted(updated_df.LAT.unique())
        lons = sorted(updated_df.LON.unique())
        U = updated_df[self.attrs[0]].to_numpy()
        V = updated_df[self.attrs[1]].to_numpy()
        U[U <= -1.e34] = np.nan
        V[V <= -1.e34] = np.nan
        U = U.reshape(len(lats), len(lons))
        V = V.reshape(len(lats), len(lons))
        return updated_df.LAT, updated_df.LON, U, V

    def getDateString(self, idx):
        date = self.dates[idx]
        dmy = date.split("_")
        return dmy[1] + "-" + dmy[2] + "-" + dmy[3] 
    
    def getFrame(self, lons, lats, U, V, idx, dep):
        plt.clf()
        map = Basemap(projection = 'cyl', 
            llcrnrlon=min(lons),
            llcrnrlat=min(lats),
            urcrnrlon=max(lons),
            urcrnrlat=max(lats),
            lat_0=0,
            lon_0=min(lons))
    
        xmin = min(lons)
        ymin = min(lats)
        xmax = max(lons)
        ymax = max(lats)
        xi = np.linspace(xmin, xmax, 181)
        yi = np.linspace(ymin, ymax, 189)

        xi, yi = np.meshgrid(xi, yi)
        px = np.array(lons).flatten()
        py = np.array(lats).flatten()
        pu = np.array(U).flatten()
        pv = np.array(V).flatten()

        gu = griddata(np.array((px, py)).T, pu, (xi, yi))
        gv = griddata(np.array((px, py)).T, pv, (xi, yi))

        # _, _, x, y = map.makegrid(181, 189, returnxy = True)
        
        map.streamplot(
                xi,
                yi,
                gu,
                gv,
                density = 2,
        )

        map.drawcoastlines()   
        map.drawparallels(np.arange(-90., 90., 10.), labels=[1,0,0,0])
        map.drawmeridians(np.arange(-180., 180., 10.), labels=[0,0,0,1])

        plt.title("Currents (zonal and meridional) at depth = {} in Indian Ocean on {}".format(str(dep), self.getDateString(idx)))
        return map
        
    def getDates(self):
        return [self.getDateString(date) for date in range(len(self.dates))]
