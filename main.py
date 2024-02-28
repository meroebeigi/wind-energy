import numpy as np
import matplotlib.pyplot as plt
from func import velocity_def, power_turbine

# Defining Induction Factor
q_Betz_limit = (1/3) * np.ones(10)
q = q_Betz_limit.copy()
deltau_wind = q_Betz_limit.copy()

# Number of turbines
N_turbine = 10

# Free wind speed
U_wind = 10  # [m/s]

# Rotor disc radius
R_rotor = 75  # [m]

# Rotor disc area
A_rotor = np.pi * R_rotor**2  # [m^2]

# Turbine spacing
dx = 12 * R_rotor  # [m/s]

# Wake-decay parameter
k = 0.04

# Air density
rho_air = 1.225  # [kg/m^3]

xR = 12

# Calculating velocity deficit
deltau_wind = velocity_def(N_turbine, k, xR, q)

# Calculating Turbine power
v, P = power_turbine(U_wind, A_rotor, rho_air, deltau_wind, q)

# Plotting Turbine Power (Betz Limit)
plt.figure(1)
plt.bar(range(1, N_turbine + 1), P)
plt.grid(True)
plt.xlabel('Turbine Number')
plt.ylabel('Produced Power [W]')

plt.figure(2)
plt.scatter(np.arange(N_turbine) * xR, np.zeros(N_turbine), s=200, c=P, cmap='viridis', edgecolors='k')
plt.grid(True)
c = plt.colorbar()
c.set_label('Power [W]')

plt.show()


