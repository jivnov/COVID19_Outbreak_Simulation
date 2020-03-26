import numpy as np
from scipy.integrate import odeint
import math as math
import matplotlib.pyplot as plt


def deriv(y, t, N, c, beta, q, m, b, f, sigma, lamb, deltaI, gammaI, gammaH, alpha):
    S, E, I, B, Q, H, R = y
    dSdt = - (((beta * c + c * q * (1 - beta)) * S * I) / N) - m * S + lamb * Q + b * (1 - f) * B
    dEdt = ((beta * c * (1 - q) * S * I) / N) - sigma * E
    dIdt = sigma * E - (deltaI + alpha + gammaI) * I
    dBdt = (beta * c * q * S * I) / N + m * S - b * B
    dQdt = ((1 - beta) * c * q * S * I) / N - lamb * Q
    dHdt = deltaI * I + b * f * B - (alpha + gammaH) * H
    dRdt = gammaI * I + gammaH * H
    return dSdt, dEdt, dIdt, dBdt, dQdt, dHdt, dRdt


def seibqhr(c0, cb, r1, beta, q0, qm, r2, m, b, f, sigma, lamb, deltaI0, deltaIf, r3, gammaI, gammaH, alpha, S0, E0, I0,
            B0, Q0, H0, R0):
    """
    :param c0: Contact rate at the initial time
    :param cb: Minimum contact rate under the current control strategies
    :param r1: Exponential decreasing rate of contact rate
    :param beta: Probability of transmission per contact
    :param q0: Quarantined rate of exposed individuals at the initial time
    :param qm: Maximum quarantined rate of exposed individuals under the current control strategies
    :param r2: Exponential increasing rate of quarantined rate of exposed individuals
    :param m: Transition rate of susceptible individuals to the suspected class
    :param b: Detection rate of the suspected class
    :param f: Confirmation ratio: Transition rate of exposed individuals in the suspected class to the quarantined infected class
    :param sigma: Transition rate of exposed individuals to the infected class
    :param lamb: Rate at which the quarantined uninfected contacts were released into the wider community
    :param deltaI0: Initial transition rate of symptomatic infected individuals to the quarantined infected class
    :param deltaIf: Fastest diagnose rate
    :param r3: Exponential decreasing rate of diagnose rate
    :param gammaI: Recovery rate of infected individuals
    :param gammaH: Recovery rate of quarantined infected individuals
    :param alpha: Disease-induced death rate
    :param S0: Initial susceptible population
    :param E0: Initial exposed population
    :param I0: Initial infected population
    :param B0: Initial suspected population
    :param Q0: Initial quarantined susceptible population
    :param H0: Initial quarantined infected population
    :param R0: Initial recovered population
    :return:
    """

    t = np.linspace(0, 1, 2)
    N = S0 + E0 + I0 + B0 + Q0 + H0 + R0
    y0 = S0, E0, I0, B0, Q0, H0, R0

    c = (c0 - cb) * math.e ** -r1 + cb
    q = (q0 - qm) * math.e ** -r2 + qm
    deltaI = 1 / ((1 / deltaI0 - 1 / deltaIf) * math.e ** -r3 + 1 / deltaIf)

    ret = odeint(deriv, y0, t, args=(N, c, beta, q, m, b, f, sigma, lamb, deltaI, gammaI, gammaH, alpha))
    S, E, I, B, Q, H, R = ret.T

    # print(S)
    # for i in range(360):
    # print(S[i] + "    " + E[i] + "     " + I[i] + "    " + R[i])

    # Plot the data on three separate curves for S(t), I(t) and R(t)

    return S[-1], E[-1], I[-1], B[-1], Q[-1], H[-1], R[-1], c, q, deltaI

# st, et, it, rt = 0, 0, 100, 0
# n = 1000000000
# S = [n - 100]
# E = [0]
# I = [100]
# R = [0]
# for i in range(250):
#     n, st, et, it, rt = seir(n, 1 / 5.5, 0.4, 0.02, 0.00001, E[-1], I[-1], R[-1])
#     S.append(st)
#     E.append(et)
#     I.append(it)
#     R.append(rt)
# print(S)
#
# fig = plt.figure(facecolor='w')
# ax = fig.add_subplot(111, axisbelow=True)
# tlin = np.linspace(0, 250, 251)
# S = np.array(S)
# E = np.array(E)
# I = np.array(I)
# R = np.array(R)
# ax.plot(tlin, S / 1000000000, 'b', alpha=0.5, lw=2, label='Susceptible')
# ax.plot(tlin, E / 1000000000, 'orange', alpha=0.5, lw=2, label='Susceptible')
# ax.plot(tlin, I / 1000000000, 'r', alpha=0.5, lw=2, label='Infected')
# ax.plot(tlin, R / 1000000000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
# ax.set_xlabel('Time /days')
# ax.set_ylabel('Number (1000s)')
# ax.set_ylim(0, 1.2)
# ax.yaxis.set_tick_params(length=0)
# ax.xaxis.set_tick_params(length=0)
# ax.grid(b=True, which='major', c='w', lw=2, ls='-')
# legend = ax.legend()
# legend.get_frame().set_alpha(0.5)
# for spine in ('top', 'right', 'bottom', 'left'):
#     ax.spines[spine].set_visible(False)
# plt.show()
