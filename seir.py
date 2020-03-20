import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


def deriv(y, t, N, alpha, beta, gamma, mu):
    S, E, I, R = y
    dSdt = - beta * (I / N) * S  # + mu * N
    dEdt = beta * (I / N) * S - (mu + alpha) * E
    dIdt = alpha * E - (gamma + mu) * I
    dRdt = gamma * I - mu * R
    return dSdt, dEdt, dIdt, dRdt


def seir(N, alpha, beta, gamma, mu, E0, I0, R0):
    t = np.linspace(0, 1, 2)
    S0 = N - I0 - E0 - R0
    y0 = S0, E0, I0, R0
    ret = odeint(deriv, y0, t, args=(N, alpha, beta, gamma, mu))
    S, E, I, R = ret.T

    # print(S)
    deaths = N - (I[-1] + E[-1] + R[-1] + S[-1])

    # for i in range(360):
    # print(S[i] + "    " + E[i] + "     " + I[i] + "    " + R[i])

    # Plot the data on three separate curves for S(t), I(t) and R(t)

    return deaths, E[-1], I[-1], R[-1]


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
