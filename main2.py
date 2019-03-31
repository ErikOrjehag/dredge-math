
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import plot
import calc

# The actual anchor position
anchor = np.array([0, 0, -10])

print("anchor", anchor)

# GPS locations we measure from
p = np.concatenate([
    np.array([(x*20, y*20, 0) for x in range(5)])
    for y in range(5)
])

print("actual positions", p)

# Add noise to GPS measurements
std = 3.0
noise = np.random.normal(0, std, p.shape)
noise[:,-1] = 0 # No noise in z-axis

print("noise", noise)

# Gather measurements in list of spheres [(x, y, z, r), ...]
spheres = np.array([
    [
        *(p[i] + noise[i]), # Position with noise
        np.linalg.norm(p[i] - anchor) # Distance
    ]
    for i in range(len(p))
])

# Only keep measurements further away
spheres = spheres[spheres[:,3] > 25]

print("measurements", spheres)

print("N", spheres.shape[0])

# Triangulate using 3 measurements and assume the anchor is under water
#guess = calc.trilaterate(spheres[0,:], spheres[1,:], spheres[2,:])
#guess = guess[0,:] if guess[0,2] < 0 else guess[1,:]
guess = spheres[np.argmin(spheres[:,3]),0:3] - np.array([0, 0, 1])

print("guess", guess)

solution = calc.optimal_location(guess, spheres)

print("solution", solution)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.axis('equal')

#for sphere in spheres:
#    plot.sphere(ax, 'gray', *sphere)

ax.scatter(spheres[:,0], spheres[:,1], spheres[:,2], c='black', alpha=1.0)
ax.scatter(anchor[0], anchor[1], anchor[2], c='g', alpha=1.0)
ax.scatter(guess[0], guess[1], guess[2], c='gray', alpha=1.0)
ax.scatter(solution[0], solution[1], solution[2], c='r', alpha=1.0)

plt.show()
