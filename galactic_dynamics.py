import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants
G = 4.30091e-6  # Gravitational constant in (kpc / Msun) * (km/s)^2
M = 1.0e12  # Mass of the galaxy in solar masses
b = 5.0  # Softening parameter (scale radius) in kpc

# Plummer potential
def plummer_potential(r, M, b):
    return -G * M / np.sqrt(r**2 + b**2)

# Gradient of the potential (force) in Cartesian coordinates
def force_plummer(x, y, z, M, b):
    r = np.sqrt(x**2 + y**2 + z**2)
    force_mag = G * M / (r**2 + b**2)**(3/2)
    return -force_mag * np.array([x, y, z])

# Time integration using Leapfrog method
def leapfrog_step(r, v, dt, M, b):
    # Half-step velocity update
    v_half = v + 0.5 * dt * force_plummer(*r, M, b)
    # Full-step position update
    r_new = r + dt * v_half
    # Full-step velocity update
    v_new = v_half + 0.5 * dt * force_plummer(*r_new, M, b)
    return r_new, v_new

# Simulate a star's orbit
def simulate_orbit(r0, v0, M, b, dt, num_steps):
    positions = np.zeros((num_steps, 3))
    velocities = np.zeros((num_steps, 3))
    r, v = r0, v0
    
    for i in range(num_steps):
        r, v = leapfrog_step(r, v, dt, M, b)
        positions[i] = r
        velocities[i] = v
        
    return positions, velocities

# Initial conditions (position in kpc, velocity in km/s)
r0 = np.array([8.0, 0.0, 0.0])  # Initial position (kpc)
v0 = np.array([0.0, 200.0, 100.0])  # Initial velocity (km/s)
dt = 1e-3  # Time step in Gyr
num_steps = 50000  # Number of time steps

# Simulate orbit
positions, velocities = simulate_orbit(r0, v0, M, b, dt, num_steps)

# 3D Visualization of the orbit
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], color='b', label="Star's Orbit")
ax.set_xlabel('X [kpc]')
ax.set_ylabel('Y [kpc]')
ax.set_zlabel('Z [kpc]')
ax.set_title("Star's Orbit in a Plummer Potential")
plt.legend()
plt.show()
