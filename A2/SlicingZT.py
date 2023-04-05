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
    
    vals = np.zeros((len(depths),len(dates)),np.float)

    lat = latitudes[5]
    lon = longitudes[5]
    
    for idx in tqdm(range(len(dates))):
        X, Y, Z, plotData = sfp.getZTPlotData(idx, lon, lat)
        for dep, data in enumerate(plotData['SALT']):
            vals[dep][idx] = data
    
    plt.contourf(dates, depths, vals, cmap="viridis")
    plt.xticks(rotation = 90) 
    plt.title("Variation of Salinity along depth at longitude = {} and latitude = {} with time".format(str(lon), str(lat)))
    plt.xlabel("Date-Time")
    plt.ylabel("Depth")
    cbar = plt.colorbar()
    cbar.set_label("Salinity")
    plt.show()