from _collections import deque
from plot import create_plot
import numpy as np
from country import CountryCreator
from seir import seir


# import matplotlib.pyplot as plt


def main(data):
    countries_arr = CountryCreator.initialization()

    fatality_rate = 0.0087
    days_to_death = 17.3
    doubling_time = 6.18
    incubation_period = 5.5

    for country in countries_arr:
        if country.country_code == 'CHN':
            country.true_cases = 1

    for i in range(int(data)):
        for country in countries_arr:
            if country.true_cases > 0 or country.inc_cases > 0:
                country.deaths, country.inc_cases, country.true_cases, country.recovered = seir(
                    N=float(country.population) - float(country.deaths), alpha=1 / incubation_period, beta=0.4,
                    gamma=0.02,
                    mu=0.00001,
                    E0=country.inc_cases, I0=country.true_cases, R0=country.recovered)
                country.true_cases_arr.append(country.true_cases)
                country.deaths_arr.append(country.deaths)
                country.inc_cases_arr.append(country.inc_cases)
                country.recovered_arr.append(country.recovered)
            else:
                country.true_cases_arr.append(0)
                country.deaths_arr.append(0)
                country.inc_cases_arr.append(0)
                country.recovered_arr.append(0)

    for country in countries_arr:
        if country.country_code == 'CHN':
            print(country.true_cases)
            print(country.recovered)
            print(country.deaths)
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

    healthy = 7000000000
    days = int(data)

    infectivity = 0.0000000001
    mortality = 0.1
    recovery = 1 - mortality
    disease_duration = 14

    incubation_deque = deque()
    for i in range(14):
        incubation_deque.append(0)

    deaths_deque = deque()
    for i in range(14):
        deaths_deque.append(0)

    result = {
        "confirmed": 10,
        "deaths": 0,
        "recovered": 0,
        "plot": "0"
    }

    confirmed = []
    deaths = []
    recovered = []

    for i in range(days):
        new_confirmed = int(healthy * infectivity * result["confirmed"])
        # print(result["confirmed"])
        result["confirmed"] += new_confirmed
        healthy -= new_confirmed

        new_deaths = int(result["confirmed"] * mortality / disease_duration)
        result["deaths"] += new_deaths
        result["confirmed"] -= new_deaths

        incubation_deque.append(new_confirmed)
        deaths_deque.append(new_deaths)
        new_recovered = int(incubation_deque.popleft() - deaths_deque.popleft())
        result["recovered"] += new_recovered
        result["confirmed"] -= new_recovered

        # print("healthy: " + str(healthy) + "; confirmed: " + str(result["confirmed"]) + "; deaths: " + str(
        #     result["deaths"]) + "; recovered: " + str(result["recovered"]))

        confirmed.append(result["confirmed"])
        deaths.append(result["deaths"])
        recovered.append(result["recovered"])

    plot_data = [days, confirmed, deaths, recovered]
    result["plot"] = create_plot(plot_data)

    return result
