import numpy as np
import scipy.optimize
import math

# Find the intersection of three spheres
# P1,P2,P3 are the centers, r1,r2,r3 are the radii
# Implementaton based on Wikipedia Trilateration article.
def trilaterate(sph1, sph2, sph3):
    P1 = sph1[0:3]
    r1 = sph1[3]
    P2 = sph2[0:3]
    r2 = sph2[3]
    P3 = sph3[0:3]
    r3 = sph3[3]
    temp1 = P2 - P1
    e_x = temp1 / np.linalg.norm(temp1)
    temp2 = P3 - P1
    i = np.dot(e_x, temp2)
    temp3 = temp2 - i*e_x
    e_y = temp3 / np.linalg.norm(temp3)
    e_z = np.cross(e_x, e_y)
    d = np.linalg.norm(P2 - P1)
    j = np.dot(e_y, temp2)
    x = (r1*r1 - r2*r2 + d*d) / (2*d)
    y = (r1*r1 - r3*r3 -2*i*x + i*i + j*j) / (2*j)
    temp4 = r1*r1 - x*x - y*y
    if temp4<0:
        raise Exception("The three spheres do not intersect!")
    z = np.sqrt(temp4)
    p_12_a = P1 + x*e_x + y*e_y + z*e_z
    p_12_b = P1 + x*e_x + y*e_y - z*e_z
    return np.array([p_12_a, p_12_b])


def optimal_location(guess, spheres):

    def mse(x, spheres):
        mse = 0.0
        for sphere in spheres:
            dist_sqrd = np.sum(np.square(x - sphere[0:3]))
            mse += math.pow(dist_sqrd - sphere[3]**2, 2)
        return mse / spheres.shape[0]

    solution = scipy.optimize.minimize(
        mse,
        guess,
        args=(spheres,),
        method='L-BFGS-B',
        options={
            'ftol': 1e-5,
            'maxiter': 1e+7
        }
    )

    print(solution)

    return solution.x