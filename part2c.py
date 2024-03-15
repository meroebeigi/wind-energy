import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def Area_ov(rw, ydis, R_rotor):
    T1 = rw**2 * np.arccos((rw**2 - R_rotor**2 + ydis**2) / (2 * ydis * rw))
    T2 = R_rotor**2 * np.arccos((R_rotor**2 - rw**2 + ydis**2) / (2 * ydis * R_rotor))
    T3 = ((rw + R_rotor)**2 - ydis**2) * (ydis**2 - (rw - R_rotor)**2)
    ovl = T1 + T2 - 0.5 * T3**0.5
    return ovl

def overlap(N_turbine, M_turbine, R_rotor, k, xs, ys):
    NM = N_turbine * M_turbine
    ovl = np.zeros((NM, NM))
    for i in range(NM):
        for j in range(NM):
            xdis = xs[i] - xs[j]
            if xdis > 0:
                rw = R_rotor + (k * abs(xdis))
                rlap = rw + R_rotor
                fullap = rw - R_rotor

                ydis = abs(ys[i] - ys[j])
                if fullap < ydis < rlap:
                    ovl[i, j] = Area_ov(rw, ydis, R_rotor)
                elif ydis <= fullap:
                    ovl[i, j] = np.pi * R_rotor**2
                else:
                    ovl[i, j] = 0
            else:
                ovl[i, j] = 0
    ovl /= np.pi * R_rotor**2
    return ovl
def Power_turb(U_wind, A_rotor, rho_air, delta_u_s, qs):
    C_p = 0.5 * (1 + qs) * (1 - qs**2)
    v = U_wind * (1 - np.sqrt(delta_u_s))
    P = 0.5 * (rho_air * A_rotor * v**3 * C_p)
    return v, P

def Velocity_def(N_turbine, M_turbine, R_rotor, k, xs, qs, ovl):
    NM = N_turbine * M_turbine
    delta_u_s = np.zeros(NM)
    for i in range(NM):
        for j in range(NM):
            delta_u_s[i] += ovl[i, j] * ((1 - qs[j]) / (1 + k * abs(xs[i] - xs[j]) / R_rotor)**2)**2
    return delta_u_s

def Power_sum(N_turbine, M_turbine, qs):
    NM = N_turbine * M_turbine
    q_Betz_limit = (1/3) * np.ones((N_turbine, M_turbine))
    q = q_Betz_limit
    qs = q.reshape(-1, 1)
    P = np.ones((N_turbine, M_turbine))
    Ps = P.reshape(-1, 1)
    delta_u = np.ones((N_turbine, M_turbine))
    delta_u_s = delta_u.reshape(-1, 1)
    delta_u = np.ones((N_turbine, M_turbine))
    U_wind = 10
    k = 0.04
    rho_air = 1.225
    R_rotor = 41.2
    dx = 858.562
    dy = -481.706
    angl = 45
    angl += 90
    A_rotor = 10
    x, y = Wind_farm(angl, N_turbine, M_turbine)
    xs = x.flatten()
    ys = y.flatten()
    ovl = overlap(N_turbine, M_turbine, R_rotor, k, xs, ys)
    delta_u_s = Velocity_def(N_turbine, M_turbine, R_rotor, k, xs, qs, ovl)
    v, P = Power_turb(U_wind, A_rotor, rho_air, delta_u_s, qs)
    P_sum = np.sum(P)
    return P, P_sum





def Wind_farm(angl, N_turbine, M_turbine):
    R_rotor = 41.2
    dx = 481.70637862320414186300933810117
    dy = 858.56241559894146317763280998799
    xR = dx / R_rotor
    yR = dy / R_rotor
    x0, y0 = 0, 0
    x = np.ones((N_turbine, M_turbine))
    y = np.ones((N_turbine, M_turbine))
    for i in range(N_turbine):
        for j in range(M_turbine):
            x[i, j] = (i - 1) * dx + np.tan(np.deg2rad(8)) * (j - 1) * dy
            y[i, j] = (j - 1) * dy + np.tan(np.deg2rad(2)) * (i - 1) * dx
    if angl != 0:
        anglr = -np.deg2rad(angl)
        for i in range(N_turbine):
            for j in range(M_turbine):
                rx = np.cos(anglr) * x[i, j] + np.sin(anglr) * y[i, j]
                ry = -np.sin(anglr) * x[i, j] + np.cos(anglr) * y[i, j]
                x[i, j] = rx
                y[i, j] = ry
    return x, y


