from ScalarFieldPlotter import ScalarFieldPlotter
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
if __name__ == '__main__':
    sfp = ScalarFieldPlotter(['TEMP', 'SALT'])
    depths = range(5, 235, 10)
    latitudes = sfp.getLatitudes()
    longitudes = sfp.getLongitudes()
    dates = sfp.getDates()
    
    vals = np.zeros((len(latitudes),len(dates)),np.float)

    lon = longitudes[60]
    depth = depths[4]
    
    for idx in tqdm(range(len(dates))):
        X, Y, Z, plotData = sfp.getYTPlotData(idx, lon, depth)
        for lat, data in enumerate(plotData['SALT']):
            vals[lat][idx] = data
    
    plt.contourf(dates, latitudes, vals, cmap="viridis")
    plt.xticks(rotation = 90) 
    plt.title("Variation of Salinity along latitude at longitude = {} and depth = {}m with time".format(str(lon), str(depth)))
    plt.xlabel("Date-Time")
    plt.ylabel("Latitude")
    cbar = plt.colorbar()
    cbar.set_label("Salinity")
    plt.show()