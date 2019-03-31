
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import plot
import calc

noise = np.random.normal(0, 1, (3, 3))
noise[:,-1] = 0

anchor = np.array([0, 0, -2])
p = np.array([
    np.array([100, 100, 0]),
    np.array([20, 80, 0]),
    np.array([80, 20, 0])
])

sph = [np.array([*(p[i] + noise[i]), np.linalg.norm(p[i]-anchor)]) for i in range(len(p))]

print(sph)

a = np.array(calc.trilaterate(sph[0], sph[1], sph[2]))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for s in sph:
    plot.sphere(ax, 'gray', *s)

print(a)

ax.scatter(a[:,0], a[:,1], a[:,2], c='r', alpha=1.0)

plt.show()
