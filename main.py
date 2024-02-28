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

#Part a, b
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


#part C
deltaui = np.zeros(N_turbine)
ptotnew = 10
ptotold = 0
ptotold2 = 0
it = 0
with open('celldata.dat', 'w') as fileID:
    while ptotnew - ptotold2 > 0.001:
        ptotold2 = ptotnew
        it += 1
        mar = 0
        for l in range(N_turbine - 1):
            ptotold = 0
            mar += 1
            while ptotnew - ptotold > 0.001:
                ptotold = ptotnew
                if q[l] < 1:
                    q[l] *= 1.01

                # Computing velocity deficits
                deltau_wind = velocity_def(N_turbine, k, xR, q)

                # Computing velocity deficits
                v, P = power_turbine(U_wind, A_rotor, rho_air, deltau_wind, q)
                ptotnew = sum(P)
                fileID.write(f'{it} {mar} {ptotnew:.8f}\n')

        # marching along the points

# Plotting Turbine Power (Sequential Optimization)
plt.figure(3)
plt.bar(range(1, N_turbine + 1), P)
plt.grid(True)
plt.xlabel('Turbine Number')
plt.ylabel('Produced Power [W]')

plt.figure(4)
plt.scatter(np.arange(N_turbine) * xR, np.zeros(N_turbine), s=200, c=P, cmap='viridis', edgecolors='k')
plt.grid(True)
c = plt.colorbar()
c.set_label('Power [W]')

# Plotting Induction Factor (Sequential Optimization)
plt.figure(5)
plt.bar(range(1, N_turbine + 1), q)
plt.grid(True)
plt.xlabel('Turbine Number')
plt.ylabel('q')

plt.figure(6)
plt.scatter(np.arange(N_turbine) * xR, np.zeros(N_turbine), s=200, c=q, cmap='viridis', edgecolors='k')
plt.grid(True)
plt.title("q")
c = plt.colorbar()
c.set_label('q')

plt.show()

