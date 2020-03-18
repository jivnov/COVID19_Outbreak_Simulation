import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


def deriv(y, t, N, alpha, beta, gamma, mu):
    S, E, I, R = y
    dSdt = - mu * S - beta * (I / N) * S  # + mu * N
    dEdt = beta * (I / N) * S - (mu + alpha) * E
    dIdt = alpha * E - (gamma + mu) * I
    dRdt = gamma * I - mu * R
    return dSdt, dEdt, dIdt, dRdt


def seir(N, alpha, beta, gamma, mu, I0, E0, R0):
    t = np.linspace(1, 1000, 1000)
    S0 = N - I0 - E0 - R0
    y0 = S0, E0, I0, R0
    ret = odeint(deriv, y0, t, args=(N, alpha, beta, gamma, mu))
    S, E, I, R = ret.T

    print(S)
    print(N - I[-1] - E[-1] - R[-1] - S[-1])

    # for i in range(360):
    # print(S[i] + "    " + E[i] + "     " + I[i] + "    " + R[i])

    # Plot the data on three separate curves for S(t), I(t) and R(t)
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(111, axisbelow=True)
    ax.plot(t, S / 1000, 'b', alpha=0.5, lw=2, label='Susceptible')
    ax.plot(t, E / 1000, 'orange', alpha=0.5, lw=2, label='Susceptible')
    ax.plot(t, I / 1000, 'r', alpha=0.5, lw=2, label='Infected')
    ax.plot(t, R / 1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
    ax.set_xlabel('Time /days')
    ax.set_ylabel('Number (1000s)')
    ax.set_ylim(0, 1.2)
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    plt.show()


seir(1000, 1 / 6.5, 0.03, 0.01, 0.0001, 1, 0, 0)
