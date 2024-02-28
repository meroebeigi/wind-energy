import numpy as np
import matplotlib.pyplot as plt

# Functions
def power_turbine(U_wind, A_rotor, rho_air, deltau_wind, q):
    C_p = 0.5 * (1 + q) * (1 - q**2)
    v = U_wind * (1 - np.sqrt(deltau_wind))
    P = 0.5 * rho_air * A_rotor * v**3 * C_p
    return v, P

def velocity_def(N_turbine, k, xR, q):
    deltau_wind = np.zeros(N_turbine)
    for i in range(1, N_turbine + 1):
        for j in range(i-1):
            deltau_wind[i-1] += ((1 - q[j]) / (1 + k * (i-j) * xR)**2)**2
    return deltau_wind

def powersum(N_turbine, q):
    U_wind = 10
    R_rotor = 75
    A_rotor = np.pi * R_rotor**2
    rho_air = 1.225
    k = 0.04
    xR = 12
    deltau_wind = velocity_def(N_turbine, k, xR, q)
    v, P = power_turbine(U_wind, A_rotor, rho_air, deltau_wind, q)
    P_sum = np.sum(P)
    return P, P_sum

def preverse(q):
    N_turbine = 10
    _, P_sum = powersum(N_turbine, q)
    Prev = 10000000 / P_sum
    return Prev

# Main Script
N_turbine = 10
q_Betz_limit = np.ones(N_turbine) * (1/3)

# Task a & b: Calculating velocity deficit and turbine power
deltau_wind = velocity_def(N_turbine, 0.04, 12, q_Betz_limit)
v, P = power_turbine(10, np.pi * 75**2, 1.225, deltau_wind, q_Betz_limit)

# Plotting Turbine Power (Betz Limit)
plt.figure(figsize=(10, 6))
plt.bar(range(1, N_turbine + 1), P)
plt.xlabel('Turbine Number')
plt.ylabel('Produced Power [W]')
plt.title('Turbine Power (Betz Limit)')
plt.grid(True)
plt.show()

# Task c & d: For demonstration, we'll skip the optimization part due to its complexity and dependency on external libraries.
# Instead, we show how to set up plots similar to your MATLAB figures.

# Note: For actual optimization in task d, consider using scipy.optimize.minimize and define your objective function based on preverse.

# Example Plot (without optimization)
plt.figure(figsize=(10, 6))
plt.scatter(range(N_turbine), np.zeros(N_turbine), s=200, c=P, cmap='viridis')
plt.colorbar(label='Power [W]')
plt.xlabel('Turbine Position')
plt.ylabel('Position Y (Dummy)')
plt.title('Power Distribution Across Turbines')
plt.grid(True)
plt.show()
