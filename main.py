from _collections import deque
from plot import create_plot
import numpy as np
from country import CountryCreator
from seir import seir
from scipy.special import binom, comb
from decimal import *
import math

# import matplotlib.pyplot as plt
countries_arr = CountryCreator.initialization()
FATALITY_RATE = 0.0087
DAYS_TO_DEATH = 17.3
DOUBLING_TIME = 6.18
INCUBATION_PERIOD = 5.5
AVG_PASS_ON_PLANE = 90
AIR_TRANSPORT_USAGE = 0.6
ROAD_TRANSPORT_USAGE = 1 - AIR_TRANSPORT_USAGE

total_arrives = 0.
for _, country in countries_arr.items():
    total_arrives += float(country.arrive)

#
# def binom(n,k): # better version - we don't need two products!
#     if not 0<=k<=n: return 0
#     b=1
#     for t in range(min(k,n-k)):
#         b*=n; b/=t+1; n-=1
#     return b

def infec_probability(prob_group, population, infected):
    n = prob_group
    probability = 0.
    q = infected / population
    p = 1 - q
    prob_arr = []
    for k in range(prob_group):

        probability += binom(n, k) * p ** k * q ** (n - k)
        prob_arr.append(probability)
        if math.isnan(probability):
            print("lal")
    print(prob_arr)
    print(probability)
    return prob_arr, probability

infec_probability(7000, 10000000, 1000)

def infec(code):
    scale = 1
    road_dep = countries_arr[code].departure * ROAD_TRANSPORT_USAGE
    pop = countries_arr[code].population
    infec_people = countries_arr[code].true_cases + countries_arr[code].inc_cases
    # while road_dep % 10 == 0 and pop % 10 == 0 and infec_people
    # prob_arr, probability = infec_probability(countries_arr[code].departure * ROAD_TRANSPORT_USAGE, countries_arr[code].population, countries_arr[code].inc_cases + countries_arr[code].true_cases)


def main(data):
    countries_arr['CHN'].true_cases = 1

    for i in range(int(data)):
        print(countries_arr)
        for code, country in countries_arr.items():
            if country.true_cases > 0 or country.inc_cases > 0:
                country.deaths, country.inc_cases, country.true_cases, country.recovered = seir(
                    N=float(country.population) - float(country.deaths), alpha=1 / INCUBATION_PERIOD, beta=0.4,
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
