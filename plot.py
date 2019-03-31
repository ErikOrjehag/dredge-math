
import numpy as np

def sphere(ax, c, x, y, z, r):
    u = np.linspace(0, 2 * np.pi, 20)
    v = np.linspace(0, np.pi, 20)
    xx = x + r * np.outer(np.cos(u), np.sin(v))
    yy = y + r * np.outer(np.sin(u), np.sin(v))
    zz = z + r * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_wireframe(xx, yy, zz, color=c)

