import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from func import powersum, preverse

# Define the optimization routine
def optimize(N_turbine, k, dx_over_R, U_wind, R_rotor, rho_air):
    q_betz_limit = (1/3) * np.ones(N_turbine)
    A_rotor = np.pi * R_rotor**2
    dx = dx_over_R * R_rotor

    # Define the objective function for optimization
    def objective(q):
        _, P = powersum(N_turbine, q)
        return -np.sum(P)

    # Solve using minimize
    result = minimize(objective, q_betz_limit, method='L-BFGS-B', options={'disp': True})
    solution = result.x
    objectiveValue = -result.fun

    new = np.zeros(N_turbine)
    delta = 0
    delta1 = 0

    for i in range(N_turbine):
        new[i] = 1/2 * rho_air * U_wind**3 * A_rotor * (((1 + solution[i]) / 2) * (1 - solution[i]**2)) * (1 - delta)**3
        delta1 = delta1**2 + ((1 - solution[i]) / (1 + k * dx_over_R)**2)**2
        delta = np.sqrt(delta1)

    P = new
    return solution, P

# Parameter sets to iterate over
N_values = [5, 10, 20]
k_values = [0.02, 0.04, 0.06]
dx_over_R_values = [8, 12, 16]

# Create figure for the q values
fig_q, axes_q = plt.subplots(len(N_values), len(k_values), figsize=(15, 10), constrained_layout=True)

# Create figure for the power values
fig_P, axes_P = plt.subplots(len(N_values), len(k_values), figsize=(15, 10), constrained_layout=True)

for i, N in enumerate(N_values):
    for j, k in enumerate(k_values):
        # Select dx/R ratio (assuming one value for simplicity here)
        dx_over_R = dx_over_R_values[1]  # Or iterate over this if you want all combinations

        # Perform the optimization to get q and P
        q_optimized, P_optimized = optimize(N, k, dx_over_R, U_wind=10, R_rotor=75, rho_air=1.225)
        
        # Plotting q values
        ax_q = axes_q[i, j]
        ax_q.bar(range(1, N + 1), q_optimized)
        ax_q.set_title(f'q (k={k}, N={N})')
        ax_q.set_xlabel('Turbine Number')
        ax_q.set_ylabel('Induction Factor')
        ax_q.grid(True)

        # Plotting P values
        ax_P = axes_P[i, j]
        ax_P.bar(range(1, N + 1), P_optimized)
        ax_P.set_title(f'P (k={k}, N={N})')
        ax_P.set_xlabel('Turbine Number')
        ax_P.set_ylabel('Power [W]')
        ax_P.grid(True)



# Adjust the layout
plt.tight_layout()
plt.show()
# Rest of your imports and function definitions remain the same

# Parameters to iterate over
N_values = [5, 10, 20]  # Number of turbines
dx_over_R_values = [8, 12, 16]  # Different x/R ratios

# Fixed k value
k_fixed = 0.04  # You can change this to 0.02 or 0.06 as needed

# Create figures for q and P values
fig_q, axes_q = plt.subplots(len(N_values), len(dx_over_R_values), figsize=(15, 15), constrained_layout=True)
fig_P, axes_P = plt.subplots(len(N_values), len(dx_over_R_values), figsize=(15, 15), constrained_layout=True)

for i, N in enumerate(N_values):
    for j, dx_over_R in enumerate(dx_over_R_values):
        # Perform the optimization to get q and P for the fixed k value
        q_optimized, P_optimized = optimize(N, k_fixed, dx_over_R, U_wind=10, R_rotor=75, rho_air=1.225)
        
        # Plotting q values with green color
        ax_q = axes_q[i, j]
        ax_q.bar(range(1, N + 1), q_optimized, color='green')
        ax_q.set_title(f'q (k={k_fixed}, dx/R={dx_over_R}, N={N})')
        ax_q.set_xlabel('Turbine Number')
        ax_q.set_ylabel('Induction Factor')
        ax_q.grid(True)
        
        # Plotting P values with orange color
        ax_P = axes_P[i, j]
        ax_P.bar(range(1, N + 1), P_optimized, color='orange')
        ax_P.set_title(f'P (k={k_fixed}, dx/R={dx_over_R}, N={N})')
        ax_P.set_xlabel('Turbine Number')
        ax_P.set_ylabel('Power [W]')
        ax_P.grid(True)

# Adjust the layout and show the plots
fig_q.suptitle('Induction Factor for Different N and dx/R Values (k Fixed)', fontsize=16)
fig_P.suptitle('Power Output for Different N and dx/R Values (k Fixed)', fontsize=16)
plt.show()