def P_reverse(qs):
    N_turbine = 8
    M_turbine = 9
    NM = N_turbine * M_turbine
    Ps = np.ones(NM)
    P_sum = 1
    _, P_sum = Power_sum(N_turbine, M_turbine, qs)
    P_rev = 10000000 / P_sum
    return P_rev

def p_total(angl):
    N_turbine = 9
    M_turbine = 8
    NM = N_turbine * M_turbine
    q_Betz_limit = (1/3) * np.ones((N_turbine, M_turbine))
    q = q_Betz_limit
    qs = q.reshape(-1, 1)
    P = np.ones((N_turbine, M_turbine))
    Ps = P.reshape(-1, 1)
    delta_u = np.ones((N_turbine, M_turbine)).flatten()
    U_wind = 10
    k = 0.04
    rho_air = 1.225
    R_rotor = 41.2
    dx = 858.562
    dy = -481.706
    A_rotor = np.pi * R_rotor**2
    x, y = Wind_farm(angl, N_turbine, M_turbine)
    xs = x.flatten()
    ys = y.flatten()
    ovl = overlap(N_turbine, M_turbine, R_rotor, k, xs, ys)
    delta_u_s = Velocity_def(N_turbine, M_turbine, R_rotor, k, xs, qs, ovl)
    v, P = Power_turb(U_wind, A_rotor, rho_air, delta_u_s, qs)
    Power_total = np.sum(P)
    return Power_total


def p_tot_opt(angl):
    N_turbine = 9
    M_turbine = 8
    NM = N_turbine * M_turbine
    q_Betz_limit = (1/3) * np.ones((N_turbine, M_turbine))
    q = q_Betz_limit
    qs = q.reshape(-1, 1)
    P = np.ones((N_turbine, M_turbine))
    Ps = P.reshape(-1, 1)
    delta_u = np.ones((N_turbine, M_turbine))
    delta_u_s = delta_u.reshape(-1, 1)
    U_wind = 10  # m/sU_wind = 10  # m/s
    k = 0.04
    rho_air = 1.225  # kg/m^3
    R_rotor = 41.2  # m
    dx = 858.562
    dy = -481.706
    A_rotor = np.pi * R_rotor**2  # m^2
    x, y = Wind_farm(angl, N_turbine, M_turbine)
    xs = x.flatten()
    ys = y.flatten()
    # Calculating the overlap area
    ovl = overlap(N_turbine, M_turbine, R_rotor, k, xs, ys)
    delta_u_i = np.zeros(N_turbine)
    p_tot_new = 10
    p_tot_old = 0
    p_tot_old_2 = 0
    it = 0
    # Open file for writing
    with open('celldata2.dat', 'w') as fileID:
        while (p_tot_new - p_tot_old_2) > 0.001:
            p_tot_old_2 = p_tot_new
            it += 1
            mar = 0
            # Marching along the points
            for l in range(NM):
                p_tot_old = 0
                mar += 1

            # Iteration at one point
            while (p_tot_new - p_tot_old) > 0.001:
                p_tot_old = p_tot_new

                if qs[l] < 1:
                    qs[l] = qs[l] * 1.001

                # Calculating velocity deficit
                delta_u_s = Velocity_def(N_turbine, M_turbine, R_rotor, k, xs, qs, ovl)

                # Calculating Turbine power
                v, P = Power_turb(U_wind, A_rotor, rho_air, delta_u_s, qs)
                p_tot_new = np.sum(P)

                # Writing data to file
                fileID.write(f'{it} {mar} {p_tot_new}\n')
                # Calculate total power
                Power_total = p_tot_new


# Load data from Excel file
num = pd.read_excel('file3.xlsx', header=None)

# Plotting the potential gain
plt.figure(figsize=(8, 6))
plt.plot(num.iloc[:, 0], num.iloc[:, 1:], label=['k=0.025', 'k=0.04', 'k=0.05'])
plt.legend(loc='upper left')
plt.xlabel(r'$\theta$')
plt.ylabel(r'$\xi$')
plt.xlim([0, 360])
plt.ylim([0, 1])
plt.title('Gain Potential as a Function of Wind Direction')
plt.grid(True)
plt.show()
