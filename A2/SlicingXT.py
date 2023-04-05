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
    
    vals = np.zeros((len(longitudes),len(dates)),np.float)

    lat = latitudes[0]
    depth = depths[4]
    
    for idx in tqdm(range(len(dates))):
        X, Y, Z, plotData = sfp.getXTPlotData(idx, lat, depth)
        for long, data in enumerate(plotData['SALT']):
            vals[long][idx] = data
    
    plt.contourf(dates, longitudes, vals, cmap="viridis")
    plt.xticks(rotation = 90) 
    plt.title("Variation of Salinity along longitude at latitude = {} and depth = {}m with time".format(str(lat), str(depth)))
    plt.xlabel("Date-Time")
    plt.ylabel("Longitude")
    cbar = plt.colorbar()
    cbar.set_label("Salinity")
    plt.show()