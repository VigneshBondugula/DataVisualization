from VectorFieldPlotter import VectorFieldPlotter

import numpy as np
import matplotlib.animation as anim
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Agg")
from tqdm import tqdm

if __name__ == '__main__':

    FFMpegWriter = anim.writers['ffmpeg']
    metadata = dict(title='Streamlines', artist='Vignesh',comment='Animation')
    writer = FFMpegWriter(fps=2, metadata=metadata)

    vfp = VectorFieldPlotter(["U", "V"])
    idx = 0
    depths = range(5, 235, 10)

    fig = plt.figure(figsize=(16,8))
    with writer.saving(fig, "streamlinesDepth.mp4", dpi=100):
        for depth in tqdm(depths):
            lats, lons, U, V = vfp.getVectorPlotData(idx, depth)
            vfp.getFrame(lons, lats, U, V, idx, depth)
            writer.grab_frame()
            