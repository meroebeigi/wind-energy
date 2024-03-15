import numpy as np
import matplotlib.pyplot as plt

# Functions
def power_turbine(U_wind, A_rotor, rho_air, deltau_wind, q):
    C_p = 0.5 * (1 + q) * (1 - q**2)
    v = U_wind * (1 - np.sqrt(deltau_wind))
    P = 0.5 * rho_air * A_rotor * v**3 * C_p
    return v, P.flatten()  # Flatten P array to make it 1D


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