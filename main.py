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



from scipy.optimize import minimize

# Task d - Optimization

N_turbine = 10
q_betz_limit = (1/3) * np.ones(N_turbine)
q = q_betz_limit.copy()
P = np.ones(N_turbine)
Psum = 1

# Call Powersum function (assuming you have this function implemented in a file func.py)
from func import powersum, preverse

P, Psum = powersum(N_turbine, q)

# Set nondefault solver options
options = {'disp': True}

# Define the objective function for optimization
def objective(q):
    _, P = powersum(N_turbine, q)
    return -np.sum(P)


# Solve using minimize
result = minimize(objective, q_betz_limit, method='L-BFGS-B', options=options)

solution = result.x
objectiveValue = -result.fun

# Task d - Plots

# Data (assuming similar data as provided)
U_wind = 10  # [m/s]
R_rotor = 75  # [m]
A_rotor = np.pi * R_rotor**2  # [m^2]
dx = 12 * R_rotor  # [m/s]
k = 0.04
rho_air = 1.225  # [kg/m^3]
xR = 12

new = np.zeros(N_turbine)
P = np.zeros(N_turbine)

q2 = np.array([0.607312424147279,
               0.704185438135635,
               0.695674289386889,
               0.694196338540093,
               0.692469442362254,
               0.689837787791577,
               0.685312467691720,
               0.676352090943476,
               0.651726189855121,
               0.333333324564787])

delta = 0
delta1 = 0

for i in range(N_turbine):
    new[i] = 1/2 * rho_air * U_wind**3 * A_rotor * (((1 + solution[i]) / 2) * (1 - solution[i]**2)) * (1 - delta)**3
    delta1 = delta1**2 + ((1 - solution[i]) / (1 + k * (dx / R_rotor))**2)**2
    delta = np.sqrt(delta1)
    P[i] = new[i]

P_tot = sum(P)

# Plotting Induction factor (minimize)
plt.figure(7)
plt.scatter(np.arange(N_turbine) * 12, np.zeros(N_turbine), s=200, c=solution, cmap='viridis', edgecolors='k')
plt.grid(True)
plt.title("Optimized q variation through each turbine")
c = plt.colorbar()
c.set_label('q ')

# Plotting Induction Turbine Power (minimize)
plt.figure(8)
plt.bar(range(1, N_turbine + 1), P)
plt.title('Power produced with optimized q')
plt.grid(True)
plt.xlabel('Turbine number')
plt.ylabel('Power [W]')

plt.figure(9)
plt.scatter(np.arange(N_turbine) * 12, np.zeros(N_turbine), s=200, c=P / 10**3, cmap='viridis', edgecolors='k')
plt.grid(True)
plt.title("Power produced with optimized q")
c = plt.colorbar()
c.set_label('Power [kW]')

plt.show()
