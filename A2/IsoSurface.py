from ScalarFieldPlotter import ScalarFieldPlotter
import plotly.graph_objects as go

if __name__ == '__main__':
    sfp = ScalarFieldPlotter(['TEMP', 'SALT'])
    idx = 0
    X, Y, Z, plotData, limits = sfp.getPlotData(idx, [5,50])
    fig = sfp.IsoSurfacePlot(X, Y, Z, plotData['TEMP'], 'Potential Temperature', limits['TEMP'], idx)

    fig.update_layout(title_x=0.5)
    fig.show()
