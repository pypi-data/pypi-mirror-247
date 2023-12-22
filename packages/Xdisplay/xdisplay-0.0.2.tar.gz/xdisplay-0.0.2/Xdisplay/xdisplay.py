from matplotlib import cm
from matplotlib.colors import LightSource
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import axes3d


class Xdisplay:
    def showSingleView3d(self, data, z_position=-1):
        assert len(data.shape) == 3

        z = data.sum(axis=z_position)
        ncols, nrows = z.shape
        x = np.linspace(0, 1, ncols)
        y = np.linspace(0, 1, nrows)
        x, y = np.meshgrid(x, y)

        region = np.s_[:, :]
        x, y, z = x[region], y[region], z[region]
        fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
        # To use a custom hillshading mode, override the built-in shading and pass in the rgb colors of the shaded surface calculated from "shade".
        rgb = LightSource(270, 45).shade(z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
        surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=rgb, linewidth=0, antialiased=False, shade=False)
        plt.show()